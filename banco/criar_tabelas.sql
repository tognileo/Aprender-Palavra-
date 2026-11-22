-- Aprender Palavras: criação do banco e das 5 tabelas
-- Sem CREATE DATABASE e sem USE: o banco já foi criado no painel do Alwaysdata.
-- O banco já foi criado no painel; selecione-o no phpMyAdmin antes de rodar.
-- Rode este arquivo UMA vez, com o banco vazio.

-- Os dois públicos do site
CREATE TABLE nichos (
  id   INT          NOT NULL AUTO_INCREMENT,
  nome VARCHAR(50)  NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_nichos_nome (nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Grupos de expressões. O grupo "Básico" tem nicho_id vazio (NULL),
-- por isso vale para os dois nichos. "ordem" é a posição nas setas.
CREATE TABLE grupos (
  id       INT          NOT NULL AUTO_INCREMENT,
  nicho_id INT          NULL,
  nome     VARCHAR(100) NOT NULL,
  ordem    INT          NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_grupos_nicho
    FOREIGN KEY (nicho_id) REFERENCES nichos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- As expressões. "ordem" = importância dentro do grupo (1 = mais importante).
-- "audio" começa vazio (NULL); será preenchido só no futuro.
CREATE TABLE expressoes (
  id         INT          NOT NULL AUTO_INCREMENT,
  grupo_id   INT          NOT NULL,
  ingles     VARCHAR(255) NOT NULL,
  portugues  VARCHAR(255) NOT NULL,
  pronuncia  VARCHAR(255) NOT NULL,
  ordem      INT          NOT NULL,
  audio      VARCHAR(255) NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_expressoes_grupo_ingles (grupo_id, ingles),
  CONSTRAINT fk_expressoes_grupo
    FOREIGN KEY (grupo_id) REFERENCES grupos (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- As contas. O nicho é escolhido no cadastro e não muda.
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Existe linha = a expressão está em "Já memorizadas".
-- Não existe linha = está em "Para estudar".
CREATE TABLE memorizadas (
  usuario_id   INT NOT NULL,
  expressao_id INT NOT NULL,
  PRIMARY KEY (usuario_id, expressao_id),
  CONSTRAINT fk_memorizadas_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
  CONSTRAINT fk_memorizadas_expressao
    FOREIGN KEY (expressao_id) REFERENCES expressoes (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Os nichos já entram prontos. Os nomes são os mesmos do CSV e da tela de cadastro.
INSERT INTO nichos (nome) VALUES ('Férias'), ('Atleta em competição no exterior');
