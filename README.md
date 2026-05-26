# 💳 Carteira Digital

Sistema WEB desenvolvido com Python, Flask e Supabase para gerenciamento de saldo, depósitos e transferências entre usuários.

## 📌 Descrição

A Carteira Digital é uma aplicação web que permite o cadastro de usuários, autenticação segura, gerenciamento de saldo e transferência de valores entre contas cadastradas.

O projeto foi desenvolvido utilizando Flask no back-end e Supabase como banco de dados, aplicando conceitos de desenvolvimento web, persistência de dados, rotas, templates e CRUD.

---

## 🚀 Funcionalidades

### Usuários
- Cadastro de usuários
- Login
- Logout
- Senhas criptografadas

### Financeiro
- Visualização de saldo
- Depósitos
- Transferências entre usuários
- Histórico de transações

### Segurança
- Senhas armazenadas com hash
- Validação de saldo
- Validação de usuários existentes
- Proteção contra transferências para a própria conta

---

## 🛠 Tecnologias Utilizadas

- Python 3
- Flask
- Supabase
- HTML5
- CSS3
- Bootstrap 5
- Jinja2

---

## 📁 Estrutura do Projeto

```text
mysite/
│
├── app.py
│
├── templates/
│   ├── login.html
│   ├── cadastro.html
│   ├── dashboard.html
│   └── recuperar.html
│
├── static/
│   └── css/
│       └── style.css
│
├── requirements.txt
├── README.md
│
└── venv/
```

---

## 🗄 Banco de Dados

### Tabela: usuarios

| Campo | Tipo |
|---------|---------|
| id | bigint |
| nome | text |
| email | text |
| senha | text |
| saldo | numeric(10,2) |

---

### Tabela: transacoes

| Campo | Tipo |
|---------|---------|
| id | bigint |
| remetente_id | bigint |
| destinatario_id | bigint |
| valor | numeric(10,2) |
| tipo | text |
| data | timestamp |

---

## ⚙ Instalação

### Clonar o projeto

```bash
git clone git@github.com:SEU_USUARIO/mysite.git

cd mysite
```

### Criar ambiente virtual

```bash
python3 -m venv venv
```

### Ativar ambiente virtual

Linux:

```bash
source venv/bin/activate
```

### Instalar dependências

```bash
pip install flask
pip install supabase
pip install werkzeug
```

---

## ▶ Executar

```bash
python app.py
```

A aplicação estará disponível em:

```text
http://localhost:5000
```

ou

```text
http://IP_DA_VM:5000
```

---

## 📖 Rotas

| Rota | Função |
|--------|--------|
| / | Dashboard |
| /login | Login |
| /cadastro | Cadastro |
| /deposito | Realizar depósito |
| /transferir | Realizar transferência |
| /logout | Encerrar sessão |
| /recuperar | Recuperação de senha |

---

## 🔮 Melhorias Futuras

- Recuperação de senha por e-mail
- Dashboard com gráficos
- Perfil de usuário
- Notificações
- Tema responsivo para dispositivos móveis
- Relatórios financeiros

---

## 👨‍💻 Desenvolvedores

Projeto acadêmico desenvolvido por:

- **Erick**
- **Jackson Douglas**

Tecnologias utilizadas:
- Python
- Flask
- Supabase
- HTML5
- CSS3
- Bootstrap 5

Desenvolvido como projeto da disciplina de Desenvolvimento WEB.