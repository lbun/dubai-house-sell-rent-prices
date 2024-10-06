{{ 
    config(
        materialized='table',
        schema='golden'
        ) 
}}

WITH monthly_sales_property AS (
    SELECT 
        year_month, 
        year, 
        month,
        property_type_en,
        COUNT(*) AS num_sales
    FROM {{ ref('sales') }}
    where year>2010 and property_type_en in ('Villa', 'Unit') and year_month < strftime(current_timestamp, '%Y%m')
    GROUP BY property_type_en, year_month, year, month
), 
all_sales as (
    SELECT
        year_month,
        year,
        month,
        --property_type_en,
        num_sales,
        SUM(num_sales) OVER (
            PARTITION BY property_type_en 
            ORDER BY year_month
            ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
        ) AS rolling_12_month_num_sales
    FROM monthly_sales_property
   ),
 villa_sales as (
   SELECT
        year_month,
        year,
        month,
        property_type_en,
        num_sales,
        SUM(num_sales) OVER (
            PARTITION BY property_type_en 
            ORDER BY year_month
            ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
        ) AS rolling_12_month_num_sales_villa
    FROM monthly_sales_property
    where property_type_en='Villa'
   ), 
   unit_sales as (
   	 SELECT
        year_month,
        year,
        month,
        property_type_en,
        num_sales,
        SUM(num_sales) OVER (
            PARTITION BY property_type_en 
            ORDER BY year_month
            ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
        ) AS rolling_12_month_num_sales_unit
    FROM monthly_sales_property
    where property_type_en='Unit'
   ),
monthly_sales_regtype as (
   SELECT 
        year_month, 
        year, 
        month,
        reg_type_en,
        COUNT(*) AS num_sales
    FROM main_silver.sales
    where year>2010 and property_type_en in ('Villa', 'Unit') and year_month < strftime(current_timestamp, '%Y%m')
    GROUP BY reg_type_en, year_month, year, month
),
offplan_sales as (
	SELECT
        year_month,
        year,
        month,
        reg_type_en,
        num_sales,
        SUM(num_sales) OVER (
            PARTITION BY reg_type_en 
            ORDER BY year_month
            ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
        ) AS rolling_12_month_num_sales_offplan
    FROM monthly_sales_regtype
    where reg_type_en='Off-Plan Properties'
),
existing_sales as (
	SELECT
        year_month,
        year,
        month,
        reg_type_en,
        num_sales,
        SUM(num_sales) OVER (
            PARTITION BY reg_type_en 
            ORDER BY year_month
            ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
        ) AS rolling_12_month_num_sales_existing
    FROM monthly_sales_regtype
    where reg_type_en='Existing Properties'
)
select 
	us.*,
	vs.rolling_12_month_num_sales_villa,
	os.rolling_12_month_num_sales_offplan,
	es.rolling_12_month_num_sales_existing,
	os.rolling_12_month_num_sales_offplan + es.rolling_12_month_num_sales_existing as total_sales
from unit_sales us
left join villa_sales vs on vs.year_month=us.year_month
left join offplan_sales os on os.year_month=us.year_month
left join existing_sales es on es.year_month=us.year_month