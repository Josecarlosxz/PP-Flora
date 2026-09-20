# Blueprint do Projeto (Flask + SQLAlchemy)

## Visão Geral
Este projeto é uma API Flask com:
- **Factory App** (`main.py`) para criar e configurar a instância do Flask.
- **BluePrints** separados por recurso dentro de `backend/controllers/`.
- **Modelos SQLAlchemy (ORM)** em `backend/models/` com relacionamentos e **herança polimórfica**.

O objetivo deste documento é registrar “todo o projeto em blueprint”: estrutura, componentes e prefixos/rotas principais.

---

## Entrypoint / Factory
**Arquivo:** `main.py`

- Função: `create_app()`
- Cria `app = Flask(__name__)`
- Registra todos os blueprints:
  - `usuario_bp`
  - `especie_bp`
  - `animal_bp`
  - `planta_bp`
  - `bioma_bp`
  - `especie_bioma_bp`
  - `token_bp`
  - `participante_bp`

Portanto a API fica centralizada no factory e as rotas pertencem aos blueprints.

---

## Camada de Controllers (BluePrints)
Pasta: `backend/controllers/`

### 1) Usuários
**Arquivo:** `backend/controllers/usuario_controller.py`
- Blueprint: `usuario_bp`
- Prefixo: **`/usuarios`**
- Rotas:
  - `POST /usuarios/`
  - `GET /usuarios/`
  - `GET /usuarios/<id>`
  - `PUT /usuarios/<id>`
  - `DELETE /usuarios/<id>`

### 2) Espécies (base + CRUD polimórfico)
**Arquivo:** `backend/controllers/especie_controller.py`
- Blueprint: `especie_bp`
- Prefixo: **`/especies`**
- Rotas:
  - `POST /especies/`
  - `GET /especies/`
  - `GET /especies/<id>`
  - `PUT /especies/<id>`
  - `DELETE /especies/<id>`

Observação: o modelo `Especie` usa herança polimórfica via `tipo`.

### 3) Animais
**Arquivo:** `backend/controllers/animal_controller.py`
- Blueprint: `animal_bp`
- Prefixo: **`/animais`**
- Rotas:
  - `POST /animais/`
  - `GET /animais/`
  - `GET /animais/<id>`
  - `PUT /animais/<id>`
  - `DELETE /animais/<id>`

### 4) Plantas
**Arquivo:** `backend/controllers/planta_controller.py`
- Blueprint: `planta_bp`
- Prefixo: **`/plantas`**
- Rotas:
  - `POST /plantas/`
  - `GET /plantas/`
  - `GET /plantas/<id>`
  - `PUT /plantas/<id>`
  - `DELETE /plantas/<id>`

### 5) Biómas
**Arquivo:** `backend/controllers/bioma_controller.py`
- Blueprint: `bioma_bp`
- Prefixo: **`/biomas`**
- Rotas:
  - `POST /biomas/`
  - `GET /biomas/`
  - `GET /biomas/<id>`
  - `PUT /biomas/<id>`
  - `DELETE /biomas/<id>`

### 6) Relação Espécie-Bióma (tabela intermediária)
**Arquivo:** `backend/controllers/especie_bioma_controller.py`
- Blueprint: `especie_bioma_bp`
- Prefixo: **`/especie-bioma`**
- Rotas:
  - `POST /especie-bioma/`
  - `GET /especie-bioma/`
  - `GET /especie-bioma/<id>`
  - `PUT /especie-bioma/<id>`
  - `DELETE /especie-bioma/<id>`

### 7) Tokens
**Arquivo:** `backend/controllers/token_controller.py`
- Blueprint: `token_bp`
- Prefixo: **`/tokens`**
- Rotas:
  - `POST /tokens/`
  - `GET /tokens/`
  - `GET /tokens/<id>`
  - `PUT /tokens/<id>`
  - `DELETE /tokens/<id>`

### 8) Participantes
**Arquivo:** `backend/controllers/participante_controller.py`
- Blueprint: `participante_bp`
- Prefixo: **`/participantes`**
- Rotas:
  - `POST /participantes/`
  - `GET /participantes/`
  - `GET /participantes/<id>`
  - `PUT /participantes/<id>`
  - `DELETE /participantes/<id>`

---

## Camada de Dados (Models SQLAlchemy)
Pasta: `backend/models/`

### `backend/database.py`
- Configura engine SQLite: **`sqlite:///meubanco.db`**
- Define:
  - `Base = declarative_base()`
  - `SessionLocal = sessionmaker(...)`

---

## Models principais

### `Usuario`
- Tabela: `usuarios`
- Campos: `id`, `nome`, `email (unique)`, `senha`
- Relacionamentos:
  - `especies`
  - `tokens`

### `Especie` (base polimórfica)
- Tabela: `especies`
- Campos: `id`, `nome_popular`, `nome_cientifico`, `descricao`, `tipo`, `usuario_id`
- Polimorfismo:
  - `polymorphic_on = tipo`
  - `polymorphic_identity = "especie"`
- Relacionamentos:
  - `usuario`
  - `biomas` via `EspecieBioma`

### `Animal` (herda `Especie`)
- Tabela: `animais`
- Chave: `id` FK para `especies.id`
- Campos: `dieta`, `habitat_especifico`
- Discriminator: `polymorphic_identity = "animal"`

### `Planta` (herda `Especie`)
- Tabela: `plantas`
- Chave: `id` FK para `especies.id`
- Campos: `tipo_folha`, `medicinal`
- Discriminator: `polymorphic_identity = "planta"`

### `Bioma`
- Tabela: `biomas`
- Campos: `id`, `nome`, `descricao`, `clima`, `vegetacao`
- Relacionamento: `especies` via `EspecieBioma`

### `EspecieBioma` (tabela intermediária)
- Tabela: `especie_bioma`
- Campos: `id`, `especie_id`, `bioma_id`

### `Token`
- Tabela: `tokens`
- Campos: `id`, `codigo (unique)`, `ativo`, `expira_em`, `usuario_id`
- Relacionamento:
  - `usuario`
  - `participantes`

### `Participante`
- Tabela: `participantes`
- Campos: `id`, `nome`, `token_id`
- Relacionamento: `token`

---

## Testes
Pasta: `tests/`
- A suite usa `pytest` + `create_app()`.
- Em `tests/conftest.py`:
  - cria as tabelas antes dos testes
  - remove as tabelas ao final

---

## Fluxo típico de uma rota (padrão usado nos controllers)
1. Recebe JSON via `request.get_json()`
2. Abre sessão: `db = SessionLocal()`
3. Cria ou busca model (`db.query(...).filter(...).first()` ou `Model(...)`)
4. `db.add(...)` / `db.commit()` / `db.refresh(...)`
5. `db.close()`
6. Retorna `jsonify(response)` (com status 200 ou 404 quando não encontrado)

