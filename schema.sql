-- schema.sql
DROP TABLE IF EXISTS produtos;

CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    preco_unitario REAL NOT NULL,
    quantidade INTEGER NOT NULL
);