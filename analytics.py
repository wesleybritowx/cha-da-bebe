"""Injeta o Google Analytics (gtag.js) no app Streamlit.

Em vez de editar o index.html (que pode ser somente-leitura no Streamlit
Cloud), a tag é inserida no <head> da página pelo lado do navegador, a partir
de um componente. Funciona em toda visita e não depende de permissão de
escrita no servidor. É idempotente (não duplica a tag).
"""

import streamlit as st
import streamlit.components.v1 as components

GA_ID = "G-TP3CS1SY3X"


def injetar_ga():
    components.html(
        f"""
        <script>
        (function() {{
            var doc = window.parent.document;
            if (doc.getElementById('ga-gtag-js')) return;  // já injetado

            var s = doc.createElement('script');
            s.id = 'ga-gtag-js';
            s.async = true;
            s.src = 'https://www.googletagmanager.com/gtag/js?id={GA_ID}';
            doc.head.appendChild(s);

            var s2 = doc.createElement('script');
            s2.id = 'ga-gtag-init';
            s2.text = "window.dataLayer = window.dataLayer || [];"
                    + "function gtag(){{dataLayer.push(arguments);}}"
                    + "gtag('js', new Date());"
                    + "gtag('config', '{GA_ID}');";
            doc.head.appendChild(s2);
        }})();
        </script>
        """,
        height=0,
        width=0,
    )
