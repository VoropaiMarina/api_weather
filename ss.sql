select c.customer_id, o.order_id 
from dim_customer c 
    left join fact_order o 
    using (customer_id)
where
    o.order_id is null;



select customer_id, order_id
  from (
      select customer_id,
             order_id,
             row_number() over (partition by customer_id order by amount desc) as rating_order
      from dim_customer  
      left join fact_order  
      using (customer_id)
      order by customer_id, rating_order
  ) counted_order
  where rating_order <= 3;