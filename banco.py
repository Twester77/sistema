import sys
import locale

sys.stdout.reconfigure(encoding='utf-8')

try:
   locale.setlocale(locale.LC_ALL, 'pt-BR.UTF-8')
except locale.Error:
   #Se não tiver lcoale segue sem erro
   pass

import sqlite3
conexao = sqlite3.connect('biblioteca.db')
cursor = conexao.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS livro (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                   titulo TEXT NOT NULL,
                   autor TEXT,
                   ano INTEGER 
               )
              """ )
print("Tabela criada com sucesso.")


livros = {
    ("Dom Casmurro", "Machado de Assis", 1899),
    ("Iracema", "José de Alencar", 1865),
    ("Memória Póstumas de Brás Cubas", "Machado de Assis", 1881),
}

# for titulo, autor, ano in livros:

#     cursor.execute("INSERT INTO livro (titulo, autor, ano) VALUES (?, ?, ?)", (titulo, autor, ano), 

#   )

print(f"{len(livros)} Livros inseridos porém aida não confirmados.")

conexao.commit()

cursor.execute (
    "SELECT id, titulo, autor, ano FROM livro WHERE id = ?",
    (2,)
)

print(cursor.fetchone())

cursor.execute("UPDATE livro SET ano = ? WHERE id = ?",
               )

cursor.execute("DELETE FROM livro WHERE id = ?", (3,))

conexao.commit()


print("Commit feito - dados salvos no arquivo.") 

cursor.execute("SELECT id, titulo , autor , ano FROM livro ")

print("\n Livros no banco ")
for codigo, titulo, autor, ano in cursor.fetchall():
    print(f"{codigo} - {titulo} - {autor} ({ano})")

conexao.close()
print("Conexão fechada.")

