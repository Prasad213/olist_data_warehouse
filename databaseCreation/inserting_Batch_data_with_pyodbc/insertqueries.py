
#for pyodbc single inserts using crsr 
olist_geolocation_dataset="""INSERT INTO geolocation (geolocation_zip_code_prefix,geolocation_lat,geolocation_lng,geolocation_city,geolocation_state) VALUES (?,?,?,?,?) """
olist_customers_dataset="""INSERT INTO customers (customer_id,customer_unique_id,customer_zip_code_prefix,customer_city,customer_state) VALUES (?,?,?,?,?)"""
olist_orders_dataset="""INSERT INTO orders (order_id,customer_id,order_status,order_purchase_timestamp,order_approved_at,order_delivered_carrier_date,order_delivered_customer_date,order_estimated_delivery_date) VALUES (?,?,?,?,?,?,?,?)"""
olist_products_dataset="""INSERT INTO products (product_id,product_category_name,product_name_lenght,product_description_lenght,product_photos_qty,product_weight_g,product_length_cm,product_height_cm,product_width_cm) VALUES (?,?,?,?,?,?,?,?,?)"""
olist_sellers_dataset="""INSERT INTO sellers (seller_id,seller_zip_code_prefix,seller_city,seller_state) VALUES (?,?,?,?)"""
olist_order_items_dataset="""INSERT INTO order_items (order_id,order_item_id,product_id,seller_id,shipping_limit_date,price,freight_value) VALUES (?,?,?,?,?,?,?)"""
olist_order_payments_dataset="""INSERT INTO order_payments (order_id,payment_sequential,payment_type,payment_installments,payment_value) VALUES (?,?,?,?,?)"""
olist_order_reviews_dataset="""INSERT INTO order_reviews (review_id,order_id,review_score,review_comment_title,review_comment_message,review_creation_date,review_answer_timestamp) VALUES (?,?,?,?,?,?,?)"""
