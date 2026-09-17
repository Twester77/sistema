Boa ideia! Vou montar um **guia de bolso** em Markdown, cobrindo tudo que é essencial dos encontros 5 ao 12. Serve tanto pra consulta rápida quanto pra revisão de última hora. É pra você deixar aberto no VS Code durante a prova (se ele permitir consulta) ou imprimir/abrir no celular.

---

# 📘 Guia de Bolso — Prova ADS / Programação Desktop e Web

## 🧱 As três camadas do sistema

```
sistema/
├── dominio/          ← as regras de negócio (Livro, Usuario, Emprestimo)
├── dados/            ← o repositório (conversa com o banco)
├── janela.py         ← a tela (conversa com o usuário)
├── banco.py          ← cria a tabela e insere dados iniciais
└── biblioteca.db     ← o arquivo do banco de dados
```

**Regra de ouro:** cada camada só conhece a de baixo.  
- A tela conhece o domínio e o repositório.  
- O repositório conhece o domínio.  
- O domínio não conhece ninguém.

Nunca colocar `input()` ou `print()` dentro de `dominio/`.  
Nunca escrever SQL dentro de `janela.py`.

---

## 🏛️ DOMÍNIO — POO essencial

### Classe, objeto, self, `__init__`

```python
class Livro:
    def __init__(self, titulo, autor, ano):
        # validações ANTES de guardar
        if not titulo:
            raise ValueError("Título é obrigatório")
        if not autor:
            raise ValueError("Autor é obrigatório")
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
```

- `class` = fôrma. `Livro(...)` = objeto.
- `self` = o próprio objeto.
- `__init__` roda sozinho quando o objeto nasce.
- Nunca chamar `__init__` diretamente.

### `__str__` (como o objeto se apresenta)

```python
    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self.ano})"
```

→ Usado no `print(livro)` e em f-strings.

### `@property` e setter (encapsulamento)

```python
    @property
    def ano(self):
        return self._ano

    @ano.setter
    def ano(self, valor):
        if valor < 1450 or valor > 2026:
            raise ValueError(f"Ano inválido: {valor}")
        self._ano = valor
```

**Por que serve:** impede que `livro.ano = 3000` passe sem validação.  
Por fora continua `livro.ano`; por dentro passa pela regra.

### Relação entre objetos (composição)

```python
class Emprestimo:
    def __init__(self, livro, usuario, data):
        self.livro = livro        # objeto Livro
        self.usuario = usuario    # objeto Usuario
        self.data = data
        self.devolvido = False
```

Navegação: `emp.livro.autor.nome` → cada ponto atravessa uma ligação.

### Método que recusa ação inválida

```python
    def devolver(self):
        if self.devolvido:
            raise ValueError("Este empréstimo já foi devolvido")
        self.devolvido = True
```

---

## 🗄️ DADOS — Repositório com SQLite

### Estrutura básica do repositório

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

### Regras essenciais de SQL

| Operação | Comando | Cuidado |
|---|---|---|
| Criar tabela | `CREATE TABLE IF NOT EXISTS ...` | Rodar antes dos INSERTs |
| Inserir | `INSERT INTO livro (col1, col2) VALUES (?, ?)` | Valores sempre via `?` |
| Ler | `SELECT ... FROM livro WHERE id = ?` | Sem WHERE traz tudo |
| Alterar | `UPDATE livro SET ... WHERE id = ?` | **SEM WHERE = tabela inteira** |
| Apagar | `DELETE FROM livro WHERE id = ?` | **SEM WHERE = apaga tudo** |
| Confirmar | `conexao.commit()` | Sem isso, nada é salvo |

### Pegadinhas clássicas

- **Tupla de um item:** `(2,)` — a vírgula é obrigatória. `(2)` não é tupla.
- **`fetchone()`** → uma linha ou `None`.  
- **`fetchall()`** → lista (vazia se nada achou).
- **`lastrowid`** → o id que o banco gerou no último INSERT.
- **Sem `commit()`** → o dado fica só na sessão; some ao fechar.

---

## 🖼️ JANELA — Tkinter

### Esqueleto mínimo

```python
import tkinter as tk

janela = tk.Tk()
janela.title("Biblioteca")
janela.geometry("460x520")

# widgets aqui...

janela.mainloop()
```

### Widgets essenciais

| Widget | Para que serve | Método chave |
|---|---|---|
| `tk.Label` | texto fixo ou resultado | `.config(text=..., fg=...)` |
| `tk.Entry` | campo de digitação | `.get()` / `.delete(0, tk.END)` |
| `tk.Listbox` | lista de itens | `.insert(tk.END, ...)` / `.curselection()` |
| `tk.Button` | botão | `command=funcao` (SEM parênteses!) |
| `tk.Frame` | agrupar widgets | usa `pack` ou `grid` internamente |

### Amarrar botão à função

```python
def cadastrar():
    ...

tk.Button(janela, text="Cadastrar", command=cadastrar).pack()
```

⚠️ `command=cadastrar()` com parênteses → executa na hora de criar o botão (errado).

### Ler campos e tratar erro

