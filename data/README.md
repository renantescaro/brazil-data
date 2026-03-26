```sql
SELECT
    ano,
    sigla_uf,
    id_municipio,
    cbo_2002,
    cnae_2,
    sexo,
    raca_cor,
    grau_instrucao_apos_2005,
    tamanho_estabelecimento,
    tipo_vinculo,
    idade,
    quantidade_horas_contratadas,
    valor_remuneracao_media,
FROM `basedosdados.br_me_rais.microdados_vinculos`
WHERE ano > 2020
AND sigla_uf = 'AL'
AND valor_remuneracao_media > 0;
```
