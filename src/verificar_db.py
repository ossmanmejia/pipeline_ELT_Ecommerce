import sqlite3

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# Verificar las tablas creadas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tablas en la base de datos:", cursor.fetchall())

# Mostrar los datos de cada tabla
for table in ["orders", "products"]:
    cursor.execute(f"SELECT * FROM {table};")
    print(f"\nDatos de la tabla {table}:")
    print(cursor.fetchall())

conn.close()
