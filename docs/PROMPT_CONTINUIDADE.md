# PROMPT DE CONTINUIDADE: APLICAÇÃO "APRENDER PALAVRAS"

Você vai continuar o desenvolvimento de uma aplicação web chamada **Aprender Palavras**. Este documento resume tudo o que foi definido e feito até agora, com o máximo de detalhe, para que você assuma o trabalho sem precisar refazer perguntas já respondidas. Leia tudo antes de responder.

Data deste resumo: 19/11/2026.

---

## 0. Como você deve trabalhar com esta pessoa (leia primeiro)

- A pessoa que desenvolve é **iniciante em programação**. Responda sempre em **português do Brasil**, com linguagem simples, explicando **arquivo por arquivo** e dizendo o que cada parte faz e por quê.
- **Faça uma pergunta de cada vez** (de preferência uma só dúvida por mensagem) antes de decidir qualquer coisa que não esteja definida aqui.
- **Não invente funcionalidades.** Não altere as regras de funcionamento descritas abaixo.
- **Não adicione tecnologias** além das listadas na seção 5. Não troque tecnologias nem design sem autorização explícita.
- Vá devagar: uma etapa por vez, e só avance quando a anterior estiver entendida e funcionando.
- Quando entregar código, diga em que pasta o arquivo fica e como testar.
- Nunca coloque senhas, chaves ou o arquivo `.env` no GitHub.

---

## 1. O que é a aplicação

O Aprender Palavras é uma plataforma para ensinar **expressões em inglês americano** (destino: EUA) a pessoas que precisam **viajar para o exterior com urgência** e têm pouco ou nenhum conhecimento do idioma.

Existem **dois nichos** (públicos):

- **Férias:** 150 expressões exclusivas.
- **Atleta em competição:** 200 expressões exclusivas.

Além disso existe um **grupo Básico, compartilhado pelos dois nichos**, com **50 expressões**.

**Total: 400 expressões.**

Cada expressão tem três campos:
1. Inglês.
2. Tradução em português.
3. Pronúncia aproximada em português brasileiro.

O **sistema de áudio** só será feito no futuro, se houver tempo. **Não faz parte do escopo obrigatório.** Não o inclua.

### Detalhes do nicho Atleta (decididos em conversas anteriores)
- O destino continua sendo os EUA (inglês americano).
- O conteúdo é genérico, para qualquer esporte (não é para um esporte específico).
- O nicho ensina a **responder perguntas de repórteres** e **como falar ao ganhar ou perder**.
- Mistura as **perguntas dos repórteres** (para a pessoa entender) com as **respostas** (para a pessoa falar).
- Lista de grupos sugerida e aprovada: apresentação, carreira, preparação, antes da competição, se ganhar, se perder, agradecimentos, perguntas difíceis, final da coletiva.
- O grupo Básico e o nicho Férias continuam como no resto do projeto. (A lista de grupos do nicho Férias ainda não foi definida neste resumo; pergunte à pessoa quando chegar a hora de montar o CSV.)

---

## 2. Regras de funcionamento (não alterar)

### 2.1 Cadastro e autenticação
- **Cadastro** com: nome, e-mail, senha e escolha de **um nicho** (Férias ou Atleta).
- O **e-mail deve ser único**.
- A **senha deve ser guardada protegida** (hash Argon2, nunca a senha pura).
- Depois do cadastro, o usuário faz **login com e-mail e senha**.
- A autenticação é feita por **JWT**.
- Existe a opção de **sair da conta** (logout).

### 2.2 Tela principal de estudos
- Depois de entrar, o usuário vai para a **área de estudos**.
- Existem dois tipos de grupo: o **Básico** e os **grupos específicos do nicho escolhido**.
- A tela de estudos **sempre começa pelo grupo Básico**.
- O usuário navega entre os grupos com **setas**: seta para a direita = próximo grupo; seta para a esquerda = grupo anterior.
- **As setas ficam desativadas** quando não existe outro grupo naquela direção.

### 2.3 Abas de organização das expressões
Na área de estudos existem duas abas:
- **Para estudar:** mostra as expressões que ainda **não** foram marcadas como memorizadas.
- **Já memorizadas:** mostra as expressões que o usuário marcou **manualmente** como memorizadas.

