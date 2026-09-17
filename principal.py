from dominio.livro import Livro
from dominio.usuario import Usuario
from dominio.emprestimo import Emprestimo

# Dados iniciais
acervo = []
emprestimos = []
usuario = Usuario("Aluno", "0000")  # usuário fixo para simplificar

while True:
    print()
    print("=== BIBLIOTECA ===")
    print("1 - Cadastrar Livro")
    print("2 - Listar acervo")
    print("3 - Emprestar")
    print("4 - Devolver")      # Desafio
    print("0 - Sair")
    opcao = input("Opcao: ")

    if opcao == "1":
        titulo = input("Titulo: ")
        autor = input("Autor: ")
        try:
            ano = int(input("Ano: "))
        except ValueError:
            print("Ano deve ser um número. Tente novamente.")
            continue

        try:
            acervo.append(Livro(titulo, autor, ano))
            print("Livro cadastrado.")
        except ValueError as erro:
            print("Nao deu:", erro)

    elif opcao == "2":
        if not acervo:
            print("Acervo vazio.")
        else:
            for livro in acervo:
                print("-", livro)   # usa o __str__ do Livro

    elif opcao == "3":
        procurado = input("Titulo do livro para emprestar: ")
        escolhido = None
        for livro in acervo:
            if livro.titulo.lower() == procurado.lower():
                escolhido = livro
                break

        if escolhido is None:
            print("Nao esta no acervo.")
        else:
            # Cria um empréstimo e guarda na lista
            emp = Emprestimo(escolhido, usuario, "24/08/2026")
            emprestimos.append(emp)
            print("Emprestado:", emp)

    elif opcao == "4":   # Devolver (desafio)
        procurado = input("Titulo do livro para devolver: ")
        emprestimo_encontrado = None
        for e in emprestimos:
            if (e.livro.titulo.lower() == procurado.lower() and
                    not e.devolvido):
                emprestimo_encontrado = e
                break

        if emprestimo_encontrado is None:
            print("Nenhum empréstimo em aberto para este título.")
        else:
            try:
                emprestimo_encontrado.devolver()
                print("Devolvido com sucesso.")
            except ValueError as erro:
                print("Erro:", erro)

    elif opcao == "0":
        print("Ate logo.")
        break

    else:
        print("Opcao invalida.")