--only rent to visualize the number of growth of the rents by year
SELECT 
	area_name_en, 
	YEAR(contract_start_date),
	ejari_property_sub_type_en,
	count(*) as number_of_contracts,
	avg(annual_amount) as average_annual_rent
FROM dubai_housing.main.rent_contracts
where month(contract_start_date) not in (9, 10, 11, 12) 
	and YEAR(contract_start_date)>2020 
	and YEAR(contract_start_date)<=2024
	and ejari_property_sub_type_id is not null 
	and ejari_property_sub_type_id in ('11', '1', '2', '170501486', '3')
group by area_name_en, YEAR(contract_start_date), ejari_property_sub_type_en 
order by 1, 3, 2

--only sales to visualize the sales growth over the previous year
select area_name_en, reg_type_en, YEAR(instance_date), count(*) from dubai_housing.main.sale_contracts sc
where month(instance_date) not in (9, 10, 11, 12) 
	and YEAR(instance_date)>2020 
	and YEAR(instance_date)<=2024
group by area_name_en, YEAR(instance_date), reg_type_en
order by 1, 3, 2


-- joining landmark
with rent_l as (
select 
	case when nearest_landmark_en is null
		then 'no_landmark'
		else nearest_landmark_en
	 end as landmark, 
	count(*) as num_rent 
from dubai_housing.main.sale_contracts 
group by nearest_landmark_en
),
sale_l as (
select 
	case when nearest_landmark_en is null
	then 'no_landmark'
	else nearest_landmark_en
 end as landmark,
count(*) as num_sales
from dubai_housing.main.rent_contracts 
group by nearest_landmark_en
)
select 
	r.landmark,
	r.num_rent,
	s.num_sales 
from rent_l r
full join sale_l s on r.landmark=s.landmark


-- compare the area names
with rent as (
	SELECT
        area_id,
        area_name_en as area_name,
		YEAR(contract_start_date) as ytd,
		count(*) as number_of_contracts,
		avg(annual_amount) as average_annual_rent
	FROM dubai_housing.main.rent_contracts
	where month(contract_start_date) not in (9, 10, 11, 12) 
		and YEAR(contract_start_date)>2022
		and YEAR(contract_start_date)<=2024
		and ejari_property_sub_type_id is not null 
		and ejari_property_sub_type_id in ('11', '1', '2', '170501486', '3')
	group by area_id, area_name, ytd 
),
sales_existing_properties as (
	select
        area_id,
        area_name_en as area_name,
        YEAR(instance_date) as ytd,
		reg_type_en, 
		count(*) as num_sales, 
		avg(meter_sale_price) as avg_meter_sale_price
	from dubai_housing.main.sale_contracts sc
	where month(instance_date) not in (9, 10, 11, 12) 
		and YEAR(instance_date)>2022
		and YEAR(instance_date)<=2024
		and reg_type_en = 'Existing Properties'
        and property_type_en in ('Unit', 'Villa')
        and property_usage_en in ('Residential')
	group by area_id, area_name, ytd, reg_type_en
),
sales_offplan as (
	select 
        area_id,
        area_name_en as area_name,
		YEAR(instance_date) as ytd, 
		reg_type_en, 
		count(*) as num_sales, 
		avg(meter_sale_price) as avg_meter_sale_price
	from dubai_housing.main.sale_contracts sc
	where month(instance_date) not in (9, 10, 11, 12) 
		and YEAR(instance_date)>2022
		and YEAR(instance_date)<=2024
		and reg_type_en != 'Existing Properties'
        and property_type_en in ('Unit', 'Villa')
        and property_usage_en in ('Residential')
	group by area_id, area_name, ytd, (instance_date), reg_type_en
)
select 
	coalesce(r.area_name, se.area_name, so.area_name) as area_name,
    coalesce(r.ytd, se.ytd, so.ytd) as ytd,
	r.number_of_contracts as num_rent,
    se.num_sales + so.num_sales as total_sales,
    se.num_sales as num_sales_existing,
    so.num_sales as num_sales_offplan,
    (se.num_sales + so.num_sales) / r.number_of_contracts * 100 as sales_to_rent_ratio,
    so.num_sales/se.num_sales * 100 as sales_offplan_existing_ratio,
	r.average_annual_rent,
	se.avg_meter_sale_price as avg_meter_price_existing_properties,
	so.avg_meter_sale_price as avg_meter_price_offplan_properties
from rent r
full join sales_offplan so on so.area_id=r.area_id and so.ytd=r.ytd
full join sales_existing_properties se on se.area_id=r.area_id and se.ytd=r.ytd
order by 1,2

--aggregation
select 
	area_name, 
	sum(number_of_contracts) as num_contracts,
	sum(num_sales_existing_properties) as num_sales, 
	sum(num_sales_offplan_properties) as num_sales_offplan,
	avg(avg_meter_price_existing_properties) as meter_price,
	avg(avg_meter_price_offplan_properties) as meter_price_offplan
from summary 
where number_of_contracts > 300
group by area_name 
order by 6 desc