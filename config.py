"""Configurações do app de confirmação de presença do chá de bebê.

São DOIS bebês no mesmo dia e no mesmo local:
  - Alice  → convidados de Dayara & Maurício (tema cereja / rosa)
  - Helena → convidados de Dayane & Wesley (tema abelhinha / amarelo)
  - Família → convidada dos dois

Edite aqui os dados do evento, os grupos e os nomes das imagens dos convites.
"""

# Título e mensagem no topo da página
NOME_EVENTO = "Chá de Bebê da Alice & da Helena"
SUBTITULO = "Confirme sua presença! 🍒🐝"

# Dados do evento (iguais para os dois)
EVENTO_DATA = "13 de setembro de 2026 (sábado)"
EVENTO_HORA = "13h"
EVENTO_LOCAL = "Rua Antônio Riscalla Husne, 692 — Jardim Rio Branco"
# Link do Google Maps do local (Espaço ´R C´ — São Vicente/SP).
# Deixe "" para gerar automaticamente a partir do endereço acima.
EVENTO_MAPS_URL = "https://www.google.com.br/maps/place/Espaco+%C2%B4R+C%C2%B4/@-23.9777355,-46.472848,95m/data=!3m1!1e3!4m15!1m8!3m7!1s0x94ce192f5315a197:0xc03802f41624e061!2sR.+Ant%C3%B4nio+Riscalle+Husne,+692+-+Jardim+Rio+Branco,+S%C3%A3o+Vicente+-+SP,+11347-020!3b1!8m2!3d-23.9778851!4d-46.4729421!16s%2Fg%2F11c15sk56j!3m5!1s0x94ce192f5374a9e1:0x965810e11c3488a0!8m2!3d-23.97773!4d-46.4728276!16s%2Fg%2F11zbt1g7cr?entry=ttu"

# Link da previsão do tempo (São Vicente). Deixe "" para ocultar o botão.
EVENTO_CLIMA_URL = "https://www.meteoprog.com/pt/weather/Saovicente/month/september/"

# Grupos de convidados (aparecem no seletor)
GRUPOS = [
    "Chá da Helena (Dayane & Wesley)",
    "Chá da Alice (Dayara & Maurício)",
    "Ambos",
]

# Qual bebê cada grupo está celebrando (texto exibido após escolher o grupo)
GRUPO_BEBE = {
    "Chá da Helena (Dayane & Wesley)": "Helena",
    "Chá da Alice (Dayara & Maurício)": "Alice",
    "Ambos": "Alice e Helena",
}

# Imagens dos convites (salve os arquivos na pasta assets/ com estes nomes)
CONVITE_ALICE = "assets/convite_alice.png"
CONVITE_HELENA = "assets/convite_helena.png"

# ID da planilha do Google Sheets.
# NÃO versione o ID aqui — ele vem dos Secrets/.env (chave `sheet_id` na seção
# [app], ou a variável SHEET_ID). Este valor é só um fallback vazio.
SHEET_ID = ""

# Senha do painel do organizador.
# NÃO versione a senha aqui — ela vem dos Secrets/.env (chave `organizador_senha`
# na seção [app], ou a variável ORGANIZADOR_SENHA). Este valor é só um fallback vazio.
ORGANIZADOR_SENHA = ""

# Nome da aba (worksheet) dentro da planilha do Google Sheets
NOME_ABA = "confirmacoes"

# Colunas gravadas na planilha (não mude a ordem depois de começar a usar)
COLUNAS = ["data_hora", "nome", "grupo", "presenca", "num_pessoas", "recado"]
