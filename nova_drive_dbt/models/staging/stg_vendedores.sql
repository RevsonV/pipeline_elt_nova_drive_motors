{{ config(materialized='view') }}

WITH raw_layer AS (
    SELECT
        id_vendedores,
        INITCAP(nome) AS nome_vendedor, 
        id_concessionarias,
        data_inclusao,
        COALESCE(data_atualizacao, data_inclusao) AS data_atualizacao 
    FROM {{ source('raw', 'vendedores') }}
)

SELECT
    id_vendedores,
    nome_vendedor,
    id_concessionarias,
    data_inclusao,
    data_atualizacao
FROM raw_layer