"""Ping do app no Streamlit Cloud para evitar o standby por inatividade.

A raiz do app responde 303 e passa por um fluxo de auth que so termina se o
cliente guardar o cookie de sessao. Um curl simples nao guarda, entra em loop
de redirect e falha. Aqui usamos requests.Session, que mantem os cookies entre
as requisicoes e fecha o handshake como um navegador faria.
"""

import sys
import time

import requests

APP_URL = "https://confirme-cha.streamlit.app"
TIMEOUT = 30
TENTATIVAS = 3
ESPERA_ENTRE_TENTATIVAS = 10

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}


def ping():
    """Abre uma sessao no app. Devolve True se o app respondeu 200."""
    with requests.Session() as sessao:
        sessao.headers.update(HEADERS)

        # 1) Raiz: passa pelo fluxo de auth e estabelece o cookie de sessao.
        inicio = time.monotonic()
        resposta = sessao.get(APP_URL, timeout=TIMEOUT, allow_redirects=True)
        duracao = time.monotonic() - inicio

        print(f"GET /            -> {resposta.status_code} "
              f"({duracao:.2f}s, {len(resposta.history)} redirects)")

        cookies = ", ".join(sessao.cookies.keys()) or "nenhum"
        print(f"cookies da sessao: {cookies}")

        if resposta.status_code != 200:
            print(f"URL final: {resposta.url}")
            return False

        # 2) Segunda requisicao reaproveitando o cookie, ja sem passar pelo auth.
        #    So responde 200 se a sessao do passo anterior valeu de fato.
        health = sessao.get(
            f"{APP_URL}/_stcore/health", timeout=TIMEOUT, allow_redirects=True
        )
        print(f"GET /_stcore/health -> {health.status_code} "
              f"({len(health.content)} bytes)")

        return health.status_code == 200


def main():
    for tentativa in range(1, TENTATIVAS + 1):
        print(f"--- tentativa {tentativa}/{TENTATIVAS} ---")
        try:
            if ping():
                print("\nApp acordado com sucesso.")
                return 0
        except requests.RequestException as erro:
            print(f"falhou: {type(erro).__name__}: {erro}")

        if tentativa < TENTATIVAS:
            time.sleep(ESPERA_ENTRE_TENTATIVAS)

    print("\nApp nao respondeu 200 apos todas as tentativas.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
