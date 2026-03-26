import pandas as pd
import glob

arquivos = sorted(glob.glob("data/TO/vinculos_tocantins_*.csv"))

dfs = [pd.read_csv(f) for f in arquivos]

df_final = pd.concat(dfs, ignore_index=True)

df_final.to_csv("data/vinculos_tocantins_2020.csv", index=False)
