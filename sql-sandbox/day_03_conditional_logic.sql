/* =====================================================================
   DAY 3: The Transformation Engine (Conditional Logic & Aggregation)
   Concept: Using CASE WHEN to create new categories based on aggregated data.
   ===================================================================== */

-- THE CHALLENGE:
-- Calculate total 2024 spend (price * quantity) for ALL customers.
-- Categorize them as 'VIP' (> $10), 'Regular' ($0.01 - $10), or 'Inactive' ($0).

-- Learning: 
-- If Where is used then the bouncer filters the whole JOINED table which cause inner JOIN
-- Better filter the table first and join to see all the record from table A

-- Direct Approach

SELECT 
	c.customer_id,
	c.name,
	COALESCE(SUM(o.price * o.quantity), 0) AS total_2024_spend,
	CASE 
		WHEN COALESCE(SUM(o.price * o.quantity), 0) :: DECIMAL > 10 THEN 'VIP'
		WHEN COALESCE(SUM(o.price * o.quantity), 0) :: DECIMAL BETWEEN 0.01 AND 10 THEN 'Regular'
		ELSE 'Inactive'
	END AS customer_status	
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id
AND o.order_date >= '2024-01-01' -- filter the table B first and join the record with A to avoid inner JOiN trap
AND o.order_date <= '2024-12-31'
GROUP BY 1,2

-- Readable Approach

WITH purchased_2024 AS -- Using CTE foor better reading prefilter the table B first
	(SELECT customer_id,
		SUM(price * quantity) AS total_spent
	FROM orders
	WHERE order_date >= '2024-01-01'
	AND order_date <= '2024-12-31'
	GROUP BY 1)
	
SELECT 
	c.customer_id,
	c.name,
	COALESCE(p.total_spent,0) AS total_2024_spend,
	CASE 
		WHEN p.total_spent :: DECIMAL > 10 THEN 'VIP'
		WHEN p.total_spent :: DECIMAL BETWEEN 0.01 AND 10 THEN 'Regular'
		ELSE 'Inactive'
		END AS customer_status	
FROM customers c
LEFT JOIN purchased_2024 p -- Join the prefiltered table here
ON c.customer_id = p.customer_id