O usuário pode **mover expressões entre as duas abas**, e **essa alteração é salva no banco de dados**.

### 2.4 Dicionário
- Área que disponibiliza **todas as expressões do nicho escolhido pelo usuário, incluindo o grupo Básico**.
- O usuário pode **pesquisar** expressões e consultar as traduções.

### 2.5 Minigames
- O usuário escolhe: (1) o **grupo** de expressões; (2) a **direção** do exercício: inglês para português **ou** português para inglês.
- O sistema mostra uma expressão e **alternativas de tradução**.
- Quando o usuário escolhe uma alternativa:
  - se estiver **correta**, o sistema informa que acertou;
  - se estiver **errada**, o sistema informa o erro e **mostra a tradução correta**.
- Os minigames usam **todas as expressões do grupo selecionado**, estejam elas em "Para estudar" ou em "Já memorizadas".
- Os minigames **não alteram** o estado de memorização das expressões.

---

## 3. Fluxograma (já pronto)

O fluxograma completo foi criado (em um canvas visual, com formas padrão: retângulo = processo, losango = decisão, cores por área: azul = acesso e sessão, verde = estudos, âmbar = dicionário, roxo = minigames, cinza = banco de dados, escuro = início, fim e retorno). Como você não consegue ver o desenho, aqui vai o conteúdo dele em texto. A pessoa deve guardar a imagem/arquivo do fluxograma na pasta `docs/` do repositório.

**Acesso e autenticação**
1. Início: "Usuário acessa o site".
2. Decisão: **"Possui conta?"**
   - **Não** → "Preenche o cadastro: nome, e-mail, senha e nicho (Férias ou Atleta)" → decisão **"Dados válidos e e-mail único?"**
     - **Não** → volta ao formulário de cadastro para corrigir os dados.
     - **Sim** → "Salva o usuário no banco (tabela `usuarios`) com a senha protegida por Argon2" → "Cadastro concluído: o usuário faz login" (segue para a tela de login).
   - **Sim** → "Informa e-mail e senha do login" → decisão **"Credenciais válidas?"**
     - **Não** → volta ao login para tentar novamente.
     - **Sim** → "Gera o token JWT e libera a área principal".
3. "Identifica o nicho escolhido (Férias ou Atleta)".
4. Decisão central (menu): **"Qual funcionalidade o usuário escolhe?"** com quatro saídas: Estudos (tela inicial), Dicionário, Minigames e Sair. Ao fim de cada funcionalidade existe um conector "A" que **volta a esse menu**.

**Estudos**
1. "Abre a área de estudos no grupo Básico".
2. Decisão **"Usuário clica em uma seta de grupo?"**
   - **Sim** → decisão **"Existe grupo na direção da seta?"**: **Sim** → "Exibe o grupo anterior ou o próximo"; **Não** → "Seta desativada: o grupo não muda". Os dois caminhos voltam para o passo 3.
   - **Não** → vai direto ao passo 3.
3. "Exibe as abas Para estudar e Já memorizadas".
4. Decisão **"Mover expressão para a outra aba?"**
   - **Sim** → "Move a expressão entre as abas Para estudar e Já memorizadas" → "Salva a alteração no banco de dados (tabela `memorizadas`)" → volta ao menu.
   - **Não** → volta ao menu.

**Dicionário**
1. "Abre o dicionário com todas as expressões do nicho, incluindo o grupo Básico".
2. "Usuário pesquisa uma expressão".
3. "Mostra as expressões encontradas e suas traduções".
4. Volta ao menu.

**Minigames**
1. "Escolhe o grupo de expressões: Básico ou um grupo do nicho".
2. "Escolhe a direção do exercício: inglês para português ou português para inglês".
3. "Mostra uma expressão e alternativas de tradução".
4. Decisão **"A alternativa escolhida está correta?"**: **Sim** → "Informa que acertou"; **Não** → "Informa o erro e mostra a tradução correta".
5. Decisão **"Continuar praticando?"**: **Sim** → volta ao passo 3 (nova expressão); **Não** → volta ao menu.
6. Nota do fluxograma: usa todas as expressões do grupo, memorizadas ou não, e não altera o estado de memorização.

**Sessão (logout)**
"Usuário clica em Sair" → "Encerra a sessão do usuário" → "Fim da sessão".

