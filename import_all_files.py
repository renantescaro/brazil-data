import os
import subprocess
from dotenv import load_dotenv

load_dotenv()


DATA_DIR = "data"
CONTAINER_NAME = "clickhouse-server"
CONTAINER_PATH = "/var/lib/clickhouse/user_files/vinculos.csv"
DB_PASSWORD = os.getenv("DB_PASSWORD")

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar: {command}\nErro: {e}")

def execute():
    if not os.path.exists(DATA_DIR):
        print(f"Diretorio {DATA_DIR} nao encontrado.")
        return

    files = [f for f in os.listdir(DATA_DIR) 
             if os.path.isfile(os.path.join(DATA_DIR, f)) 
             and f.startswith("vinculos_") 
             and f.endswith(".csv")]

    print(f"Encontrados {len(files)} arquivos para importar.")

    for file_name in files:
        local_path = os.path.join(DATA_DIR, file_name)
        
        print(f"--- Processando: {file_name} ---")

        copy_cmd = f'docker cp "{local_path}" {CONTAINER_NAME}:{CONTAINER_PATH}'
        run_command(copy_cmd)

        insert_cmd = (
            f'docker exec {CONTAINER_NAME} clickhouse-client '
            f'--password {DB_PASSWORD} '
            f'--query="INSERT INTO rais_vinculos FROM INFILE \'{CONTAINER_PATH}\' FORMAT CSVWithNames"'
        )
        run_command(insert_cmd)

        print(f"Finalizado: {file_name}\n")

if __name__ == "__main__":
    execute()
