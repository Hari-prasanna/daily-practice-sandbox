
--🏋️ Exercise 1: The "First Impression" (INNER JOIN + Aggregation)
--The Concept: The "First Action" pattern. In interviews, you will constantly be asked to find what a user did on their very first day.
--The Scenario: The Product team wants to know exactly which coffee people buy on their very first visit, to understand what draws people in.

-- My way --
WITH rnk_customers AS 
(SELECT 
	c.customer_id, c.name , o.order_date, o.product,
	ROW_NUMBER() OVER (PARTITION BY c.customer_id ORDER BY o.order_date ASC) AS rnk
FROM customers c 
JOIN orders o 
ON c.customer_id = o.customer_id)


SELECT
	customer_id,
	name,
	order_date,
	product
FROM rnk_customers
WHERE rnk = 1

-- suggested JOIN approach --

WITH first_order AS 
	(SELECT customer_id, MIN(order_date) AS first_order
	FROM orders
	GROUP BY 1),
	
	
customers_first_order AS 
	(SELECT f.customer_id, c.name, f.first_order
	FROM customers c 
	JOIN first_order f
	ON c.customer_id = f.customer_id)


SELECT cf.*, o.product
FROM customers_first_order cf
JOIN orders o
ON cf.first_order = o.order_date
AND cf.customer_id = o.customer_id




--🏋️ Exercise 2: The Year-over-Year Reconciler (FULL OUTER JOIN)
--The Concept: Comparing two different time periods side-by-side.
--The Scenario: Finance is doing a YoY (Year-over-Year) audit for 2023 and 2024. They want a single report showing a customer's total spend in 2023 next to their total spend in 2024.


WITH total_spend_2023 AS 
(SELECT 
	customer_id,
	SUM(price * quantity) AS total_spend_2023
FROM orders 
WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31' 
GROUP BY 1),



total_spend_2024 AS 
(SELECT 
	customer_id,
	SUM(price * quantity) AS total_spend_2024
FROM orders 
WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31' 
GROUP BY 1)


SELECT 
	COALESCE(t1.customer_id,t2.customer_id,0) AS customer_id, -- 0 is given there is error to be fixed in the table 
	COALESCE(t1.total_spend_2023,0) AS total_spend_2023, 
	COALESCE(t2.total_spend_2024,0) AS total_spend_2024 
FROM total_spend_2023 t1
FULL OUTER JOIN total_spend_2024 t2
ON t1.customer_id = t2.customer_id




--🏋️ Exercise 3: The "Perfect Grid" (CROSS JOIN -> LEFT JOIN)
--The Concept: Forcing zero-fill reporting. Business dashboards (like Tableau or PowerBI) crash if data is simply "missing." You have to manufacture rows that say $0.
--The Scenario: The CEO wants a matrix. She wants to see every single customer and their total spend in every single year (2022, 2023, 2024, 2025, 2026), even if they hadn't signed up yet or didn't buy anything.


-- my way: suppose to be wrong for the context :(
WITH year_spend AS
(SELECT 
	customer_id,
	EXTRACT(YEAR FROM order_date) AS order_year,
	SUM(price * quantity) AS yearly_spend
FROM orders
GROUP BY customer_id, EXTRACT(YEAR FROM order_date))



SELECT c."name", y.order_year, COALESCE(y.yearly_spend,0) AS yearly_spend
FROM customers c 
LEFT JOIN year_spend y
ON c.customer_id = y.customer_id
ORDER BY order_year


-- Appropriate way

-- Step 1: Create a hardcoded list of the years we care about
WITH years AS (
    SELECT 2022 AS report_year UNION ALL
    SELECT 2023 UNION ALL
    SELECT 2024 UNION ALL
    SELECT 2025 UNION ALL
    SELECT 2026
),

-- Step 2: The CROSS JOIN (The Skeleton Grid)
-- This multiplies 10 customers x 5 years = exactly 50 rows.
-- Everyone gets 5 rows, guaranteed.
skeleton_grid AS (
    SELECT 
        c.customer_id, 
        c.name, 
        y.report_year
    FROM customers c
    CROSS JOIN years y 
),

-- Step 3: Your exact aggregation logic
year_spend AS (
    SELECT 
        customer_id,
        EXTRACT(YEAR FROM order_date) AS order_year,
        SUM(price * quantity) AS yearly_spend
    FROM orders
    GROUP BY customer_id, EXTRACT(YEAR FROM order_date)
)

-- Step 4: LEFT JOIN the sales onto the guaranteed Skeleton Grid
SELECT 
    grid.name, 
    grid.report_year, 
    COALESCE(ys.yearly_spend, 0) AS yearly_spend
FROM skeleton_grid grid
LEFT JOIN year_spend ys
    ON grid.customer_id = ys.customer_id 
    AND grid.report_year = ys.order_year
ORDER BY 
    grid.name, 
    grid.report_year;