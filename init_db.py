import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Crea la tabla de usuarios con columnas adicionales para el código de verificación y el estado de verificación
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        verification_code INTEGER,
        verified BOOLEAN NOT NULL CHECK (verified IN (0, 1)) DEFAULT 0
    )
''')

connection.commit()
connection.close()