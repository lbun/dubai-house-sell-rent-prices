{{ 
    config(
        materialized='table',
        schema='silver'
        ) 
}}

with sales_contracts as (

    select 
        area_name_en,
        instance_date,
        CAST(strftime(instance_date, '%Y') AS INTEGER) AS year,
        strftime(instance_date, '%Y%m') AS year_month,
        strftime(instance_date, '%Y%m%d') AS year_month_day,
        CAST(strftime(instance_date, '%m') AS INTEGER) AS month,
        reg_type_en,
        meter_sale_price,
        property_type_en,
        property_usage_en,
        area_id,
        nearest_landmark_en
    from {{ source('dubai_housing', 'sale_contracts')}}
    where strftime(instance_date, '%Y%m') < strftime(current_timestamp, '%Y%m')
)

select *
from sales_contracts
