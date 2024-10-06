{{ 
    config(
        materialized='table',
        schema='golden'
        ) 
}}

with rent_by_month as (
select 
    area_id,
	area_name_en, 
	master_project_en,
	project_name_en,
	ejari_property_sub_type_en,  
	year_month,
	year,
	month,
    count(*) as num_contracts_started,
    COUNT(CASE 
         WHEN contract_reg_type_en = 'New' 
         THEN 1 
         ELSE NULL 
     END) AS new_contracts,
    COUNT(CASE 
         WHEN contract_reg_type_en = 'Renew' 
         THEN 1 
         ELSE NULL 
     END) AS renew_contracts,
     median(annual_amount) as median_annual_amount
from {{ ref('rent_projects') }}
where year_month < strftime(current_timestamp, '%Y%m') 
group by area_id, area_name_en, master_project_en, project_name_en, ejari_property_sub_type_en, year_month, year, month
)
select 
	current.area_id,
	current.area_name_en,
	current.ejari_property_sub_type_en,
	current.master_project_en, 
	current.project_name_en,
	current.year_month,
	current.year,
	current.month,
	current.new_contracts,
	current.renew_contracts,
	current.num_contracts_started as current_contract_started,
	previous.num_contracts_started as previous_contract_started,
	round(
		(current.num_contracts_started - previous.num_contracts_started)/previous.num_contracts_started * 100,
		1) as contracts_grotwh_perc,
	current.median_annual_amount as current_annual_amount,
	previous.median_annual_amount as previous_annual_amount,
	round(
		(current.median_annual_amount - previous.median_annual_amount)/previous.median_annual_amount * 100,
		1) as annual_amount_grotwh_perc,
from rent_by_month current
left join rent_by_month previous
	on current.year=previous.year and current.month=previous.month + 1
	or (current.year=previous.year + 1) and current.month = 1 and previous.month=12