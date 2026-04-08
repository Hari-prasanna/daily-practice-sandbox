-- Write your PostgreSQL query statement below
WITH CTE AS
    (SELECT 
    d.name AS Department,
    e.name AS Employee, 
    e.salary AS Salary,
    RANK() OVER(PARTITION BY e.departmentId ORDER BY e.salary DESC) AS rnk
FROM Employee e
JOIN Department d
ON e.departmentId = d.id
)

SELECT Department, Employee, Salary
FROM CTE 
WHERE rnk = 1