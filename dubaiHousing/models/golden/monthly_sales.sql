{{ 
    config(
        materialized='view',
        schema='golden'
        ) 
}}

select 
    area_id,
	area_name_en, 
	year_month, 
    count(*) as num_sales,
	median(meter_sale_price) AS median_meter_sale_price
from {{ ref('sales') }}
where year_month < strftime(current_timestamp, '%Y%m') and property_type_en in ('Villa', 'Unit')
group by area_id, area_name_en, year_month 
order by 3 desc