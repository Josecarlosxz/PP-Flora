# PP — BioSistema

Sistema web desenvolvido para consulta e apresentação de informações sobre a biodiversidade brasileira.

O projeto possui um backend desenvolvido em **Python/Flask**, integração com **MySQL** e um frontend composto por **HTML, CSS e JavaScript**.

---

## 📋 Sobre o projeto

O **PP — BioSistema** tem como objetivo disponibilizar informações organizadas sobre a biodiversidade brasileira de forma simples e acessível.

O sistema permite:

- Visualização de informações sobre biodiversidade;
- Consulta de informações detalhadas;
- Navegação entre diferentes regiões;
- Visualização de informações relacionadas aos biomas;
- Cadastro e autenticação de usuários;
- Acesso a páginas de detalhes;
- Interface web responsiva;
- Integração com banco de dados MySQL.

---

## 🛠️ Tecnologias utilizadas

### Backend

- Python
- Flask
- python-dotenv
- MySQL Connector

### Frontend

- HTML5
- CSS3
- JavaScript

### Banco de dados

- MySQL
- XAMPP

### Ferramentas

- Git
- GitHub
- Visual Studio Code

---

## 📁 Estrutura do projeto

```text
PP/
│
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   ├── base.css
│   │   │   ├── login.css
│   │   │   ├── detalhe.css
│   │   │   └── mapa.css
│   │   │
│   │   ├── js/
│   │   └── images/
│   │
│   └── templates/
│       ├── base.html
│       ├── home.html
│       ├── login.html
│       ├── usuario.html
│       └── detalhe.html
│
├── backend/
│   └── ...
│
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

### 1. Abra um terminal:
- PowerShell ou CMD


### 2. Navegue até a pasta do backend:

```bash
cd d:\Users\COMPUTER\Documents\PP\backend
```

### 3. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 4. Instalar dependências
No diretório do backend, execute:

```bash
pip install -r requirements.txt
```
Caso ainda não exista um requirements.txt, instale as principais dependências:

```bash
pip install flask python-dotenv mysql-connector-python
```

### 5. Configurar o arquivo .env:
Na raiz do projeto, crie um arquivo chamado:
.env

```bash
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=pp SECRET_KEY=sua_chave_secreta
```
Se o seu MySQL possuir senha, informe-a em:

DB_PASSWORD=sua_senha

Não publique o arquivo .env no GitHub.

O .gitignore deve conter:

```bash
.venv/
__pycache__/
.env
*.pyc
```

### 6. Inicie o MySQL:
Abra o XAMPP e inicie:

```bash
Apache
MySQL
```
O MySQL deve estar funcionando na porta: 3306

### 7. Executar o projeto:

```bash
python main.py
```
Você verá um aviso dizendo que o servidor está rodando em http://127.0.0.1:5000.

## Como rodar o frontend

### 1. Abra outro terminal
- PowerShell ou CMD


### 2. Navegue até a pasta do frontend:

```bash
cd d:\Users\COMPUTER\Documents\PP\frontend
```

### 3. Vamos usar o Python para servir os arquivos HTML (simular um servidor web simples):

```bash
python -m http.server 8000
```
Isso iniciará um servidor para o frontend na porta 8000

### Acessar
 - 1. Abra seu navegador (Chrome, Edge, Firefox).
 - 2. Acesse: http://localhost:8000

## Execução rápida:
Terminal 1 — Backend
```bash
cd d:\Users\COMPUTER\Documents\PP
.venv\Scripts\activate
python main.py
```

Terminal 2 — Frontend
```bash
cd d:\Users\COMPUTER\Documents\PP\frontend
python -m http.server 8000
```

