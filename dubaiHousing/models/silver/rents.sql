{{ 
    config(
        materialized='table',
        schema='silver'
        ) 
}}

with sales_contracts as (
    select 
        area_id,
        area_name_en, 
        contract_start_date,
        CAST(strftime(contract_start_date, '%Y') as integer) AS year,
        strftime(contract_start_date, '%Y%m') AS year_month,
        strftime(contract_start_date, '%Y%m%d') AS year_month_day,
        cast(strftime(contract_start_date, '%m') as integer) AS month,
        ejari_property_sub_type_id,
        ejari_property_sub_type_en,
        annual_amount,
        nearest_landmark_en
    from {{ source('dubai_housing', 'rent_contracts') }}
    where ejari_property_sub_type_id in 
	('11', '1', '2', '3') --, '4', '5', '6', '7', '8', '9', '35', '170501486', ) -- Studio, 1-9 Bed, Duplex, 2Beds + Maid
)

select *
from sales_contracts
