import psycopg2
import traceback

def test_psycopg2_connection():
    try:
        conn = psycopg2.connect("dbname=VeterinariaProyecto user=postgres password='root host=localhost")
        print("Conexión exitosa a la base de datos con psycopg2.")
        conn.close()
    except Exception as e:
        print(f"Error al conectar a la base de datos con psycopg2: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    test_psycopg2_connection()






