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

# Grupos de convidados (aparecem no seletor)
GRUPOS = [
    "Dayane & Wesley",
    "Dayara & Maurício",
    "Família",
]

# Qual bebê cada grupo está celebrando (texto exibido após escolher o grupo)
GRUPO_BEBE = {
    "Dayane & Wesley": "Helena",
    "Dayara & Maurício": "Alice",
    "Família": "Alice e Helena",
}

# Imagens dos convites (salve os arquivos na pasta assets/ com estes nomes)
CONVITE_ALICE = "assets/convite_alice.png"
CONVITE_HELENA = "assets/convite_helena.png"

# ID da planilha do Google Sheets (trecho da URL entre /d/ e /edit)
SHEET_ID = "1vN3zzjPd6opO4Dz61_rZHm01R3qD79EjpNG_QKGiBfY"

# Senha padrão do painel do organizador.
# Recomendado: defina ORGANIZADOR_SENHA no .env (ou nos Secrets do Streamlit)
# em vez de deixar a senha aqui, já que este arquivo vai para o GitHub.
ORGANIZADOR_SENHA = "organizador123"

# Nome da aba (worksheet) dentro da planilha do Google Sheets
NOME_ABA = "confirmacoes"

# Colunas gravadas na planilha (não mude a ordem depois de começar a usar)
COLUNAS = ["data_hora", "nome", "grupo", "presenca", "num_pessoas", "recado"]
