{{ config(materialized='view') }}

WITH raw_layer AS (
    SELECT
        id_veiculos,
        nome,
        tipo,
        ROUND(CAST(valor AS NUMERIC), 2) AS valor,
        COALESCE(data_atualizacao, CURRENT_TIMESTAMP()) AS data_atualizacao,
        data_inclusao
    FROM {{ source('raw', 'veiculos') }}
)

SELECT
    id_veiculos,
    nome,
    tipo,
    valor,
    data_atualizacao,
    data_inclusao
FROM raw_layer