// cadastro.js: tela de criar conta

const formulario = document.getElementById("formulario");
const campoNome = document.getElementById("nome");
const campoEmail = document.getElementById("email");
const campoSenha = document.getElementById("senha");
const campoConfirmar = document.getElementById("confirmar-senha");
const areaOpcoes = document.getElementById("opcoes-nicho");
const areaMensagem = document.getElementById("mensagem");
const botao = document.getElementById("botao-cadastrar");

// A descrição de cada motivo não vem da API: fica aqui, ligada ao nome do nicho
const DESCRICOES = {
  "Férias": "Viagem de turismo para os EUA",
  "Atleta em competição no exterior": "Entrevistas com a imprensa",
};

function mostrarErro(texto) {
  areaMensagem.textContent = texto;
}

// Busca os nichos na API e desenha as opções de "Motivo da viagem"
async function carregarNichos() {
  const resposta = await chamarApi("/nichos");
  if (!resposta.ok) {
    mostrarErro(mensagemDeErro(resposta));
    return;
  }

  areaOpcoes.innerHTML = "";
  resposta.dados.forEach(function (nicho) {
    const opcao = document.createElement("label");
    opcao.className = "opcao";

    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "nicho";
    radio.value = nicho.id;

    const textos = document.createElement("div");
    const nome = document.createElement("div");
    nome.className = "nome-opcao";
    nome.textContent = nicho.nome;
    const descricao = document.createElement("div");
    descricao.className = "descricao-opcao";
    descricao.textContent = DESCRICOES[nicho.nome] || "";
    textos.appendChild(nome);
    textos.appendChild(descricao);

    opcao.appendChild(radio);
    opcao.appendChild(textos);
    areaOpcoes.appendChild(opcao);
  });
}

formulario.addEventListener("submit", async function (evento) {
  evento.preventDefault();
  mostrarErro("");

  const nome = campoNome.value.trim();
  const email = campoEmail.value.trim();
  const senha = campoSenha.value;
  const confirmar = campoConfirmar.value;
  const escolhido = document.querySelector('input[name="nicho"]:checked');

  // Conferências antes de enviar (a API confere de novo)
  if (!nome || !email || !senha || !confirmar) {
    mostrarErro("Preencha todos os campos.");
    return;
  }
  if (senha.length < 8) {
    mostrarErro("A senha precisa ter pelo menos 8 caracteres.");
    return;
  }
  if (senha !== confirmar) {
    mostrarErro("As senhas não são iguais.");
    return;
  }
  if (!escolhido) {
    mostrarErro("Escolha o motivo da viagem.");
    return;
  }

  botao.disabled = true;
  const resposta = await chamarApi("/auth/cadastro", "POST", {
    nome: nome,
    email: email,
    senha: senha,
    confirmar_senha: confirmar,
    nicho_id: Number(escolhido.value),
  });
  botao.disabled = false;

  if (!resposta.ok) {
    mostrarErro(mensagemDeErro(resposta));
    return;
  }

  // Conta criada: vai para o login com um aviso
  window.location.href = "login.html?cadastro=ok";
});

carregarNichos();
