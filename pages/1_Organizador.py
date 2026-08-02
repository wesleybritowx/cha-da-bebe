"""Painel do organizador — protegido por senha.

Mostra todas as confirmações, filtros, métricas e download em CSV.
"""

import streamlit as st

import config
from estilo import aplicar_estilo
from sheets import carregar_confirmacoes, senha_organizador

st.set_page_config(page_title="Organizador", page_icon="📋")
aplicar_estilo()

st.title("📋 Painel do Organizador")


# --- Proteção por senha ---
def _checar_senha():
    senha_correta = senha_organizador()
    if st.session_state.get("_autenticado"):
        return True

    senha = st.text_input("Senha do organizador", type="password")
    if not senha:
        st.info("Digite a senha para acessar o painel.")
        return False
    if senha == senha_correta:
        st.session_state["_autenticado"] = True
        return True
    st.error("Senha incorreta.")
    return False


if not _checar_senha():
    st.stop()

# --- Dados ---
col_atualizar, _ = st.columns([1, 3])
if col_atualizar.button("🔄 Atualizar dados"):
    carregar_confirmacoes.clear()

df = carregar_confirmacoes()

if df.empty:
    st.warning("Ainda não há confirmações.")
    st.stop()

# --- Filtro por grupo ---
grupos_opcoes = ["Todos"] + config.GRUPOS
filtro_grupo = st.selectbox("Filtrar por grupo", grupos_opcoes)

df_view = df if filtro_grupo == "Todos" else df[df["grupo"] == filtro_grupo]

# --- Métricas ---
confirmados = df_view[df_view["presenca"] == "Sim"]
nao_vao = df_view[df_view["presenca"] == "Não"]

c1, c2, c3 = st.columns(3)
c1.metric("Confirmaram presença", len(confirmados))
c2.metric("Total de pessoas", int(confirmados["num_pessoas"].sum()))
c3.metric("Não vão", len(nao_vao))

# Pessoas por grupo (sempre considerando todos os grupos, só entre quem vai)
st.subheader("Pessoas por grupo")
por_grupo = (
    df[df["presenca"] == "Sim"]
    .groupby("grupo")["num_pessoas"]
    .sum()
    .reindex(config.GRUPOS, fill_value=0)
    .astype(int)
)
st.bar_chart(por_grupo)

# --- Tabela ---
st.subheader("Lista de confirmações")
st.dataframe(df_view, use_container_width=True, hide_index=True)

# --- Download CSV ---
csv = df.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "⬇️ Baixar CSV (todos os grupos)",
    data=csv,
    file_name="confirmacoes_cha_de_bebe.csv",
    mime="text/csv",
)
