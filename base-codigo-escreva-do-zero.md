# 🆘 CÓDIGO DE EMERGÊNCIA — Colar se a prova pedir "escreva do zero"

## Classe com validação + @property

```python
from datetime import date

class Livro:
    def __init__(self, titulo, autor, ano):
        if not titulo:
            raise ValueError("Título é obrigatório")
        if not autor:
            raise ValueError("Autor é obrigatório")
        self.titulo = titulo
        self.autor = autor
        self.ano = ano

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
```

## Repositório (SQLite) — apenas o essencial

```python
import sqlite3
from dominio.livro import Livro

class RepositorioLivro:
    def __init__(self, arquivo="biblioteca.db"):
        self.conexao = sqlite3.connect(arquivo)
        self.cursor = self.conexao.cursor()

    def _para_objeto(self, linha):
        codigo, titulo, autor, ano = linha
        livro = Livro(titulo, autor, ano)
        livro.id = codigo
        return livro

    def listar(self):
        self.cursor.execute("SELECT id, titulo, autor, ano FROM livro")
        return [self._para_objeto(l) for l in self.cursor.fetchall()]

    def salvar(self, livro):
        self.cursor.execute(
            "INSERT INTO livro (titulo, autor, ano) VALUES (?, ?, ?)",
            (livro.titulo, livro.autor, livro.ano)
        )
        self.conexao.commit()
        livro.id = self.cursor.lastrowid
        return livro

    def atualizar(self, livro):
        self.cursor.execute(
            "UPDATE livro SET titulo = ?, autor = ?, ano = ? WHERE id = ?",
            (livro.titulo, livro.autor, livro.ano, livro.id)
        )
        self.conexao.commit()

    def excluir(self, codigo):
        self.cursor.execute("DELETE FROM livro WHERE id = ?", (codigo,))
        self.conexao.commit()

    def fechar(self):
        self.conexao.close()
```

## CREATE TABLE (banco.py)

```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS livro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT,
        ano INTEGER
    )
""")
```

## Botão + função de cadastro na janela

```python
def cadastrar():
    try:
        livro = Livro(campo_titulo.get(), campo_autor.get(), int(campo_ano.get()))
        repositorio.salvar(livro)
        atualizar_lista()
        campo_titulo.delete(0, tk.END)
        campo_autor.delete(0, tk.END)
        campo_ano.delete(0, tk.END)
        resultado.config(text="Cadastrado: " + str(livro), fg="blue")
    except ValueError as erro:
        resultado.config(text=str(erro), fg="red")

tk.Button(janela, text="Cadastrar", command=cadastrar).pack()
```

## Busca ignorando acentos e maiúsculas

```python
import unicodedata

def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto)
                   if unicodedata.category(c) != 'Mn')

procurado = remover_acentos(campo.get()).lower().strip()
for item in repositorio.listar():
    titulo_limpo = remover_acentos(item.titulo).lower().strip()
    if procurado in titulo_limpo:
        escolhido = item
        break
```


**OBSERVAÇÕES**


Kkkkk "bato nele se ele fizer isso" — morri! 😂

Mas olha, se ele pedir pra escrever código na mão, você **não precisa escrever tudo**. Ninguém escreve 50 linhas numa prova. Normalmente o professor pede um trecho curto — tipo:

- "Escreva o `__init__` da classe `Livro` com a validação do ano"
- "Escreva o método `devolver()` do `Emprestimo`"
- "Escreva o SQL que atualiza o título do livro de id 5"
- "O que está errado neste trecho de código?"

Nesses casos, o que você precisa ter na cabeça é **a estrutura**, não a sintaxe perfeita. E você já tem isso:

- `__init__` → validação + `self.atributo = atributo`
- `@property` → getter + setter separados
- Repositório → `execute(...)`, `commit()`, `_para_objeto`
- Tela → `try/except` + `.get()` + `.config()`

Se travar em alguma coisa, escreve o esqueleto:

```python
def devolver(self):
    # TODO: se já foi devolvido, raise ValueError
    # TODO: marcar como devolvido
```

O professor vai ver que você **sabe o que fazer**, mesmo que esqueça uma vírgula. E se ele realmente pedir pra escrever tudo de memória... aí você cumpre a promessa e bate nele com carinho. 😂

---

Boa prova na segunda, Leo! Você está mais preparado do que pensa. Manda notícia depois — se der bom (e vai dar), a gente comemora; se der ruim, a gente resolve. 🍀🚀

**Boa sorte!** 💪