// login.js: tela de entrar

const formulario = document.getElementById("formulario");
const campoEmail = document.getElementById("email");
const campoSenha = document.getElementById("senha");
const areaMensagem = document.getElementById("mensagem");
const areaSucesso = document.getElementById("mensagem-sucesso");
const botao = document.getElementById("botao-entrar");

// Vindo do cadastro, mostra o aviso de conta criada
if (new URLSearchParams(window.location.search).get("cadastro") === "ok") {
  areaSucesso.textContent = "Conta criada! Entre com seu e-mail e sua senha.";
}

formulario.addEventListener("submit", async function (evento) {
  evento.preventDefault();
  areaMensagem.textContent = "";

  const email = campoEmail.value.trim();
  const senha = campoSenha.value;

  if (!email || !senha) {
    areaMensagem.textContent = "Preencha o e-mail e a senha.";
    return;
  }

  botao.disabled = true;
  const resposta = await chamarApi("/auth/login", "POST", { email: email, senha: senha });
  botao.disabled = false;

  if (!resposta.ok) {
    areaMensagem.textContent = mensagemDeErro(resposta);
    return;
  }

  // Login certo: guarda o token no navegador e vai para a tela de estudo
  guardarLogin(resposta.dados.access_token, resposta.dados.nome);
  window.location.href = "estudo.html";
});
