// estudo.js: tela de estudo (por enquanto, só a versão provisória)

exigirLogin();

document.getElementById("saudacao").textContent = "Olá, " + pegarNome() + "!";
document.getElementById("botao-sair").addEventListener("click", sair);
