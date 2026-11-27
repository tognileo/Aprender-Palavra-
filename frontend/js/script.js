// script.js: funções usadas por todas as telas
// (falar com a API, guardar o token e sair)

// Endereço da API. Quando publicar o site, troque pelo endereço do servidor.
const ENDERECO_API = "http://127.0.0.1:8000";

// ---------- Token de login (guardado no navegador) ----------

function guardarLogin(token, nome) {
  localStorage.setItem("token", token);
  localStorage.setItem("nome", nome);
}

function pegarToken() {
  return localStorage.getItem("token");
}

function pegarNome() {
  return localStorage.getItem("nome");
}

// Botão "Sair": apaga o token do navegador e volta para o login
function sair() {
  localStorage.removeItem("token");
  localStorage.removeItem("nome");
  window.location.href = "login.html";
}

// Telas que só podem ser vistas logado chamam esta função no começo
function exigirLogin() {
  if (!pegarToken()) {
    window.location.href = "login.html";
  }
}

// ---------- Falar com a API ----------

// Devolve { ok, status, dados }. Nunca "quebra": se o servidor estiver
// desligado, devolve ok = false com uma mensagem em português.
async function chamarApi(caminho, metodo = "GET", corpo = null) {
  const cabecalhos = { "Content-Type": "application/json" };
  const token = pegarToken();
  if (token) {
    cabecalhos["Authorization"] = "Bearer " + token;
  }

  let resposta;
  try {
    resposta = await fetch(ENDERECO_API + caminho, {
      method: metodo,
      headers: cabecalhos,
      body: corpo ? JSON.stringify(corpo) : null,
    });
  } catch (erro) {
    return {
      ok: false,
      status: 0,
      dados: { detail: "Não foi possível conectar ao servidor. Tente de novo em instantes." },
    };
  }

  // Token vencido ou inválido numa tela protegida: volta para o login
  if (resposta.status === 401 && token && caminho !== "/auth/login") {
    sair();
  }

  let dados = null;
  try {
    dados = await resposta.json();
  } catch (erro) {
    // algumas respostas (204) vêm sem corpo
  }
  return { ok: resposta.ok, status: resposta.status, dados: dados };
}

// Transforma a resposta de erro da API em uma frase para mostrar na tela
function mensagemDeErro(resposta) {
  const detalhe = resposta.dados && resposta.dados.detail;

  if (typeof detalhe === "string") {
    return detalhe;
  }

  // Erro de validação (422): lista com um item por campo errado
  if (Array.isArray(detalhe) && detalhe.length > 0) {
    const texto = detalhe[0].msg || "";
    if (texto.includes("at least 8")) {
      return "A senha precisa ter pelo menos 8 caracteres.";
    }
    return texto.replace("Value error, ", "") || "Confira os dados digitados.";
  }

  return "Algo deu errado. Tente de novo.";
}
