"""Ping do app no Streamlit Cloud para evitar o standby por inatividade.

Requisicao HTTP simples nao serve: o Streamlit so conta uma sessao ativa
quando o navegador executa o JS e abre o WebSocket em /_stcore/stream. Por
isso aqui usamos um Chromium headless de verdade, que carrega a pagina,
espera o WebSocket subir e mantem a aba aberta por alguns segundos.

Dois detalhes que custaram caro e por isso estao anotados:

1. No Streamlit Cloud o app roda dentro de um iframe (/~/+/), entao o
   innerText da pagina de cima tem so algumas dezenas de caracteres. O
   conteudo precisa ser conferido dentro do frame.
2. Na API sincrona do Playwright os eventos so sao despachados durante
   chamadas do proprio Playwright. Um time.sleep() trava a thread sem
   despachar nada, e a lista de websockets nunca enche. Toda espera aqui
   usa pagina.wait_for_timeout().

Por padrao o script BLOQUEIA o Google Analytics, para nao encher o GA4 de
sessoes falsas a cada 3 horas. Rode com PING_ALLOW_GA=1 quando quiser
justamente confirmar no GA4 que o ping chegou ate o fim.
"""

import os
import sys

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

APP_URL = "https://confirme-cha.streamlit.app"

SEGUNDOS_NA_PAGINA = 20      # aba aberta apos conectar, para contar a sessao
TIMEOUT_MS = 90_000
TIMEOUT_WEBSOCKET_MS = 60_000
TIMEOUT_CONTEUDO_MS = 60_000
MIN_CARACTERES = 200         # conteudo minimo esperado dentro do iframe

# UA real: o Chromium headless anuncia "HeadlessChrome" por padrao, o que faz
# o GA4 descartar o acesso como bot.
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

PERMITIR_GA = os.environ.get("PING_ALLOW_GA") == "1"
CAMINHO_SCREENSHOT = os.environ.get("PING_SCREENSHOT", "ping.png")


def esperar(pagina, condicao, timeout_ms, passo_ms=500):
    """Espera `condicao()` virar verdadeira.

    Usa pagina.wait_for_timeout (e nao time.sleep) para que o Playwright
    despache os eventos de rede enquanto esperamos.
    """
    for _ in range(max(1, timeout_ms // passo_ms)):
        if condicao():
            return True
        pagina.wait_for_timeout(passo_ms)
    return condicao()


def frame_do_app(pagina):
    """Devolve o frame onde o app roda, ou None se ainda nao existe."""
    for frame in pagina.frames:
        if "/~/+/" in frame.url:
            return frame
    return None


def texto_do_app(pagina):
    """Quantidade de texto ja renderizada dentro do iframe do app."""
    frame = frame_do_app(pagina)
    if frame is None:
        return 0
    try:
        return frame.evaluate(
            "document.body ? document.body.innerText.trim().length : 0"
        )
    except Exception:
        return 0  # frame navegando; tenta de novo no proximo passo


def main():
    websockets = []
    ga_requests = []
    conectou = False
    renderizou = False

    with sync_playwright() as p:
        navegador = p.chromium.launch(
            args=["--disable-blink-features=AutomationControlled"]
        )
        contexto = navegador.new_context(
            user_agent=USER_AGENT,
            viewport={"width": 1366, "height": 768},
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
        )
        pagina = contexto.new_page()
        pagina.on("websocket", lambda ws: websockets.append(ws.url))

        if PERMITIR_GA:
            pagina.on(
                "request",
                lambda req: (
                    ga_requests.append(req.url)
                    if "googletagmanager.com" in req.url
                    or "google-analytics.com" in req.url
                    else None
                ),
            )
        else:
            # Corta o gtag para o ping nao virar sessao no relatorio do GA4.
            pagina.route("**://*.googletagmanager.com/**", lambda r: r.abort())
            pagina.route("**://*.google-analytics.com/**", lambda r: r.abort())

        print(f"abrindo {APP_URL} ...")
        try:
            resposta = pagina.goto(
                APP_URL, wait_until="domcontentloaded", timeout=TIMEOUT_MS
            )
            print(f"HTTP {resposta.status if resposta else '?'} -> {pagina.url}")

            # 1) WebSocket: e isso que o Streamlit conta como sessao ativa.
            conectou = esperar(
                pagina,
                lambda: any("_stcore/stream" in u for u in websockets),
                TIMEOUT_WEBSOCKET_MS,
            )
            print("websocket conectado" if conectou else "websocket NAO subiu")

            # 2) Conteudo dentro do iframe, para saber que o app rodou mesmo.
            renderizou = esperar(
                pagina,
                lambda: texto_do_app(pagina) > MIN_CARACTERES,
                TIMEOUT_CONTEUDO_MS,
            )
            print(f"texto renderizado no app: {texto_do_app(pagina)} caracteres")

            # 3) Mantem a aba viva para a sessao ser contabilizada.
            pagina.wait_for_timeout(SEGUNDOS_NA_PAGINA * 1000)
            print(f"titulo: {pagina.title()}")

        except PlaywrightTimeout as erro:
            print(f"TIMEOUT: {str(erro).splitlines()[0]}")
        finally:
            try:
                pagina.screenshot(path=CAMINHO_SCREENSHOT, full_page=True)
                print(f"screenshot: {CAMINHO_SCREENSHOT}")
            except Exception as erro:
                print(f"nao consegui salvar screenshot: {erro}")
            navegador.close()

    print(f"\nwebsockets abertos: {len(websockets)}")
    for url in websockets:
        print(f"  - {url}")

    if PERMITIR_GA:
        print(f"requisicoes de GA disparadas: {len(ga_requests)}")
        for url in ga_requests[:6]:
            print(f"  - {url[:110]}")
    else:
        print("GA bloqueado (rode com PING_ALLOW_GA=1 para permitir)")

    if not conectou:
        print("\nFALHOU: sem WebSocket, o Streamlit nao conta sessao.")
        return 1
    if not renderizou:
        print("\nFALHOU: WebSocket subiu mas o app nao renderizou conteudo.")
        return 1

    print("\nSessao real estabelecida. App acordado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
