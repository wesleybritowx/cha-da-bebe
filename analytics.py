"""Injeta o Google Analytics (gtag.js) no <head> do index.html do Streamlit.

O Streamlit remove <script> de dentro do st.markdown, então a forma
confiável de adicionar a tag é editar o index.html servido pelo próprio
Streamlit no início da execução. É idempotente (não duplica a tag) e roda
tanto localmente quanto no Streamlit Cloud.
"""

import pathlib

import streamlit as st

GA_ID = "G-TP3CS1SY3X"

_GA_SNIPPET = f"""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_ID}');
</script>
"""


def injetar_ga():
    """Insere a tag do Google Analytics no index.html (uma única vez)."""
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    try:
        html = index_path.read_text(encoding="utf-8")
    except Exception:
        return  # em ambientes onde não há permissão de leitura, apenas ignora

    if GA_ID in html:
        return  # já injetado

    novo_html = html.replace("<head>", "<head>" + _GA_SNIPPET, 1)
    try:
        index_path.write_text(novo_html, encoding="utf-8")
    except Exception:
        pass  # sem permissão de escrita: segue sem analytics, sem quebrar o app
