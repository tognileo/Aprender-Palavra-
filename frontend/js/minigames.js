// minigames.js: tela de escolha do grupo para jogar

exigirLogin();

const areaMensagem = document.getElementById("mensagem");
const listaGrupos = document.getElementById("lista-grupos");

document.getElementById("saudacao").textContent = "Olá, " + pegarNome();
document.getElementById("botao-sair").addEventListener("click", sair);

// Monta o cartão de um grupo.
// É um link: o id do grupo vai no endereço para a próxima tela.
function criarCartaoGrupo(grupo, numero) {
  const cartao = document.createElement("a");
  cartao.className = "cartao-grupo";
  cartao.href = "direcao.html?grupo=" + grupo.id;

  const textos = document.createElement("div");

  const etiqueta = document.createElement("span");
  etiqueta.className = "etiqueta";
  etiqueta.textContent = "Grupo " + numero;

  const nome = document.createElement("h2");
  nome.textContent = grupo.nome;

  textos.append(etiqueta, nome);

  const seta = document.createElement("span");
  seta.className = "cartao-grupo-seta";
  seta.textContent = "›";

  cartao.append(textos, seta);
  return cartao;
}

async function iniciar() {
  // A API já devolve só o Básico e os grupos do nicho da pessoa
  const resposta = await chamarApi("/grupos");
  listaGrupos.innerHTML = "";

  if (!resposta.ok) {
    areaMensagem.textContent = mensagemDeErro(resposta);
    return;
  }

  resposta.dados.forEach((grupo, indice) => {
    listaGrupos.appendChild(criarCartaoGrupo(grupo, indice + 1));
  });
}

iniciar();
