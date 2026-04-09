from google.cloud import bigquery

client = bigquery.Client(project="fred-the-cat-4")

# 2018 168.345.130
# 2019 166.265.772
# 2020 168.213.073
# 2021 160.195.327

ano_referencia = 2016  # vai até 2021
mes_competencia = 3

while mes_competencia <= 12:
    print(f"baixando ano {ano_referencia}, mes {mes_competencia}")

    query = f"""
        SELECT *
        FROM `basedosdados.br_cgu_beneficios_cidadao.bolsa_familia_pagamento`
        WHERE ano_referencia = {ano_referencia}
        AND mes_competencia = {mes_competencia};
    """

    df = client.query(query).to_dataframe()

    df.to_csv(
        f"data/bolsa_familia/dados_bigquery_{ano_referencia}_{mes_competencia}.csv",
        index=False,
    )

    mes_competencia += 1