**Preparação dos dados (antes do primeiro acesso)**
"Arquivo CSV com as 400 expressões (inglês, tradução e pronúncia)" → "Script Python importa o CSV para o banco" → "Banco MySQL com cinco tabelas".

---

## 4. Banco de dados

O banco terá **exatamente cinco tabelas**: `nichos`, `grupos`, `expressoes`, `usuarios`, `memorizadas`.

O script `schema.sql` já foi criado (cole o arquivo na pasta `banco/` do projeto). Ele ainda **não foi testado** em um MySQL real; o primeiro passo é rodá-lo e conferir se há erros. Conteúdo:

```sql
CREATE DATABASE IF NOT EXISTS aprender_palavras
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE aprender_palavras;

CREATE TABLE nichos (
  id   INT          NOT NULL AUTO_INCREMENT,
  nome VARCHAR(50)  NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_nichos_nome (nome)
) ENGINE=InnoDB;

CREATE TABLE grupos (
  id       INT          NOT NULL AUTO_INCREMENT,
  nicho_id INT          NULL,
  nome     VARCHAR(100) NOT NULL,
  ordem    INT          NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_grupos_nicho
    FOREIGN KEY (nicho_id) REFERENCES nichos (id)
) ENGINE=InnoDB;

CREATE TABLE expressoes (
  id         INT          NOT NULL AUTO_INCREMENT,
  grupo_id   INT          NOT NULL,
  ingles     VARCHAR(255) NOT NULL,
  portugues  VARCHAR(255) NOT NULL,
  pronuncia  VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_expressoes_grupo_ingles (grupo_id, ingles),
  CONSTRAINT fk_expressoes_grupo
    FOREIGN KEY (grupo_id) REFERENCES grupos (id)
) ENGINE=InnoDB;

CREATE TABLE usuarios (
  id         INT          NOT NULL AUTO_INCREMENT,
  nome       VARCHAR(100) NOT NULL,
  email      VARCHAR(255) NOT NULL,
  senha_hash VARCHAR(255) NOT NULL,
  nicho_id   INT          NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_usuarios_email (email),
  CONSTRAINT fk_usuarios_nicho
    FOREIGN KEY (nicho_id) REFERENCES nichos (id)
) ENGINE=InnoDB;

CREATE TABLE memorizadas (
  usuario_id   INT NOT NULL,
  expressao_id INT NOT NULL,
  PRIMARY KEY (usuario_id, expressao_id),
  CONSTRAINT fk_memorizadas_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
  CONSTRAINT fk_memorizadas_expressao
    FOREIGN KEY (expressao_id) REFERENCES expressoes (id) ON DELETE CASCADE
) ENGINE=InnoDB;

INSERT INTO nichos (nome) VALUES ('Férias'), ('Atleta');
```

### Como o modelo funciona
- **`nichos`**: os dois públicos (Férias e Atleta). Já vêm inseridos no script.
- **`grupos`**: conjuntos de expressões. O grupo **Básico** tem `nicho_id` vazio (NULL), e é assim que ele vale para os dois nichos. A coluna `ordem` define a posição nas setas de navegação (Básico = 0, depois os grupos do nicho em ordem). Os grupos **não** estão no script: entram pela importação do CSV.
- **`expressoes`**: cada expressão pertence a um grupo; guarda inglês, português e pronúncia.
- **`usuarios`**: nome, e-mail único, `senha_hash` (hash Argon2) e o nicho escolhido no cadastro.
- **`memorizadas`**: tabela de ligação entre usuário e expressão. **Existe linha = a expressão está em "Já memorizadas". Não existe linha = está em "Para estudar".** Mover para "Já memorizadas" é inserir uma linha; mover de volta para "Para estudar" é apagar a linha. Os minigames nunca mexem nessa tabela.

### Escolhas feitas por conta própria (ainda não confirmadas pela pessoa; confirme com ela se for relevante)
- Par (grupo, inglês) único em `expressoes`, para o script de importação não duplicar linhas se rodar duas vezes.
- `ON DELETE CASCADE` em `memorizadas`: apagar um usuário (ou uma expressão) apaga também as marcações.
- Grupo Básico representado por `nicho_id` NULL, e `ordem` nos grupos para as setas.
- Colunas e tipos (INT, VARCHAR) escolhidos como padrão; nada além das tabelas e campos descritos.

