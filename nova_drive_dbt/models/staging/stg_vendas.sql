{{ config(materialized='view') }}

WITH raw_layer AS (
    SELECT
        id_vendas,
        id_veiculos,
        id_concessionarias,
        id_vendedores,
        id_clientes,
        ROUND(CAST(valor_pago AS NUMERIC),2) AS valor_venda, 
        data_venda,
        data_inclusao,
        COALESCE(data_atualizacao, data_venda) AS data_atualizacao
    FROM {{ source('raw', 'vendas') }}
)

SELECT
    id_vendas,
    id_veiculos,
    id_concessionarias,
    id_vendedores,
    id_clientes,
    valor_venda,
    data_venda,
    data_inclusao,
    data_atualizacao
FROM raw_layer