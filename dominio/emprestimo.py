class Emprestimo:
    def __init__(self, livro, usuario, data_emprestimo):
        self.livro = livro
        self.usuario = usuario
        self.data_emprestimo = data_emprestimo
        self.devolvido = False

    def __str__(self):
        status = "devolvido" if self.devolvido else "em aberto"
        return f"{self.livro.titulo} -> {self.usuario.nome} ({status})"

    def devolver(self):
        if self.devolvido:
            raise ValueError("Este empréstimo já foi devolvido")
        self.devolvido = True