from dominio.livro import Livro
from dominio.usuario import Usuario
from dominio.emprestimo import Emprestimo

print("---- testando o dominio, sem tela nenhuma ----")

# 1. Criar livro válido
livro = Livro("Dom Casmurro", "Machado de Assis", 1899)
print("livro criado:", livro)

# 2. Tentar criar com ano inválido – deve levantar ValueError
try:
    Livro("Sem ano", "Alguem", 3000)
    print("FALHOU: o ano 3000 passou")
except ValueError as erro:
    print("ok, barrou:", erro)

# 3. Usuário e empréstimo
ana = Usuario("Ana Souza", "2026001")
emp = Emprestimo(livro, ana, "24/08/2026")
print("emprestimo:", emp)

# 4. Devolver uma vez
emp.devolver()
print("depois de devolver:", emp)

# 5. Tentar devolver novamente – deve levantar ValueError
try:
    emp.devolver()
    print("FALHOU: devolveu duas vezes")
except ValueError as erro:
    print("ok, barrou:", erro)

# 6. Lista de livros (acervo)
acervo = [
    livro,
    Livro("Iracema", "Jose de Alencar", 1865),
]
print("livros no acervo:", len(acervo))
print("o autor do primeiro:", acervo[0].autor)

# 7. Busca por título (case insensitive)
procurado = "iracema"
escolhido = None
for item in acervo:
    if item.titulo.lower() == procurado.lower():
        escolhido = item
print("escolhido:", escolhido)

# 8. Lista de empréstimos e filtro dos em aberto
emprestimos = [emp, Emprestimo(acervo[1], ana, "24/08/2026")]
em_aberto = [e for e in emprestimos if not e.devolvido]
print("emprestimos:", len(emprestimos), "- em aberto:", len(em_aberto))