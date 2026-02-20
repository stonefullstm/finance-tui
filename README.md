# 💰 TUI Finance

Um gerenciador de finanças pessoais com interface textual (TUI) construído em Python usando o framework **Textual** e banco de dados **Firebird**.

<p align="center">
<img src="https://img.shields.io/badge/STATUS-EM DESENVOLVIMENTO-blue"/>
</p>

## 📋 Características

- 🎯 **Interface TUI Intuitiva** - Aplicação de terminal moderna e responsiva
- 💳 **Gerenciamento de Transações** - Adicionar, editar e deletar transações
- 📂 **Categorização de Despesas** - Organizar transações por categorias personalizadas
- 📊 **Visualização de Dados** - Gráficos de despesas por mês e por categoria
- 💾 **Banco de Dados Firebird** - Persistência robusta de dados
- ✅ **Testes Automatizados** - Cobertura com pytest
- 🎨 **Interface Customizável** - Estilos TCSS (Textual CSS)

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.8+
- Firebird 3.0+
- pip ou pipenv

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/tui-finance.git
   cd tui-finance
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados Firebird:**
   
   Edite o arquivo [db/config.py](db/config.py) com as credenciais do seu Firebird:
   ```python
   DATABASE_URL = "firebird+firebird://usuario:senha@localhost:3050/caminho/banco.fdb"
   ```

5. **Execute a aplicação:**
   ```bash
   python -m finance
   ```

## 📚 Estrutura do Projeto

```
tui-finance/
├── finance/              # Módulo principal da aplicação TUI
│   ├── tui.py           # Aplicação principal (FinanceApp)
│   ├── dashboard.py     # Dashboard com gráficos
│   ├── transaction_dialog.py  # Diálogo de transações
│   ├── category_dialog.py     # Diálogo de categorias
│   ├── question_dialog.py     # Diálogo de confirmação
│   └── *.tcss           # Estilos Textual CSS
├── dao/                 # Data Access Objects (DAOs)
│   ├── transaction_dao.py
│   └── category_dao.py
├── models/              # Modelos SQLAlchemy
│   └── models.py        # Category e Transaction
├── db/                  # Configuração do banco de dados
│   └── config.py        # Conexão com Firebird
├── tests/               # Testes automatizados
│   ├── test_category_dao.py
│   └── conftest.py
├── requirements.txt     # Dependências
└── pytest.ini           # Configuração pytest
```

## 🎮 Como Usar

<img src="images/main-screen.png" alt="main screen"/>

### Navegação Básica

| Tecla | Ação |
|-------|------|
| `a` | Adicionar transação |
| `e` | Editar transação selecionada |
| `d` | Deletar transação selecionada |
| `c` | Limpar todas as transações |
| `m` | Alternar tema escuro/claro |
| `q` | Sair |

### Operações Principais

1. **Adicionar Transação:**
   - Pressione `a` ou clique em "Add"
   - Preencha: descrição, data, valor, tipo (Receita/Despesa) e categoria. Se precisar, clique no botão "+" para criar uma nova categoria

2. **Visualizar Categorias:**
   - Veja a lista de categorias no painel direito
   - Duplo clique em uma categoria para filtrar e visualizar o gráfico

3. **Consultar Gráficos:**
   - Gráfico de despesas por mês
   - Gráfico de despesas por categoria

## 🔧 Desenvolvimento

### Instalar Dependências de Desenvolvimento

```bash
pip install -r requirements-dev.txt
```

### Executar Testes

```bash
pytest                  # Executar todos os testes
pytest -v              # Modo verboso
pytest --cov           # Com cobertura
```

### Formatação de Código

```bash
black .                # Formatar com Black
flake8 .              # Verificar estilo
isort .               # Organizar imports
```

## 📦 Dependências Principais

- **textual** - Framework TUI para Python
- **textual-plot** - Gráficos no terminal
- **sqlalchemy** - ORM e query builder
- **firebird-driver** - Driver para Firebird
- **pytest** - Framework de testes

## 📝 Logging

A aplicação registra atividades em `app.log`. Configure o nível de logging em [finance/tui.py](finance/tui.py):

```python
logging.basicConfig(level=logging.INFO)  # DEBUG, INFO, WARNING, ERROR
```

## 👤 Autor

Carlos Araújo - [GitHub](https://github.com/stonefullstm)
