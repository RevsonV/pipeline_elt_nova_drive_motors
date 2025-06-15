{{ config(materialized='view') }}

WITH raw_layer AS (
    SELECT
        id_cidades,
        INITCAP(cidade) AS nome_cidade,
        id_estados,
        data_inclusao,
        COALESCE(data_atualizacao, data_inclusao) AS data_atualizacao
    FROM {{ source('raw', 'cidades') }}
)

SELECT
    id_cidades,
    nome_cidade,
    id_estados,
    data_inclusao,
    data_atualizacao
FROM
    raw_layer