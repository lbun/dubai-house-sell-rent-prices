{{ 
    config(
        materialized='table',
        schema='golden'
        ) 
}}

select 
    area_id,
	area_name_en, 
	ejari_property_sub_type_en,  
	year_month, 
    count(*) as num_contracts_started,
	median(annual_amount) AS median_annual_amount
from {{ ref('rents') }}
where year_month < strftime(current_timestamp, '%Y%m') 
group by area_id, area_name_en, ejari_property_sub_type_en, year_month 
order by 4 desc