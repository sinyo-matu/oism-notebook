#! /bin/bash
DB_NAME=oism-data.db
sqlite3 $DB_NAME "drop table if exists ph_items;"    
sqlite3 --csv $DB_NAME ".import items.csv ph_items"    
sqlite3 $DB_NAME "drop table if exists order_items;"    
sqlite3 --csv $DB_NAME ".import order_items.csv order_items"    
sqlite3 $DB_NAME "drop view if exists sales_info"
sqlite3 $DB_NAME "create view sales_info as select id, customer_id,item_code_ext,order_datetime,rate,status,item_name,label,material,price from order_items inner join ph_items on substr(item_code_ext,1,11) = ph_items.code;"