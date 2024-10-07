{{ 
    config(
        materialized='table',
        schema='golden'
        ) 
}}

select 
    area_id,
	area_name_en, 
	reg_type_en,
	property_type_en,  
	year_month, count(*) as num_sales,
	median(meter_sale_price) AS median_meter_sale_price
from {{ ref('sales')}}
where property_type_en in ('Villa', 'Unit')
group by area_id, area_name_en, reg_type_en, property_type_en,  year_month 
order by 5 desc