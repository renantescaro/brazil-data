1. Criar o Container Docker, roda o servidor com senha definida e limites de arquivos.

```cmd
docker run -d --name clickhouse-server -p 8123:8123 -p 9000:9000 --ulimit nofile=262144:262144 -e CLICKHOUSE_PASSWORD=sua_senha clickhouse/clickhouse-server
```

2. Configurar Tabelas, acesse o terminal do ClickHouse:

```cmd
docker exec -it clickhouse-server clickhouse-client --password sua_senha
```

Dentro do ClickHouse, execute a criação das tabelas:

```sql
CREATE TABLE rais_vinculos (
    ano UInt16,
    sigla_uf LowCardinality(String),
    id_municipio FixedString(7),
    cbo_2002 String,
    cnae_2 FixedString(5),
    sexo Enum8('1' = 1, '2' = 2),
    raca_cor LowCardinality(String),
    grau_instrucao_apos_2005 LowCardinality(String),
    tamanho_estabelecimento LowCardinality(String),
    idade UInt8,
    valor_remuneracao_media Float32
) ENGINE = MergeTree()
ORDER BY (sigla_uf, cbo_2002, ano);

CREATE TABLE cbo_nomes (
    cbo_2002 String,
    descricao String
) ENGINE = TinyLog();

CREATE TABLE bolsa_familia (
    ano_competencia UInt16,
    mes_competencia UInt8,
    ano_referencia UInt16,
    mes_referencia UInt8,
    id_municipio UInt32,
    sigla_uf LowCardinality(String),
    cpf_favorecido String,
    nis_favorecido String,
    nome_favorecido String,
    valor_parcela Float32
)
ENGINE = MergeTree
PARTITION BY ano_competencia
ORDER BY (sigla_uf, id_municipio, nis_favorecido)
SETTINGS index_granularity = 8192;
```

3. Preparar e Importar Dados, saia do ClickHouse (exit) e execute no terminal do Windows:

A. Mover arquivos para a pasta segura do ClickHouse, isso evita erros de DATABASE_ACCESS_DENIED.

```cmd
docker exec -it clickhouse-server mkdir -p /var/lib/clickhouse/user_files
docker cp "data\vinculos_acre_2020.csv" clickhouse-server:/var/lib/clickhouse/user_files/vinculos.csv
docker cp "data\infos\cbo_2002.csv" clickhouse-server:/var/lib/clickhouse/user_files/cbo.csv
```

B. Importar RAIS (Vínculos)

```cmd
docker exec -it clickhouse-server clickhouse-client --password sua_senha --query="INSERT INTO rais_vinculos FROM INFILE '/var/lib/clickhouse/user_files/vinculos.csv' FORMAT CSVWithNames"
```

C. Importar CBO (Nomes)
Este comando limpa espaços extras e ignora colunas desnecessárias do CSV original.

```cmd
docker exec -it clickhouse-server clickhouse-client --password sua_senha --input_format_skip_unknown_fields=1 --query="INSERT INTO cbo_nomes SELECT trim(cbo_2002), trim(descricao) FROM file('cbo.csv', 'CSVWithNames', 'cbo_2002 String, descricao String')"
```

4. Caso precise corrigir permissões de pastas internas:

```cmd
docker exec -u 0 -it clickhouse-server chown -R clickhouse:clickhouse /var/lib/clickhouse
```
