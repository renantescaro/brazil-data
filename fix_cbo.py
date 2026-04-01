import pandas as pd
import os


def fix_cbo(input_path, output_path):
    print(f"Lendo o arquivo: {input_path}...")

    df = pd.read_csv(input_path, dtype={"cbo_2002": str})

    df["cbo_2002"] = df["cbo_2002"].str.replace(r"\.0$", "", regex=True).str.zfill(6)

    print(f"Salvando arquivo tratado em: {output_path}...")
    df.to_csv(output_path, index=False)
    print("Processo concluído com sucesso!")


if __name__ == "__main__":
    input_file = r"data\vinculos_sao_paulo_2020.csv"
    output_file = r"data\vinculos_sao_paulo_2020_2.csv"

    if os.path.exists(input_file):
        fix_cbo(input_file, output_file)
    else:
        print(f"Erro: O arquivo {input_file} não foi encontrado.")