```python
def cadastrar():
    titulo = campo_titulo.get()
    autor = campo_autor.get()
    ano = campo_ano.get()

    try:
        livro = Livro(titulo, autor, int(ano))
        repositorio.salvar(livro)
        atualizar_lista()
        campo_titulo.delete(0, tk.END)
        campo_autor.delete(0, tk.END)
        campo_ano.delete(0, tk.END)
        resultado.config(text="Cadastrado: " + str(livro), fg="blue")
    except ValueError as erro:
        resultado.config(text=str(erro), fg="red")
```

### Atualizar a lista a partir do banco

```python
livros_na_tela = []

def atualizar_lista():
    lista.delete(0, tk.END)
    livros_na_tela.clear()
    for livro in repositorio.listar():
        livros_na_tela.append(livro)
        lista.insert(tk.END, str(livro))
```

**Por que `livros_na_tela`?**  
A Listbox mostra; ela não guarda. `livros_na_tela` mantém a ordem dos objetos que estão na tela — serve para ligar a posição clicada ao objeto real.

### Descobrir livro selecionado

```python
def livro_selecionado():
    selecionados = lista.curselection()
    if not selecionados:
        resultado.config(text="Selecione um livro.", fg="red")
        return None
    posicao = selecionados[0]
    return livros_na_tela[posicao]
```

⚠️ **Posição na tela ≠ id do banco.**  
A posição serve para achar o objeto em `livros_na_tela`. O id está dentro do objeto (`.id`).

---

## 🧠 Perguntas conceituais que provavelmente caem

### 1. Por que a classe não pode ter `input()` ou `print()`?
Porque ela representa o **negócio**, não a conversa com o usuário. Se tiver `input`, ela deixa de ser reaproveitável (não serve para web, API, etc.). Quem conversa com o usuário é a camada de cima.

### 2. Por que usar `@property` no ano?
Para que **toda** alteração de ano passe pela validação — inclusive depois que o objeto foi criado. Sem `@property`, o construtor valida, mas `livro.ano = 3000` passa direto.

### 3. O que faz o `_para_objeto`?
Transforma uma linha do banco (tupla) em um objeto do domínio (`Livro`). Assim, o resto do sistema trabalha com objetos de verdade, com `.titulo`, `.descricao()`, etc.

### 4. Por que o `UPDATE` sem `WHERE` é perigoso?
Porque sem `WHERE` ele altera **toda a tabela**. É a mesma lógica do `DELETE`.

### 5. Por que precisa `commit()`?
Porque o SQLite trabalha com transações. Sem `commit`, as alterações ficam em memória e somem quando o programa fecha.

### 6. Por que `command=cadastrar` sem parênteses?
Porque o Tkinter precisa **guardar a função** para chamar quando o botão for clicado. Com parênteses, ela é executada na hora.

### 7. Diferença entre `Livro` e `livro`?
- `Livro` (maiúsculo) = a classe (a fôrma).
- `livro` (minúsculo) = um objeto criado a partir dela.

### 8. Se amanhã a janela virar site, quantos arquivos do domínio mudam?
**Nenhum.** O domínio é independente da interface. É justamente por isso que ele fica intacto do encontro 5 ao 12.

---

## 🔥 Erros mais comuns e como resolver

| Mensagem | Causa | Solução |
|---|---|---|
| `ValueError: Ano inválido: 3000` | Sua classe funcionou | Não é bug — é a validação |
| `NameError: name 'X' is not defined` | Faltou import ou a função vem depois | Mover função/import para cima |
| `AttributeError: 'tuple' object has no attribute 'titulo'` | O repositório devolveu tupla | Usar `_para_objeto` no `listar` |
| `AttributeError: 'Livro' object has no attribute 'id'` | Livro nunca passou pelo banco | Só tem id quem foi salvo ou lido |
| `ModuleNotFoundError: No module named 'dominio'` | Rodou de dentro de `dados/` ou pasta errada | Rodar a partir de `sistema/` |
| `IndentationError` | Recuo errado | 4 espaços, sempre |
| `TypeError: can only concatenate str` | Somou texto com número | Usar `int()` no input |
| `sqlite3.OperationalError: no such table: livro` | Rodou em pasta com banco vazio | Rodar `banco.py` antes |
| Janela abre e fecha sozinha | Faltou `mainloop()` | Adicionar no fim do arquivo |
| Botão não faz nada | `command=funcao()` com parênteses | Tirar os parênteses |

---

## ✅ Checklist antes de entregar/defender

- [ ] `dominio/` tem `livro.py`, `usuario.py`, `emprestimo.py` + `__init__.py` vazio
- [ ] `dados/` tem `repositorio_livro.py` + `__init__.py` vazio
- [ ] Nenhum `input`/`print` de conversa dentro de `dominio/` ou `dados/`
- [ ] `banco.py` cria a tabela e insere dados iniciais
- [ ] `janela.py` roda o CRUD completo (cadastrar, listar, alterar, excluir)
- [ ] Os dados sobrevivem ao fechar e reabrir a janela
- [ ] `testar_dominio.py` e `testar_repositorio.py` rodam sem erro
- [ ] UTF-8 configurado (`sys.stdout.reconfigure`) se houver acentos

---

Boa prova na segunda! Esse guia cobre o que o professor enfatizou nos roteiros — principalmente a separação das camadas, o encapsulamento com `@property` e a pegadinha do `WHERE`. Se quiser, posso montar um segundo arquivo com **exemplos de código prontos para colar** (o CRUD completo), mas o guia acima já é a cola ideal. 🚀