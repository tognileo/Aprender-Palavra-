// direcao.js: tela de escolher a direção do jogo

exigirLogin();

const areaMensagem = document.getElementById("mensagem");
const numeroGrupo = document.getElementById("numero-grupo");

document.getElementById("saudacao").textContent = "Olá, " + pegarNome();
document.getElementById("botao-sair").addEventListener("click", sair);

// Lê o id do grupo no endereço (direcao.html?grupo=3)
const grupoId = Number(new URLSearchParams(window.location.search).get("grupo"));

async function iniciar() {
  const resposta = await chamarApi("/grupos");

  if (!resposta.ok) {
    numeroGrupo.textContent = "Grupo";
    areaMensagem.textContent = mensagemDeErro(resposta);
    return;
  }

  const posicao = resposta.dados.findIndex((grupo) => grupo.id === grupoId);

  // Sem grupo ou grupo que não é da pessoa: volta para a escolha
  if (posicao === -1) {
    window.location.href = "minigames.html";
    return;
  }

  numeroGrupo.textContent = "Grupo " + (posicao + 1);
}

iniciar();

// Botões "Começar": abrem o jogo levando o grupo e a direção no endereço
document.querySelectorAll(".botao-comecar").forEach((botao) => {
  botao.addEventListener("click", () => {
    window.location.href = "jogo.html?grupo=" + grupoId + "&direcao=" + botao.dataset.direcao;
  });
});
