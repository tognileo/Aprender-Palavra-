# Aprender Palavras

Site para aprender, em pouco tempo, as principais expressões em inglês americano
para quem precisa viajar com urgência. Projeto do curso Jovem Programador.

## Estrutura

- `banco/`: criar_tabelas.sql, expressoes.csv e importar_expressoes.py
- `backend/`: API em FastAPI (modelos, controladores, rotas, esquemas)
- `frontend/`: telas em HTML, CSS e JavaScript
- `Modelos do projeto/`: documentação, fluxograma, esquema do banco e telas de referência

## Como rodar

1. Copie `.env.example` para `.env` e preencha com os dados reais do banco.
2. Crie o ambiente Python: `python -m venv venv`
3. Ative: `venv\Scripts\Activate.ps1`
4. Instale as bibliotecas: `pip install -r requirements.txt`
5. Crie as tabelas rodando `banco/criar_tabelas.sql` no banco.
6. Importe as expressões: `python -m banco.importar_expressoes` (pode rodar de novo: o que já existe é pulado)
7. Inicie o servidor: `uvicorn backend.main:app --reload`
8. Teste a API em http://127.0.0.1:8000/docs


## Se aparecer "ModuleNotFoundError: No module named 'backend'"

Rode os comandos sempre na pasta raiz do projeto (a que tem `backend/`, `banco/` e `README.md`).
Nesta versão, o projeto também acha a raiz sozinho, mesmo com o botão Play do VS Code.
Teste da conexão com o banco: `python -m backend.banco_de_dados`
