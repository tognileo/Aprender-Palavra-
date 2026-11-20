-- ============================================================
-- Aprender Palavras - criação do banco de dados (MySQL)
-- Cinco tabelas: nichos, grupos, expressoes, usuarios, memorizadas
-- ============================================================

CREATE DATABASE IF NOT EXISTS aprender_palavras
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE aprender_palavras;

-- ------------------------------------------------------------
-- 1) nichos: os dois públicos do sistema (Férias e Atleta)
-- ------------------------------------------------------------
CREATE TABLE nichos (
  id   INT          NOT NULL AUTO_INCREMENT,
  nome VARCHAR(50)  NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_nichos_nome (nome)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 2) grupos: conjuntos de expressões
--    nicho_id vazio (NULL) = grupo Básico, compartilhado pelos dois nichos
--    ordem = posição do grupo nas setas de navegação (Básico = 0)
-- ------------------------------------------------------------
CREATE TABLE grupos (
  id       INT          NOT NULL AUTO_INCREMENT,
  nicho_id INT          NULL,
  nome     VARCHAR(100) NOT NULL,
  ordem    INT          NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_grupos_nicho
    FOREIGN KEY (nicho_id) REFERENCES nichos (id)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 3) expressoes: as 400 expressões (inglês, português e pronúncia)
-- ------------------------------------------------------------
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

-- ------------------------------------------------------------
-- 4) usuarios: contas cadastradas
--    email único; senha_hash guarda o hash Argon2, nunca a senha pura
-- ------------------------------------------------------------
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

-- ------------------------------------------------------------
-- 5) memorizadas: quais expressões cada usuário marcou como memorizadas
--    Existe linha = aba "Já memorizadas"
--    Não existe linha = aba "Para estudar"
-- ------------------------------------------------------------
CREATE TABLE memorizadas (
  usuario_id   INT NOT NULL,
  expressao_id INT NOT NULL,
  PRIMARY KEY (usuario_id, expressao_id),
  CONSTRAINT fk_memorizadas_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
  CONSTRAINT fk_memorizadas_expressao
    FOREIGN KEY (expressao_id) REFERENCES expressoes (id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Dados iniciais: os dois nichos
-- (os grupos e as expressões entram depois, pelo script de importação do CSV)
-- ------------------------------------------------------------
INSERT INTO nichos (nome) VALUES ('Férias'), ('Atleta');
