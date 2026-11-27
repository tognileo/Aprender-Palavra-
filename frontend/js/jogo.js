// jogo.js: o minigame de alternativas
// O jogo não muda nada no banco: ele só lê as expressões do grupo.

exigirLogin();

const areaMensagem = document.getElementById("mensagem");
const etiquetaJogo = document.getElementById("etiqueta-jogo");
const areaJogo = document.getElementById("area-jogo");
const rotuloPergunta = document.getElementById("rotulo-pergunta");
const textoPergunta = document.getElementById("texto-pergunta");
const pronunciaPergunta = document.getElementById("pronuncia-pergunta");
const botaoAudio = document.getElementById("botao-audio");
const areaAlternativas = document.getElementById("alternativas");
const rodape = document.getElementById("rodape");
const retorno = document.getElementById("retorno");
const botaoProxima = document.getElementById("botao-proxima");

document.getElementById("saudacao").textContent = "Olá, " + pegarNome();
document.getElementById("botao-sair").addEventListener("click", sair);

// Lê o grupo e a direção no endereço (jogo.html?grupo=3&direcao=en-pt)
const parametros = new URLSearchParams(window.location.search);
const grupoId = Number(parametros.get("grupo"));
const inglesParaPortugues = parametros.get("direcao") !== "pt-en";

// Qual campo aparece na pergunta e qual aparece nas alternativas
const campoPergunta = inglesParaPortugues ? "ingles" : "portugues";
const campoResposta = inglesParaPortugues ? "portugues" : "ingles";

let expressoes = [];  // todas do grupo (memorizadas ou não)
let fila = [];        // as que ainda não foram perguntadas nesta rodada
let atual = null;     // a expressão da pergunta que está na tela

// Devolve uma cópia da lista em ordem sorteada
function embaralhar(lista) {
  const copia = [...lista];
  for (let i = copia.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copia[i], copia[j]] = [copia[j], copia[i]];
  }
  return copia;
}

// A certa + até 3 erradas do mesmo grupo, sem textos repetidos
function montarAlternativas(certa) {
  const usados = new Set([certa[campoResposta]]);
  const erradas = [];

  for (const outra of embaralhar(expressoes)) {
    if (erradas.length === 3) break;
    // Mesma pergunta em outra linha seria uma segunda resposta certa
    if (outra[campoPergunta] === certa[campoPergunta]) continue;
    if (usados.has(outra[campoResposta])) continue;
    usados.add(outra[campoResposta]);
    erradas.push(outra);
  }

  return embaralhar([certa, ...erradas]);
}

function mostrarPergunta() {
  // Quando todas já foram perguntadas, sorteia uma nova rodada
  if (fila.length === 0) {
    fila = embaralhar(expressoes);
    // Não repete a última pergunta logo no começo da rodada nova
    if (atual && fila.length > 1 && fila[fila.length - 1].id === atual.id) {
      fila.unshift(fila.pop());
    }
  }
  atual = fila.pop(); // pega a última da fila

  rotuloPergunta.textContent = inglesParaPortugues ? "O QUE SIGNIFICA?" : "COMO SE DIZ EM INGLÊS?";
  textoPergunta.textContent = atual[campoPergunta];

  // Pronúncia e áudio só no inglês para português:
  // na outra direção eles entregariam a resposta
  pronunciaPergunta.textContent = inglesParaPortugues ? atual.pronuncia : "";
  botaoAudio.hidden = !(inglesParaPortugues && atual.audio);

  rodape.hidden = true;
  areaAlternativas.innerHTML = "";

  montarAlternativas(atual).forEach((opcao, indice) => {
    const botao = document.createElement("button");
    botao.type = "button";
    botao.className = "alternativa";

    const letra = document.createElement("span");
    letra.className = "alternativa-letra";
    letra.textContent = "ABCD"[indice];

    const texto = document.createElement("span");
    texto.className = "alternativa-texto";
    texto.textContent = opcao[campoResposta];

    const marca = document.createElement("span");
    marca.className = "alternativa-marca";

    botao.append(letra, texto, marca);
    botao.dataset.id = opcao.id;
    botao.addEventListener("click", () => responder(botao));
    areaAlternativas.appendChild(botao);
  });
}

function responder(escolhido) {
  const acertou = Number(escolhido.dataset.id) === atual.id;

  areaAlternativas.querySelectorAll(".alternativa").forEach((botao) => {
    botao.disabled = true; // só vale a primeira resposta

    if (Number(botao.dataset.id) === atual.id) {
      botao.classList.add("certa");
      botao.querySelector(".alternativa-marca").textContent = "Resposta certa";
    } else if (botao === escolhido) {
      botao.classList.add("errada");
      botao.querySelector(".alternativa-marca").textContent = "Sua resposta";
    }
  });

  retorno.textContent = acertou ? "Muito bem! Você acertou." : "Quase! Veja a resposta certa acima.";
  rodape.hidden = false;
}

async function iniciar() {
  const respostaGrupos = await chamarApi("/grupos");

  if (!respostaGrupos.ok) {
    etiquetaJogo.textContent = "Jogo";
    areaMensagem.textContent = mensagemDeErro(respostaGrupos);
    return;
  }

  const posicao = respostaGrupos.dados.findIndex((grupo) => grupo.id === grupoId);
  if (posicao === -1) {
    window.location.href = "minigames.html";
    return;
  }

  const direcao = inglesParaPortugues ? "Inglês para português" : "Português para inglês";
  etiquetaJogo.textContent = "Grupo " + (posicao + 1) + " · " + direcao;

  const resposta = await chamarApi("/grupos/" + grupoId + "/expressoes");

  if (!resposta.ok || resposta.dados.length === 0) {
    areaMensagem.textContent = resposta.ok ? "Este grupo não tem expressões." : mensagemDeErro(resposta);
    return;
  }

  expressoes = resposta.dados;
  areaJogo.hidden = false;
  mostrarPergunta();
}

botaoProxima.addEventListener("click", mostrarPergunta);
botaoAudio.addEventListener("click", () => new Audio(atual.audio).play());

iniciar();
