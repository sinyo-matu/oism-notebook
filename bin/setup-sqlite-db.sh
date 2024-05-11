#! /bin/bash
PROD_MONGODB_CONNECTION_URI="mongodb+srv://eliamo:64659027Qy@cluster0.k6d04.mongodb.net/?authSource=admin&replicaSet=atlas-e5y1lc-shard-0&readPreference=primary&ssl=true"
mongoexport --uri=$PROD_MONGODB_CONNECTION_URI --db=phitems --collection=items --fields="code,item_name,label,material,price" --type=csv --out="db_data/items.csv"
mongoexport --uri=$PROD_MONGODB_CONNECTION_URI --db=taobao --collection=order_items --fields="id,customer_id,item_code_ext,order_datetime,rate,status" --type=csv --out="db_data/order_items.csv"

DB_NAME=db_data/oism-data.db
sqlite3 $DB_NAME "drop table if exists ph_items;"    
sqlite3 --csv $DB_NAME ".import db_data/items.csv ph_items"    
sqlite3 $DB_NAME "drop table if exists order_items;"    
sqlite3 --csv $DB_NAME ".import db_data/order_items.csv order_items"    
sqlite3 $DB_NAME "drop view if exists sales_info"
sqlite3 $DB_NAME "create view sales_info as select id, customer_id,item_code_ext,order_datetime,rate,status,item_name,label,material,price from order_items inner join ph_items on substr(item_code_ext,1,11) = ph_items.code;"