const API=  "http://127.0.0.1:8000";
async function listarLivros() {
    const resposta = await fetch(API + "/livros");
    const livros = await resposta.json();
    console.log(livros);

    
}

const botaoListar= document.getElementById("botao-listar");
botaoListar.addEventListener("click", listarLivros);