// estudo.js: tela de estudo (grupos, abas e expressões)

exigirLogin();

const setaVoltar = document.getElementById("seta-voltar");
const setaAvancar = document.getElementById("seta-avancar");
const numeroGrupo = document.getElementById("numero-grupo");
const nomeGrupo = document.getElementById("nome-grupo");
const abaEstudar = document.getElementById("aba-estudar");
const abaMemorizadas = document.getElementById("aba-memorizadas");
const areaMensagem = document.getElementById("mensagem");
const lista = document.getElementById("lista");

let grupos = [];            // Básico + grupos do nicho, já na ordem
let posicao = 0;            // qual grupo está na tela (0 = Básico)
let expressoes = [];        // expressões do grupo atual
let mostrarMemorizadas = false;  // qual aba está aberta

document.getElementById("saudacao").textContent = "Olá, " + pegarNome();
document.getElementById("botao-sair").addEventListener("click", sair);

// Cria um elemento com uma classe e um texto.
// textContent mostra o texto como texto, nunca como código HTML.
function criar(tag, classe, texto) {
  const elemento = document.createElement(tag);
  elemento.className = classe;
  if (texto) {
    elemento.textContent = texto;
  }
  return elemento;
}

// ---------- Desenhar a tela ----------

function desenharLista() {
  abaEstudar.classList.toggle("ativa", !mostrarMemorizadas);
  abaMemorizadas.classList.toggle("ativa", mostrarMemorizadas);
  lista.innerHTML = "";

  const visiveis = expressoes.filter((e) => e.memorizada === mostrarMemorizadas);

  if (visiveis.length === 0) {
    const texto = mostrarMemorizadas
      ? "Nenhuma expressão memorizada neste grupo."
      : "Não há expressões para estudar neste grupo.";
    lista.appendChild(criar("p", "lista-vazia", texto));
    return;
  }

  visiveis.forEach((expressao) => lista.appendChild(criarCartao(expressao)));
}

function criarCartao(expressao) {
  const cartao = criar("article", "expressao");

  const textos = criar("div", "expressao-textos");
  textos.appendChild(criar("h2", "", expressao.ingles));
  textos.appendChild(criar("p", "expressao-pronuncia", expressao.pronuncia));
  textos.appendChild(criar("p", "expressao-portugues", expressao.portugues));
  cartao.appendChild(textos);

  // O botão de áudio só aparece se a expressão tiver áudio
  if (expressao.audio) {
    const botaoAudio = criar("button", "botao-audio", "🔊");
    botaoAudio.type = "button";
    botaoAudio.setAttribute("aria-label", "Ouvir");
    botaoAudio.addEventListener("click", () => new Audio(expressao.audio).play());
    cartao.appendChild(botaoAudio);
  }

  const texto = expressao.memorizada ? "Voltar para estudar" : "✓  Já memorizei";
  const botaoMover = criar("button", "botao-contorno", texto);
  botaoMover.type = "button";
  botaoMover.addEventListener("click", () => mover(expressao, botaoMover));
  cartao.appendChild(botaoMover);

  return cartao;
}

// ---------- Falar com a API ----------

// Move a expressão para a outra aba e salva no banco
async function mover(expressao, botao) {
  areaMensagem.textContent = "";
  botao.disabled = true;

  const metodo = expressao.memorizada ? "DELETE" : "POST";
  const resposta = await chamarApi("/expressoes/" + expressao.id + "/memorizar", metodo);

  if (!resposta.ok) {
    botao.disabled = false;
    areaMensagem.textContent = mensagemDeErro(resposta);
    return;
  }

  expressao.memorizada = !expressao.memorizada;
  desenharLista();
}

async function abrirGrupo(novaPosicao) {
  posicao = novaPosicao;
  const grupo = grupos[posicao];

  numeroGrupo.textContent = "GRUPO " + (posicao + 1);
  nomeGrupo.textContent = grupo.nome;
  areaMensagem.textContent = "";
  lista.innerHTML = "";

  // Setas desativadas enquanto carrega (evita misturar dois grupos)
  setaVoltar.disabled = true;
  setaAvancar.disabled = true;

  const resposta = await chamarApi("/grupos/" + grupo.id + "/expressoes");

  // Nas pontas, a seta continua desativada
  setaVoltar.disabled = posicao === 0;
  setaAvancar.disabled = posicao === grupos.length - 1;

  if (!resposta.ok) {
    expressoes = [];
    areaMensagem.textContent = mensagemDeErro(resposta);
    return;
  }

  expressoes = resposta.dados;
  desenharLista();
}

async function iniciar() {
  const resposta = await chamarApi("/grupos");

  if (!resposta.ok || resposta.dados.length === 0) {
    nomeGrupo.textContent = "Não foi possível carregar";
    areaMensagem.textContent = resposta.ok ? "Nenhum grupo encontrado." : mensagemDeErro(resposta);
    return;
  }

  grupos = resposta.dados;
  abrirGrupo(0); // sempre começa no Básico
}

setaVoltar.addEventListener("click", () => abrirGrupo(posicao - 1));
setaAvancar.addEventListener("click", () => abrirGrupo(posicao + 1));

abaEstudar.addEventListener("click", () => {
  mostrarMemorizadas = false;
  desenharLista();
});
abaMemorizadas.addEventListener("click", () => {
  mostrarMemorizadas = true;
  desenharLista();
});

iniciar();
