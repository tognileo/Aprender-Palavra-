# Aprender Palavras

Site para aprender, em pouco tempo, as principais expressões em inglês americano
para quem precisa viajar com urgência. Projeto do curso Jovem Programador.

## Estrutura

- `banco/`: scripts SQL, CSV das expressões e (em breve) o script de importação
- `backend/`: API em FastAPI (models, controllers, routes, schemas)
- `frontend/`: telas em HTML, CSS e JavaScript
- `docs/`: documentação do projeto e telas de referência

## Como rodar

1. Copie `.env.example` para `.env` e preencha com os dados reais do banco.
2. Crie o ambiente Python: `python -m venv venv`
3. Ative: `venv\Scripts\Activate.ps1`
4. Instale as bibliotecas (o `requirements.txt` será gerado na etapa do ambiente).
