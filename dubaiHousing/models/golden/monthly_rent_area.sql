{{ 
    config(
        materialized='table',
        schema='golden'
        ) 
}}

with monthly_data as (
select 
	year_month,
    area_id,
	area_name_en,
	ejari_property_sub_type_en,
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
    median(annual_amount) as median_month_amount
from {{ ref('rent_projects') }} 
where year_month < strftime(current_timestamp, '%Y%m') --and area_name_en = 'Marsa Dubai' and ejari_property_sub_type_en = 'Studio'
group by area_id, area_name_en, ejari_property_sub_type_en, year_month, year, month
),
rolling as (
	select 
		*, 
		sum(num_contracts_started) over (
	    partition by area_id, area_name_en, ejari_property_sub_type_en
	    order by year_month rows between 11 preceding and current row
	    ) as rolling_year_contracts,
	    sum(new_contracts) over (
	    partition by area_id, area_name_en, ejari_property_sub_type_en
	    order by year_month rows between 11 preceding and current row
	    ) as rolling_year_new_contracts,
	    sum(renew_contracts) over (
	    partition by area_id, area_name_en, ejari_property_sub_type_en
	    order by year_month rows between 11 preceding and current row
	    ) as rolling_year_renew_contracts,
	    round(AVG(median_month_amount) over (
	    partition by area_id, area_name_en, ejari_property_sub_type_en
	    order by year_month rows between 11 preceding and current row
	    ),0) as avg_median_annual_amount,
	from monthly_data
)
select 
	current.area_id,
	current.area_name_en,
	current.ejari_property_sub_type_en,
	current.year_month,
	current.year,
	current.month,
	current.rolling_year_new_contracts as rolling_month__year_new_contracts,
	current.rolling_year_renew_contracts as rolling_month__year_renew_contracts,
	current.rolling_year_contracts as current_month__yearly_contract_started,
	previous.rolling_year_contracts as previous_month__yearly_contract_started,
	round(current.rolling_year_new_contracts/current.rolling_year_contracts * 100, 1) as current_month__yearly_contracts_perc,
	round(
		(current.rolling_year_contracts - previous.rolling_year_contracts)/previous.rolling_year_contracts * 100,
		1) as month__yearly_contracts_grotwh_perc,
	current.avg_median_annual_amount as current_avg_monthly__yearly_median_amount,
	previous.avg_median_annual_amount as previous_avg_monthly__yearly_median_amount,
	round(
		(current.avg_median_annual_amount - previous.avg_median_annual_amount)/previous.avg_median_annual_amount * 100,
		1) as month__yearly_avg_amount_grotwh_perc
from rolling current
left join rolling previous
	on current.area_id=previous.area_id and current.ejari_property_sub_type_en=previous.ejari_property_sub_type_en and 
	(current.year=previous.year and current.month=previous.month + 1
	or (current.year=previous.year + 1) and current.month = 1 and previous.month=12)
