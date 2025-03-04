from typing import Dict
from pandas import DataFrame
import sqlite3
import os
from extract import extract


def get_database_connection(db_name: str = "ecommerce.db") -> sqlite3.Connection:
    """Create and return a connection to the SQLite database.

    Args:
        db_name (str): The name of the SQLite database file.

    Returns:
        sqlite3.Connection: Una conexión SQLite válida.
    """
    db_path = os.path.abspath(db_name)  # Ruta absoluta para evitar errores
    connection = sqlite3.connect(db_path)  # 🔥 Conexión directa con sqlite3
    print(f"🔗 Conectado a la base de datos SQLite en {db_path}")
    return connection


def load(data_frames: Dict[str, DataFrame], database: sqlite3.Connection):
    """Load the dataframes into the SQLite database.

    Args:
        data_frames (Dict[str, DataFrame]): Diccionario con nombres de tablas y DataFrames.
        database (sqlite3.Connection): Conexión a SQLite.
    """
    cursor = database.cursor()
    for table_name, df in data_frames.items():
        if df.empty:
            print(
                f"⚠️ Tabla '{table_name}' está vacía. No se cargará en la base de datos.")
            continue

        print(f"Cargando tabla '{table_name}' con {df.shape[0]} filas...")

        # 🔥 Usar conexión SQLite en lugar de un objeto Engine
        df.to_sql(table_name, con=database, if_exists="replace", index=False)

        print(
            f"✅ Tabla '{table_name}' cargada correctamente en la base de datos.")

    database.commit()
    cursor.close()
    database.close()


if __name__ == "__main__":

    connection = get_database_connection()

    csv_folder = os.path.abspath("../dataset")
    csv_table_mapping = {
        "olist_customers_dataset.csv": "customers",
        "olist_geolocation_dataset.csv": "geolocation",
        "olist_order_items_dataset.csv": "order_items",
        "olist_order_payments_dataset.csv": "order_payments",
        "olist_order_reviews_dataset.csv": "order_reviews",
        "olist_orders_dataset.csv": "orders",
        "olist_products_dataset.csv": "products",
        "olist_sellers_dataset.csv": "sellers",
        "product_category_name_translation.csv": "product_category_translation",
        "public_holidays.csv": "public_holidays",
    }
    public_holidays_url = "https://date.nager.at/api/v3/publicholidays"

    data_frames = extract(csv_folder, csv_table_mapping, public_holidays_url)

    # Ejecutar la carga con los datos reales
    load(data_frames, connection)

    print("\n✅ Proceso de carga completado.")
