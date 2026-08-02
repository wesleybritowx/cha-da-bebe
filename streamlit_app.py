"""Tela do convidado — confirmação de presença (RSVP) do chá de bebê.

São dois bebês (Alice e Helena) no mesmo dia e local. O convidado escolhe o
grupo e confirma a presença; os dados vão para uma planilha do Google Sheets.
"""

import os

import streamlit as st

import config
from sheets import registrar_confirmacao

st.set_page_config(page_title=config.NOME_EVENTO, page_icon="🍼")

st.title(f"🍼 {config.NOME_EVENTO}")
if config.SUBTITULO:
    st.subheader(config.SUBTITULO)

# --- Dados do evento ---
st.markdown(
    f"""
📅 **{config.EVENTO_DATA}**
🕐 **{config.EVENTO_HORA}**
📍 **{config.EVENTO_LOCAL}**
"""
)

# --- Convites (as duas imagens) ---
# Força as duas imagens a terem a MESMA altura, sem distorcer nem cortar
# (proporções diferentes ficam centralizadas dentro de uma caixa de altura fixa).
st.markdown(
    """
    <style>
    [data-testid="stImage"] img {
        height: 480px;
        object-fit: contain;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)
if os.path.exists(config.CONVITE_ALICE):
    col1.image(config.CONVITE_ALICE, caption="Alice 🍒", use_container_width=True)
if os.path.exists(config.CONVITE_HELENA):
    col2.image(config.CONVITE_HELENA, caption="Helena 🐝", use_container_width=True)

st.divider()
st.write("Preencha os campos abaixo para confirmar. Leva menos de um minuto 💙")

# --- Formulário ---
nome = st.text_input("Seu nome *", placeholder="Ex: Maria Silva")

grupo = st.selectbox("Você é convidado(a) de qual grupo? *", config.GRUPOS)
bebe = config.GRUPO_BEBE.get(grupo)
if bebe:
    st.caption(f"💛 Comemorando: **{bebe}**")

presenca = st.radio(
    "Vai comparecer? *",
    ["Sim, vou! 🎉", "Não vou conseguir 😢"],
    index=0,
)
vai = presenca.startswith("Sim")

if vai:
    num_pessoas = st.number_input(
        "Quantas pessoas no total (incluindo você)? *",
        min_value=1,
        max_value=20,
        value=1,
        step=1,
        help="Conte você + acompanhantes.",
    )
else:
    num_pessoas = 0

recado = st.text_area("Deixe um recado (opcional)", placeholder="Uma mensagem carinhosa...")

st.write("")  # espaçamento

if st.button("Confirmar ✅", type="primary", use_container_width=True):
    if not nome.strip():
        st.error("Por favor, preencha o seu nome.")
    else:
        presenca_valor = "Sim" if vai else "Não"
        try:
            with st.spinner("Salvando sua confirmação..."):
                registrar_confirmacao(
                    nome=nome.strip(),
                    grupo=grupo,
                    presenca=presenca_valor,
                    num_pessoas=num_pessoas,
                    recado=recado.strip(),
                )
            if vai:
                st.success(f"Presença confirmada, {nome.strip()}! Te esperamos lá 🎉")
                st.balloons()
            else:
                st.success("Recebido! Que pena que não vai dar, mas obrigado por avisar 💙")
        except Exception as e:
            st.error(
                "Ops, não consegui salvar agora. Tente de novo em instantes. "
                "Se persistir, avise o organizador."
            )
            st.caption(f"Detalhe técnico: {e}")
