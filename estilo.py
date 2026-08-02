"""Estilo visual compartilhado do app (gradiente rosa → amarelo)."""

import streamlit as st


def aplicar_estilo():
    """Aplica o fundo em gradiente e ajustes de leitura em todas as páginas."""
    st.markdown(
        """
        <style>
        /* Fundo em gradiente: rosa (Alice) -> amarelo (Helena) */
        .stApp {
            background: linear-gradient(135deg, #ffc6dd 0%, #ffe9f2 45%, #fff3c9 100%);
            background-attachment: fixed;
        }
        [data-testid="stAppViewContainer"] { background: transparent; }
        [data-testid="stHeader"] { background: transparent; }

        /* Sidebar levemente translúcida para combinar com o fundo */
        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.45);
            backdrop-filter: blur(2px);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
