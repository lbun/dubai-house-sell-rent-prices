{{ 
    config(
        materialized='view',
        schema='golden'
        ) 
}}

with all_sales as (
select 
    year_month, year, month, 'all' as property_type, count(*) as num_contracts  
from {{ ref('rents') }}
group by year_month, year, month
),
split_sales as (
select 
    year_month, year, month, property_type, count(*) as num_contracts 
from {{ ref('rents') }}
group by year_month, year, month, property_type
),
all_n_split_property as (
select * from split_sales
union 
select * from all_sales
)
select * from all_n_split_property