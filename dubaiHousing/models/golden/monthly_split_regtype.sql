{{ 
    config(
        materialized='view',
        schema='golden'
        ) 
}}

with all_sales as (
select 
    year_month, year, month, 'all' as contract_reg_type_en, count(*) as num_contracts  
from {{ ref('rents') }}
group by year_month, year, month
),
split_sales as (
select 
    year_month, year, month, contract_reg_type_en, count(*) as num_contracts 
from {{ ref('rents') }}
group by year_month, year, month, contract_reg_type_en
),
all_n_split_reg_type as (
select * from split_sales
union 
select * from all_sales
)
select * from all_n_split_reg_type