---

## 5. Tecnologias (lista fechada)

- Backend: **Python + FastAPI**.
- Frontend: **HTML, CSS puro e JavaScript tradicional** (sem React, Vue ou frameworks de CSS).
- Banco de dados: **MySQL**.
- ORM: **SQLAlchemy**.
- Driver MySQL: **PyMySQL**.
- Servidor: **Uvicorn**.
- Autenticação: **JWT + PyJWT**.
- Validação: **Pydantic**.
- Proteção de senhas: **pwdlib + Argon2**.
- Configurações: **python-dotenv**.
- Requisições HTTP: **Requests**.
- Tradução: **LibreTranslate**.
- Dicionário: **Free Dictionary API**.
- Importação inicial: **CSV + script Python**.
- Controle de versão: **Git e GitHub**.
- Hospedagem: **Alwaysdata**.

Observação: nas regras de funcionamento, o papel exato do LibreTranslate e da Free Dictionary API **não foi descrito**. Não assuma. Quando chegar à etapa do dicionário, **pergunte à pessoa** onde cada uma entra (ou se entram).

---

## 6. Visual e telas (informações de conversas anteriores, confirmar antes de usar)

Em uma versão anterior do projeto (um dicionário pessoal de inglês-português) a pessoa definiu um design: fonte **Inter**, paleta em **azul e preto-azulado**, referência de tela **1440x900**. A pessoa também tem **telas prontas (PNG)** que precisam ser **adaptadas ao novo nicho/versão**. Antes de criar qualquer tela, **peça à pessoa os PNG** e **confirme se esse design continua valendo**. Não altere o design sem autorização.

---

## 7. O que já foi feito até agora

1. **Definição completa do produto** (seções 1 e 2).
2. **Fluxograma completo** da aplicação (seção 3), com todas as decisões.
3. **Script do banco `schema.sql`** com as cinco tabelas e os dois nichos (seção 4). Ainda não foi executado/testado.
4. **Repositório no GitHub criado**; a pessoa informou que já versionou os arquivos iniciais (documentação, fluxograma). Estrutura sugerida para o repositório:

```
aprender-palavras/
├── README.md          (o que é o projeto e como rodar)
├── .gitignore         (venv, __pycache__, .env)
├── .env.example       (modelo das configurações, sem senhas reais)
├── docs/              (prompt do projeto, fluxograma, telas em PNG)
├── backend/           (FastAPI)
├── frontend/          (HTML, CSS e JavaScript)
└── banco/             (schema.sql e o CSV das expressões)
```

---

## 8. O que falta fazer (ordem sugerida)

1. **Ambiente:** criar o ambiente virtual do Python e o `requirements.txt` com as bibliotecas da seção 5; criar o `.env` (dados do banco, chave do JWT) e o `.env.example`.
2. **Banco:** rodar o `schema.sql` no MySQL e conferir as tabelas.
3. **CSV e importação:** definir o formato do CSV e fazer o script Python que carrega as 400 expressões (grupos incluídos).
4. **Backend, parte 1:** conexão com o banco (SQLAlchemy + PyMySQL), cadastro e login com JWT e Argon2.
5. **Backend, parte 2:** rotas dos estudos (grupos, abas, memorizadas), depois dicionário e minigames.
6. **Frontend:** as telas em HTML, CSS e JavaScript, ligadas às rotas, uma tela por vez.
7. **Publicação** na Alwaysdata.

---

## 9. Ponto em aberto agora (comece por aqui)

A última pergunta feita à pessoa, ainda **sem resposta**, foi sobre o **formato do CSV** das expressões:

> Você quer que cada linha do CSV traga o nome do grupo e o nicho (ou "Básico") numa coluna, ou prefere um arquivo CSV separado por grupo?

Também falta saber se a pessoa **já tem** o CSV com as 400 expressões (inglês, tradução e pronúncia) ou se ele ainda precisa ser criado, e qual é a lista de grupos do nicho Férias.

**Sua primeira ação:** cumprimente brevemente, confirme que leu este resumo e faça **apenas uma pergunta** (a do formato do CSV). Depois siga a ordem da seção 8, um passo de cada vez.
