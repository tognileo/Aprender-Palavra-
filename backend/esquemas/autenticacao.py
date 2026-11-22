import re
#VALIDA OS DADOS QUE CHEGAM: SENHA DE OITO CARACTER ETC
from pydantic import BaseModel, Field, field_validator, model_validator


class CadastroEntrada(BaseModel):
    """Dados que a tela de cadastro envia."""
    nome: str = Field(max_length=100)
    email: str = Field(max_length=255)
    senha: str = Field(min_length=8, max_length=128)
    confirmar_senha: str
    nicho_id: int  # o motivo da viagem escolhido

    @field_validator("nome")
    @classmethod
    def nome_nao_vazio(cls, valor):
        valor = valor.strip()
        if not valor:
            raise ValueError("Informe o nome.")
        return valor

    @field_validator("email")
    @classmethod
    def email_valido(cls, valor):
        valor = valor.strip().lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
            raise ValueError("E-mail inválido.")
        return valor

    @model_validator(mode="after")
    def senhas_iguais(self):
        if self.senha != self.confirmar_senha:
            raise ValueError("As senhas não são iguais.")
        return self


class LoginEntrada(BaseModel):
    """Dados que a tela de login envia."""
    email: str = Field(max_length=255)
    senha: str = Field(max_length=128)

    @field_validator("email")
    @classmethod
    def email_minusculo(cls, valor):
        return valor.strip().lower()


class UsuarioSaida(BaseModel):
    """O que a API devolve sobre o usuário (nunca a senha)."""
    id: int
    nome: str
    email: str
    nicho_id: int

    model_config = {"from_attributes": True}


class TokenSaida(BaseModel):
    """O que a API devolve no login."""
    access_token: str
    token_type: str = "bearer"
    nome: str