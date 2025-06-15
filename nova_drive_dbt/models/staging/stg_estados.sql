{{ config(materialized='view') }}

WITH raw_layer AS (
    SELECT
        id_estados,
        UPPER(estado) AS estado,
        UPPER(sigla) AS sigla,
        data_inclusao,
        data_atualizacao
    FROM {{ source('raw', 'estados') }}
)

SELECT
    id_estados,
    estado,
    sigla,
    data_inclusao,
    data_atualizacao
FROM raw_layer