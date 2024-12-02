import requests
import pandas as pd
import pyodbc

# Función para extraer los datos de la API
def extract_weather_data():
    # Solicitar al usuario la ciudad
    city = str(input("Ingresa Ciudad: "))  
    
    # Crear la URL para la solicitud a la API de OpenWeather
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=4bd8caf1606847f52fe184ccd4076ce9"
    
    # Realizar la solicitud GET a la API
    response = requests.get(url)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Retornar los datos en formato JSON
        return response.json()
    else:
        print(f"Error al obtener los datos para {city}. Código de error: {response.status_code}")
        return None

# Función para transformar los datos
def transform_weather_data(data):
    # Convertir los datos extraídos en un DataFrame para visualizarlos mejor
    weather_data = {
        "Ciudad": [data["name"]],
        "Temperatura (°C)": [data["main"]["temp"] - 273.15],  # Convertimos de Kelvin a Celsius
        "Descripción": [data["weather"][0]["description"]],
        "Humedad (%)": [data["main"]["humidity"]],
        "Viento (m/s)": [data["wind"]["speed"]],
        "Presión (hPa)": [data["main"]["pressure"]],
        "Latitud": [data["coord"]["lat"]],
        "Longitud": [data["coord"]["lon"]]
    }

    # Convertir el diccionario en un DataFrame de pandas
    df = pd.DataFrame(weather_data)
    
    return df

# Función para cargar los datos en SQL Server
def insert_weather_data_to_sql(df):
    # Conexión a SQL Server
    conexion = pyodbc.connect('DRIVER={SQL Server};'
                               'SERVER=DESKTOP-7AGUG97;'  # Cambia esto si tu servidor está en una IP o tiene un nombre de instancia
                               'DATABASE=weather_db;'
                               'UID=santiago;'
                               'PWD=123')

    # Crear un cursor para insertar los datos
    cursor = conexion.cursor()

    # Insertar los datos del DataFrame en la tabla (asegúrate de que la tabla exista)
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO weather_table (Ciudad, Temperatura, Descripcion, Humedad, Viento, Presion, Latitud, Longitud)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, row['Ciudad'], row['Temperatura (°C)'], row['Descripción'], row['Humedad (%)'], 
           row['Viento (m/s)'], row['Presión (hPa)'], row['Latitud'], row['Longitud'])
    
    # Confirmar los cambios y cerrar la conexión
    conexion.commit()
    cursor.close()
    conexion.close()

# Proceso ETL
def etl_process():
    print("Extrayendo datos...")
    data = extract_weather_data()

    if data:
        print("\nDatos extraídos correctamente:")
        print(data)  # Imprimir los datos crudos obtenidos de la API
        
        print("\nTransformando los datos...")
        # Transformar los datos
        df = transform_weather_data(data)

        print("\nDatos en formato DataFrame:")
        print(df)

        print("\nCargando los datos a la base de datos...")
        # Insertar los datos en SQL Server
        insert_weather_data_to_sql(df)
        print("¡Datos cargados con éxito en la base de datos!")
    else:
        print("No se pudieron extraer los datos.")

# Ejecutar el proceso ETL
etl_process()