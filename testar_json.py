import json
from dominio.livro import Livro

livro = Livro("Dom Casmurro","Machado de Assis", 1899")
print(json.dumps(livro))