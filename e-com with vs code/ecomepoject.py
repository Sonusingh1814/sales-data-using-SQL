import pandas as pd
import mysql.connector
import os
import numpy as np


db=mysql.connector.connect(host='localhost',
                           username='root',
                           password='12345',
                           database='ecommerce')

cur=db.cursor()

query=""" select products.product_category AS product,

(sum(payments.payment_value)/(select sum(payment_value) from payments))*100 as avarage

from products join order_items
on products.product_id=order_items.product_id 
join payments 
on payments.order_id=order_items.order_id 
group by products.product_category order by avarage desc; """

query1="""select products.product_category, count(order_items.order_id),
avg(order_items.price)
from products join order_items 
on products.product_id=order_items.product_id
group by  products.product_category;"""

# Calculate the total revenue generated by each seller, and rank them by revenue.
query2=""" select sellers.seller_id,sum(payments.payment_value) as total_sell
from sellers join order_items 
on sellers.seller_id= order_items.seller_id 
join payments on order_items.order_id=payments.order_id
group by sellers.seller_id  order by  total_sell desc limit 5

"""


query3="""select  customer_id,order_purchase_timestamp, payment,
avg( payment) over(partition by customer_id order by order_purchase_timestamp rows between 2 preceding and current row) as moving_avg
from
(select orders.customer_id,orders.order_purchase_timestamp,  payments.payment_value as payment
from orders join payments
on orders.order_id =  payments.order_id)as a;"""
 
query4=""" select year_of_order,months, payment,sum(payment)
over(order by year_of_order,months )
from
(select year(orders.order_delivered_carrier_date) as year_of_order,
monthname(orders.order_delivered_carrier_date)as months,
round(sum(payments.payment_value))as payment
from orders join payments 
on orders.order_id=payments.order_id
group by  year_of_order, months order by year_of_order desc) as a """

query5="""
with a AS
(select year(orders.order_delivered_carrier_date) as year_of_order,

round(sum(payments.payment_value))as payment
from orders join payments 
on orders.order_id=payments.order_id
group by  year_of_order order by year_of_order desc)

select year_of_order,payment, ((payment-lag(payment, 1) over(order by year_of_order))/lag(payment, 1) over(order by year_of_order))*100   from a
"""

cur.execute(query5)

data=cur.fetchall()

k=pd.DataFrame(data,columns=["years","paymnet","lag"])

print(k)


