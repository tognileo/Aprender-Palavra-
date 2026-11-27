# Aprender Palavras

Site para aprender, em pouco tempo, as principais expressões em inglês americano
para quem precisa viajar com urgência. Projeto do curso Jovem Programador.

Foi feito para telas de computador (referência: 1440x900).

## O que o site faz

- **Cadastro e login.** No cadastro, a pessoa escolhe o motivo da viagem
  (Férias ou Atleta em competição no exterior). Essa escolha não pode ser trocada.
- **Estudo.** Começa no grupo Básico. As setas trocam de grupo. Cada expressão
  mostra o inglês, a pronúncia escrita em português e a tradução. A pessoa separa
  as expressões entre "Para estudar" e "Já memorizadas".
- **Minigames.** A pessoa escolhe o grupo e a direção (inglês para português ou
  português para inglês) e responde perguntas de alternativas. O jogo continua até
  ela sair, usa todas as expressões do grupo e não muda as abas do estudo.

São 400 expressões: 50 do grupo Básico, 150 de Férias e 200 de Atleta.

## Tecnologias

- **Backend:** Python, FastAPI, Uvicorn, SQLAlchemy, PyMySQL e Pydantic
- **Segurança:** senhas com Argon2 (pwdlib) e login com JWT (PyJWT)
- **Configuração:** python-dotenv
- **Banco de dados:** MariaDB no Alwaysdata
- **Frontend:** HTML, CSS e JavaScript puros

## Estrutura

- `banco/`: `criar_tabelas.sql`, `expressoes.csv` e `importar_expressoes.py`
- `backend/`: API em FastAPI (modelos, controladores, rotas, esquemas)
- `frontend/`: telas em HTML, CSS e JavaScript
- `Modelos do projeto/`: documentos, fluxograma e telas de referência

## Como rodar (Windows, PowerShell)

Rode todos os comandos na pasta raiz do projeto (a que tem este `README.md`).
Os comandos usam o Python da `venv` direto, então não é preciso ativá-la.

### 1. Preparar o ambiente (uma vez em cada computador)

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
```

Abra o arquivo `.env` e preencha com os dados do banco. Para criar o `JWT_SECRET`:

```powershell
.\venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

**Nunca envie o `.env` para o GitHub.**

Teste a conexão:

```powershell
.\venv\Scripts\python.exe -m backend.banco_de_dados
```

### 2. Preparar o banco (somente se o banco estiver vazio)

1. Rode o arquivo `banco/criar_tabelas.sql` no banco, uma única vez.
2. Importe as expressões:

```powershell
.\venv\Scripts\python.exe -m banco.importar_expressoes
```

A importação pode ser repetida: expressões que já existem são puladas
(o texto delas não é atualizado).

### 3. Ligar o site (dois terminais)

Terminal 1, a API:

```powershell
.\venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

Terminal 2, as telas:

```powershell
.\venv\Scripts\python.exe -m http.server 5500 --bind 127.0.0.1 --directory frontend
```

Abra no navegador: http://127.0.0.1:5500/login.html

No lugar do terminal 2, também dá para usar o Live Server ("Go Live") do VS Code,
desde que ele use a porta 5500. Não abra os arquivos HTML com dois cliques:
a API bloqueia o acesso.

Para desligar, aperte `Ctrl+C` em cada terminal.

A documentação da API fica em http://127.0.0.1:8000/docs

## Problemas comuns

- **"No module named 'backend'":** o terminal não está na pasta raiz do projeto.
- **"Falta a configuração ... no arquivo .env":** confira o `.env` e salve o arquivo.
- **"Não foi possível conectar ao servidor":** a API (terminal 1) está desligada.
- **A tela não mudou depois de uma alteração:** salve o arquivo e aperte `Ctrl+F5`.
- **Pediu login de novo:** o login expira no tempo definido em `JWT_EXPIRE_MINUTES`
  (padrão: 15 minutos).

## Ainda não feito

- Publicação no Alwaysdata
- Áudio das expressões
