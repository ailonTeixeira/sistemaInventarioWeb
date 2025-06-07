
# Conecta ao banco de dados (cria o arquivo se não existir)
connection = sqlite3.connect('database.db')

# Abre o arquivo com o schema SQL
with open('schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()

print("Banco de dados inicializado com sucesso!")