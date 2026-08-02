"""Conexão com o Google Sheets (ler e gravar confirmações).

As credenciais da conta de serviço vêm de:
  - LOCAL: variáveis do arquivo .env (carregado com python-dotenv), ou
  - NUVEM: st.secrets (Streamlit Community Cloud).
Nunca ficam no código. Veja o README.md para o passo a passo.
"""

import os
from datetime import datetime

import gspread
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

import config

# Carrega o .env (se existir) para as variáveis de ambiente
load_dotenv()

# Escopos necessários para ler/escrever na planilha
_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Campos que compõem a conta de serviço do Google
_CAMPOS_SA = [
    "type",
    "project_id",
    "private_key_id",
    "private_key",
    "client_email",
    "client_id",
    "auth_uri",
    "token_uri",
    "auth_provider_x509_cert_url",
    "client_x509_cert_url",
    "universe_domain",
]


def _secret(*caminho):
    """Lê um valor de st.secrets sem quebrar se não existir arquivo de secrets."""
    try:
        valor = st.secrets
        for parte in caminho:
            valor = valor[parte]
        return valor
    except Exception:
        return None


def _service_account_info():
    """Monta o dicionário de credenciais a partir do st.secrets ou do .env."""
    # 1) Nuvem (Streamlit): tabela [gcp_service_account]
    secreto = _secret("gcp_service_account")
    if secreto:
        info = dict(secreto)
    else:
        # 2) Local: variáveis de ambiente (.env)
        info = {c: os.getenv(c) for c in _CAMPOS_SA if os.getenv(c) is not None}

    if not info.get("private_key"):
        raise RuntimeError(
            "Credenciais do Google não encontradas. Verifique o .env "
            "(local) ou os Secrets do Streamlit (nuvem)."
        )

    # Normaliza quebras de linha da chave privada (\\n -> \n)
    info["private_key"] = info["private_key"].replace("\\n", "\n")
    return info


def _sheet_id():
    return _secret("app", "sheet_id") or os.getenv("SHEET_ID") or config.SHEET_ID


def senha_organizador():
    """Senha do painel do organizador (secrets > .env > config)."""
    return (
        _secret("app", "organizador_senha")
        or os.getenv("ORGANIZADOR_SENHA")
        or config.ORGANIZADOR_SENHA
    )


@st.cache_resource(show_spinner=False)
def _get_worksheet():
    """Abre (e mantém em cache) a aba de confirmações da planilha."""
    creds = Credentials.from_service_account_info(_service_account_info(), scopes=_SCOPES)
    client = gspread.authorize(creds)
    planilha = client.open_by_key(_sheet_id())

    try:
        ws = planilha.worksheet(config.NOME_ABA)
    except gspread.WorksheetNotFound:
        ws = planilha.add_worksheet(title=config.NOME_ABA, rows=1000, cols=len(config.COLUNAS))

    # Garante o cabeçalho na primeira linha
    if ws.row_values(1) != config.COLUNAS:
        ws.update([config.COLUNAS], "A1")

    return ws


def _agora():
    """Data/hora atual no fuso de São Paulo (com fallback para hora local)."""
    try:
        from zoneinfo import ZoneInfo

        return datetime.now(ZoneInfo("America/Sao_Paulo"))
    except Exception:
        return datetime.now()


def registrar_confirmacao(nome, grupo, presenca, num_pessoas, recado):
    """Adiciona uma linha na planilha com a confirmação do convidado."""
    ws = _get_worksheet()
    ws.append_row(
        [
            _agora().strftime("%d/%m/%Y %H:%M"),
            nome,
            grupo,
            presenca,
            int(num_pessoas),
            recado,
        ],
        value_input_option="USER_ENTERED",
    )
    # Limpa o cache de leitura para o painel refletir a nova confirmação
    carregar_confirmacoes.clear()


@st.cache_data(ttl=60, show_spinner=False)
def carregar_confirmacoes():
    """Lê todas as confirmações da planilha e devolve um DataFrame."""
    ws = _get_worksheet()
    registros = ws.get_all_records()
    if not registros:
        return pd.DataFrame(columns=config.COLUNAS)
    df = pd.DataFrame(registros)
    if "num_pessoas" in df.columns:
        df["num_pessoas"] = pd.to_numeric(df["num_pessoas"], errors="coerce").fillna(0).astype(int)
    return df
