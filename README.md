
## Como rodar o Backend

### 1. Abra um terminal
- PowerShell ou CMD


### 2. Navegue até a pasta do backend:

```bash
cd d:\Users\COMPUTER\Documents\PP
```

### 3. (Opcional, mas recomendado) Crie e ative um ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 4. Instalar dependências
No diretório do backend, execute:

```bash
pip install flask flask-cors
```

### 5.Inicie o servidor Flask:
```bash
python main.py
```
Você verá um aviso dizendo que o servidor está rodando em http://127.0.0.1:5000.

## Como rodar o frontend

### 1. Abra outro terminal
- PowerShell ou CMD


### 2. Navegue até a pasta do frontend:

```bash
cd d:\Users\COMPUTER\Documents\PP\\frontend
```

### 3. Vamos usar o Python para servir os arquivos HTML (simular um servidor web simples):

```bash
python -m http.server 8000
```
Isso iniciará um servidor para o frontend na porta 8000

### Acessar
 - 1. Abra seu navegador (Chrome, Edge, Firefox).
 - 2. Acesse: http://localhost:8000
