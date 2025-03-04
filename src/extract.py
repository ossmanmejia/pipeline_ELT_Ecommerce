from typing import Dict
import requests
import os
from pandas import DataFrame, read_csv, to_datetime


def get_public_holidays(public_holidays_url: str, year: str) -> DataFrame:
    """Get the public holidays for the given year for Brazil.

    Args:
        public_holidays_url (str): URL to the public holidays.
        year (str): The year to get the public holidays for.

    Raises:
        SystemExit: If the request fails.

    Returns:
        DataFrame: A dataframe with the public holidays.
    """
    url = f"{public_holidays_url}/{year}/BR"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza error si la solicitud falla
        holidays_data = response.json()

        df_holidays = DataFrame(holidays_data)

        # Eliminar columnas innecesarias
        df_holidays.drop(columns=["types", "counties"],
                         errors="ignore", inplace=True)

        # Convertir la columna "date" a datetime
        df_holidays["date"] = to_datetime(df_holidays["date"])

        # Asegurar que la carpeta dataset/ existe
        dataset_folder = os.path.abspath("../dataset")
        os.makedirs(dataset_folder, exist_ok=True)

        # Guardar en un archivo CSV dentro de dataset/
        csv_path = os.path.join(dataset_folder, "public_holidays.csv")
        df_holidays.to_csv(csv_path, index=False)

        print(f"Días festivos guardados en {csv_path}")

        return df_holidays

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los días festivos: {e}")
        raise SystemExit(e)


def extract(
    csv_folder: str, csv_table_mapping: Dict[str, str], public_holidays_url: str
) -> Dict[str, DataFrame]:
    """Extract the data from the csv files and load them into the dataframes.

    Args:
        csv_folder (str): The path to the csv's folder.
        csv_table_mapping (Dict[str, str]): The mapping of the csv file names to the
        table names.
        public_holidays_url (str): The url to the public holidays.

    Returns:
        Dict[str, DataFrame]: A dictionary with keys as the table names and values as
        the dataframes.
    """
    dataframes = {
        table_name: read_csv(os.path.join(csv_folder, csv_file))
        for csv_file, table_name in csv_table_mapping.items()
    }

    # Extraer días festivos para el año 2017
    holidays = get_public_holidays(public_holidays_url, "2017")

    dataframes["public_holidays"] = holidays

    return dataframes


if __name__ == "__main__":
    # Definir parámetros de prueba
    csv_folder = os.path.abspath("../dataset")
    csv_table_mapping = {
        "olist_orders_dataset.csv": "orders",
        "olist_order_items_dataset.csv": "order_items",
        "olist_products_dataset.csv": "products"
    }
    public_holidays_url = "https://date.nager.at/api/v3/publicholidays"

    # Ejecutar la extracción
    dataframes = extract(csv_folder, csv_table_mapping, public_holidays_url)

    # Mostrar nombres de las tablas extraídas
    print("\nTablas extraídas:")
    for table_name, df in dataframes.items():
        print(f"- {table_name}: {df.shape[0]} filas")

    # Mostrar las primeras filas de los días festivos
    print("\nPrimeras filas de los días festivos extraídos:")
    print(dataframes["public_holidays"].head())
