const API=  "http://127.0.0.1:8000";
async function listarLivros() {
    const resposta = await fetch(API + "/livros");
    const livros = await resposta.json();
    
    const lista = document.getElementById("lista");
    lista.innerHTML = "";
    for(const livro of livros) {
        const item = document.createElement("li");
        item.textContent = '${livro.id} - ${livro.titulo} (${livro.ano}) ';
        lista.appendChild(item);
    }

    
}

const botaoListar= document.getElementById("botao-listar");
botaoListar.addEventListener("click", listarLivros);