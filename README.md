# 🍼 Chá de Bebê — Confirmação de Presença (Alice & Helena)

App de confirmação de presença (RSVP) para o chá de bebê da **Alice** (Dayara &
Maurício) e da **Helena** (Dayane & Wesley), no mesmo dia e local. Feito em
**Streamlit** + **Google Sheets** — 100% gratuito, sem banco de dados pago.

- **Convidado** abre um link único, escolhe o grupo, diz se vai e quantas pessoas.
- **Organizador** entra num painel com senha e vê tudo (métricas, lista, CSV).

---

## 📁 O que tem no projeto

| Arquivo | Para que serve |
|---|---|
| `streamlit_app.py` | Tela do convidado (confirmação) |
| `pages/1_Organizador.py` | Painel do organizador (com senha) |
| `sheets.py` | Lê/grava no Google Sheets |
| `config.py` | Dados do evento, grupos e nomes das imagens |
| `assets/` | Onde ficam os convites (`convite_alice.png`, `convite_helena.png`) |
| `requirements.txt` | Dependências |
| `secrets.example.toml` | Modelo das credenciais |

---

## ✅ Passo a passo (o que VOCÊ precisa fazer)

### 1. Imagens dos convites
Salve os dois convites na pasta `assets/` com os nomes:
- `assets/convite_alice.png`
- `assets/convite_helena.png`

(Se forem `.jpg`, ajuste os nomes em `config.py`.)

### 2. Planilha no Google Sheets ✅ (já configurada)
O ID da planilha já está no `config.py` (`SHEET_ID`). Se um dia trocar de
planilha, é só atualizar esse valor.

### 3. Criar a conta de serviço do Google (grátis)
1. Acesse <https://console.cloud.google.com/> e crie um projeto.
2. Ative a **Google Sheets API**:
   *APIs e serviços → Biblioteca → procure "Google Sheets API" → Ativar*.
   (Ative também a **Google Drive API**.)
3. Vá em *APIs e serviços → Credenciais → Criar credenciais → Conta de serviço*.
4. Criada a conta, abra-a → aba **Chaves** → *Adicionar chave → Criar nova chave →
   JSON*. Vai baixar um arquivo `.json`. **Guarde-o com cuidado.**
5. Copie o e-mail da conta de serviço (algo como
   `nome@projeto.iam.gserviceaccount.com`).

### 4. Compartilhar a planilha com a conta de serviço
Na planilha, clique em **Compartilhar** e adicione o e-mail da conta de serviço
como **Editor**. (É isso que permite o app gravar as confirmações.)

### 5. Credenciais ✅ (já configuradas no `.env`)
As credenciais da conta de serviço já estão no arquivo `.env` (que **não** vai
para o GitHub — está no `.gitignore`). Testado e funcionando.

**Senha do organizador:** por padrão é `organizador123` (definida em `config.py`).
Para trocar sem mexer no código, adicione uma linha no `.env`:

```
ORGANIZADOR_SENHA=suanovasenha
```

---

## 💻 Rodar no seu computador (teste)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Abra o link que aparecer (geralmente <http://localhost:8501>). Faça uma
confirmação de teste e veja a linha aparecer na planilha. O painel fica no menu
lateral, em **Organizador** (pede a senha que você definiu).

---

## 🌐 Publicar de graça (gerar o link para o WhatsApp)

O deploy é feito pelo **Streamlit Community Cloud** a partir do GitHub —
**não precisa de GitHub Actions**.

1. Suba o projeto para um repositório no **GitHub** (o `secrets.toml` não sobe).
2. Acesse <https://share.streamlit.io> e faça login com o GitHub.
3. Clique em **New app**, escolha o repositório e o arquivo `streamlit_app.py`.
4. Em **Advanced settings → Secrets**, cole as credenciais em formato TOML
   (o `.env` **não** é lido na nuvem). Use o modelo `secrets.example.toml` como
   base — basta copiar cada valor do seu `.env` para o campo correspondente,
   dentro da tabela `[gcp_service_account]`, e preencher `[app]`.
5. Clique em **Deploy**. Em um minuto você recebe um **link público** — é esse
   link que você compartilha com os convidados. 🎉

O painel do organizador fica no mesmo link, na página **Organizador** (protegida
pela senha).

---

## 🔒 Segurança
- O arquivo com as credenciais (`secrets.toml`) **não** vai para o GitHub.
- O painel do organizador é protegido por senha.
- A lista é aberta: qualquer pessoa com o link confirma o próprio nome (é o
  esperado para um convite compartilhado no WhatsApp).
