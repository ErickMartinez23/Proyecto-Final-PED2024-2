import pandas as pd
import re # para encontrar coincidencias 
import logging

# Configurar logging, monitoreo de la ejecucion del programa se vera en rojo en la consola
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Diccionario para traducir meses
MONTHS = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12",
    "january": "01", "february": "02", "march": "03", "april": "04",
    "may": "05", "june": "06", "july": "07", "august": "08",
    "september": "09", "october": "10", "november": "11", "december": "12"
}

def Transformar_fecha(date_str):
    try:
        formatos = [
            r"(\d{1,2}) de (\w+) de (\d{4})",  # "1 de enero de 2021"
            r"(\d{4})-(\d{2})-(\d{2})",  # "2021-01-01"
            r"(\d{2})/(\d{2})/(\d{4})"  # "01/01/2021"
        ]

        for formato in formatos: 
            match = re.match(formato, date_str.lower())
            if match:
                if len(match.groups()) == 3:
                    if formato == r"(\d{1,2}) de (\w+) de (\d{4})":
                        day, month, year = match.groups()
                        month = MONTHS.get(month, "01")
                    elif formato == r"(\d{4})-(\d{2})-(\d{2})":
                        year, month, day = match.groups()
                    else:  # "DD/MM/YYYY"
                        day, month, year = match.groups()
                    return f"{int(day):02d}/{int(month):02d}/{year}"

        logging.warning(f"Formato de fecha no reconocido: {date_str}")
        return date_str
    except Exception as e:
        logging.error(f"Error al normalizar la fecha {date_str}: {e}")
        return date_str


def Transofrmar_temp(temp):
    if pd.isna(temp) or temp == 'Desconocida':
        return None
    try:
        # aqui se convierte los grados farenheit a celcius en formato int
        fahrenheit = int(re.sub(r"\D", "", str(temp)))
        celsius = round((fahrenheit - 32) * 5 / 9)
        return celsius
    except ValueError:
        logging.warning(f"No se pudo convertir la temperatura a entero: {temp}")
        return None


def EliminarDuplis(df):
    # Elimina por completo las filas duplicadas del DataFrame y las filas con fechas duplicadas.

    rows_before = len(df)

    # Eliminar filas completamente duplicadas
    df_sin_duplicados = df.drop_duplicates(keep=False)

    # Eliminar filas con fechas duplicadas, manteniendo la primera ocurrencia
    df_sin_duplicados = df_sin_duplicados.drop_duplicates(subset=['Fecha'], keep='first')

    rows_after = len(df_sin_duplicados)
    duplicates_removed = rows_before - rows_after
    logging.info(f"Filas eliminadas (duplicados completos y fechas duplicadas): {duplicates_removed}")
    return df_sin_duplicados

def Ordenar_fechas_por_mes(data):
    try:
        data['Fecha'] = pd.to_datetime(data['Fecha'], errors='coerce')
        data = data.dropna(subset=['Fecha'])
        data['Año'] = data['Fecha'].dt.year
        data['Mes'] = data['Fecha'].dt.month
        data = data.sort_values(by=['Año', 'Mes', 'Fecha'], ascending=[True, True, True])
        data = data.drop(columns=['Año', 'Mes'])
        return data
    except Exception as e:
        logging.error(f"Error al ordenar las fechas por mes: {e}")
        return data


def Proceso(eliminar_desconocidos=True):
    try:
        # Cargar el archivo CSV
        input_file = 'archivos/clima_tijuana.csv'
        logging.info(f"Cargando archivo: {input_file}")
        data = pd.read_csv(input_file)

        # Eliminar filas con datos vacíos
        rows_before = len(data)
        data.dropna(inplace=True)
        rows_after = len(data)
        logging.info(f"Filas eliminadas por datos vacíos: {rows_before - rows_after}")

        # Normalizar y transformar las fechas
        logging.info("Normalizando fechas...")
        data['Fecha'] = data['Fecha'].apply(Transformar_fecha)

        # Limpiar temperaturas
        logging.info("Limpiando temperaturas...")
        data['Temperatura Máxima'] = data['Temperatura Máxima'].apply(Transofrmar_temp)
        data['Temperatura Mínima'] = data['Temperatura Mínima'].apply(Transofrmar_temp)

        # Normalizar Condición Climática
        logging.info("Normalizando condición climática...")
        data['Condición Climática'] = data['Condición Climática'].str.strip().str.lower()

        if eliminar_desconocidos:
            # Eliminar filas con 'Desconocida' o 'desconocido'
            rows_before = len(data)
            data = data[~data.isin(['Desconocida', 'desconocido']).any(axis=1)]
            rows_after = len(data)
            logging.info(f"Filas eliminadas por contener 'Desconocida' o 'desconocido': {rows_before - rows_after}")

        # Eliminar filas duplicadas completamente y filas con fechas duplicadas
        data = EliminarDuplis(data)

        # Guardar el resultado limpio en un nuevo archivo
        cleaned_file_path = 'archivos/clima_tijuana_limpio.csv'
        data.to_csv(cleaned_file_path, index=False)
        logging.info(f"Archivo limpio guardado en: {cleaned_file_path}")

    except Exception as e:
        logging.error(f"Error en el procesamiento: {e}")


if __name__ == "__main__":
    # aqui se cambia el valor o true o false para omitir en el loggin los datos desconocidos
    eliminar_desconocidos = False
    Proceso(eliminar_desconocidos)
