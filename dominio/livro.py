from datetime import date

class Livro:
    def __init__(self, titulo, autor, ano):
        if not titulo:
            raise ValueError("Título é obrigatório")
        if not autor:
            raise ValueError("Autor é obrigatório")
        # Usa o setter para validar o ano
        self.ano = ano
        self.titulo = titulo
        self.autor = autor

    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self._ano})"

    @property
    def ano(self):
        return self._ano

    @ano.setter
    def ano(self, valor):
        if valor < 1450 or valor > date.today().year:
            raise ValueError(f"Ano inválido: {valor}")
        self._ano = valor

    def idade(self):
        return date.today().year - self._ano

    def e_classico(self):
        return self.idade() > 100