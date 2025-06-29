{{ config(materialized='view') }}

WITH raw_layer AS (
    SELECT
        id_concessionarias,
        TRIM(concessionaria) AS nome_concessionaria, 
        id_cidades,
        data_inclusao,
        COALESCE(data_atualizacao, data_inclusao) AS data_atualizacao 
    FROM {{ source('raw', 'concessionarias') }}
)

SELECT
    id_concessionarias,
    nome_concessionaria,
    id_cidades,
    data_inclusao,
    data_atualizacao
FROM raw_layer