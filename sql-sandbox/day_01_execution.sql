/* =====================================================================
   DAY 1: Logical Order of Execution
   Concept: Why 'SELECT' aliases can't be used in 'WHERE' clauses.
   ===================================================================== */

-- THE CHALLENGE:
-- Find employees who have made more than 50 sales. 
-- Why does this junior code fail?
/*
   SELECT employee_id, COUNT(sale_id) AS total_sales
   FROM sales
   WHERE total_sales > 50
   GROUP BY employee_id;
*/


-- SOLUTION:
-- We must use HAVING to filter the groups.

SELECT 
    employee_id, 
    COUNT(sale_id) AS total_sales
FROM 
    sales
GROUP BY 
    employee_id 
HAVING
    COUNT(sale_id) > 50
ORDER BY 
    total_sales DESC;