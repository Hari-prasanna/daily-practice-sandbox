/* =====================================================================
   DAY 2: Relational Assembly (The Anti-Join)
   Concept: Finding records that exist in one table but NOT the other.
   ===================================================================== */

-- THE CHALLENGE:
-- The marketing team wants a "We Miss You" campaign for customers 
-- who registered but have NEVER placed an order.

-- MY EXPLANATION:
-- We use a LEFT JOIN to keep all customers, regardless of if they have 
-- an order. Customers without orders will have NULL values in the order 
-- columns. Then, we use the WHERE clause (The Bouncer) to filter OUT 
-- anyone who actually has an order_id.

-- THE SOLUTION:
SELECT 
    c.name, 
    c.email
FROM 
    customers c
LEFT JOIN 
    orders o ON c.customer_id = o.customer_id
WHERE 
    o.order_id IS NULL; --bouncer only allows the customer who don't have placed any order