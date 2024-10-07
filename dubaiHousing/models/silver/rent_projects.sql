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
        cast(strftime(contract_start_date, '%Y') as integer) AS year,
        strftime(contract_start_date, '%Y%m') AS year_month,
        strftime(contract_start_date, '%Y%m%d') AS year_month_day,
        cast(strftime(contract_start_date, '%m') as integer) AS month,
        ejari_property_sub_type_id,
        ejari_property_sub_type_en,
        contract_reg_type_en, --new or renewal
        project_name_en,
        master_project_en, -- area of Dubai
        annual_amount
    from {{ source('dubai_housing', 'rent_contracts') }}
    where strftime(contract_start_date, '%Y%m') < strftime(current_timestamp, '%Y%m') and project_name_en is not null and property_usage_en = 'Residential' 
    and tenant_type_en = 'Person' and 
    master_project_en is not null and ejari_property_sub_type_id in 
	('11', '1', '2', '3') --, '4', '5', '6', '7', '8', '9', '35', '170501486', ) 
)

select *
from sales_contracts