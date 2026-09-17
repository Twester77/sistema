class Usuario:
    def __init__(self, nome, matricula):
        if not nome:
            raise ValueError("Nome é obrigatório")
        if not matricula:
            raise ValueError("Matrícula é obrigatória")
        self.nome = nome
        self.matricula = matricula

    def __str__(self):
        return f"{self.nome} ({self.matricula})"