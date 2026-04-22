-- =====================================================
-- Table 1: customers
-- =====================================================
CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    email         VARCHAR(100),
    city          VARCHAR(50),
    signup_date   DATE
);
 
INSERT INTO customers (customer_id, name, email, city, signup_date) VALUES
    (1,  'Emma Wilson',      'emma.w@mail.com',     'London',    '2022-01-15'),
    (2,  'Liam Chen',        'liam.c@mail.com',     'New York',  '2022-02-03'),
    (3,  'Sophia Rodriguez', 'sophia.r@mail.com',   'Madrid',    '2022-06-20'),
    (4,  'Noah Patel',       'noah.p@mail.com',     'Toronto',   '2023-03-11'),
    (5,  'Olivia Kim',       'olivia.k@mail.com',   'Seoul',     '2023-04-07'),
    (6,  'James Brown',      'james.b@mail.com',    'London',    '2023-05-19'),
    (7,  'Ava Müller',       'ava.m@mail.com',      'Berlin',    '2023-09-02'),
    (8,  'Ethan Johnson',    'ethan.j@mail.com',    'New York',  '2024-02-14'),
    (9,  'Isabella Rossi',   'isabella.r@mail.com', 'Rome',      '2024-08-25'),
    (10, 'Mason Garcia',     'mason.g@mail.com',    'Barcelona', '2025-01-30');

-- =====================================================
-- Table 2: orders
-- =====================================================
CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER,
    product      VARCHAR(50),
    quantity     INTEGER,
    price        DECIMAL(6,2),
    order_date   DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
 
INSERT INTO orders (order_id, customer_id, product, quantity, price, order_date) VALUES
    -- 2022
    (101, 1, 'Latte',            2, 4.50, '2022-02-10'),
    (102, 2, 'Cappuccino',       1, 4.00, '2022-03-15'),
    (103, 1, 'Blueberry Muffin', 1, 3.25, '2022-11-05'),
    -- 2023
    (104, 2, 'Americano',        2, 3.75, '2023-01-20'),
    (105, 1, 'Cappuccino',       1, 4.00, '2023-03-22'),
    (106, 4, 'Cold Brew',        3, 5.00, '2023-04-05'),
    (107, 5, 'Matcha Latte',     1, 5.25, '2023-08-08'),
    (108, 7, 'Espresso',         2, 3.00, '2023-10-10'),
    (109, 4, 'Croissant',        2, 3.50, '2023-12-20'),
    -- 2024
    (110, 8, 'Flat White',       1, 4.25, '2024-03-12'),
    (111, 2, 'Espresso',         1, 3.00, '2024-06-11'),
    (112, 1, 'Cold Brew',        1, 5.00, '2024-07-18'),
    (113, 8, 'Chai Latte',       1, 4.75, '2024-09-15'),
    (114, 4, 'Mocha',            2, 4.80, '2024-10-05'),
    (115, 9, 'Americano',        2, 3.75, '2024-10-15'),
    (116, 5, 'Matcha Latte',     2, 5.25, '2024-11-22'),
    (117, 7, 'Macchiato',        1, 4.20, '2024-12-03'),
    -- 2025
    (118, 4, 'Flat White',       1, 4.25, '2025-05-14'),
    (119, 7, 'Espresso',         2, 3.00, '2025-06-18'),
    (120, 8, 'Americano',        3, 3.75, '2025-07-22'),
    (121, 2, 'Latte',            1, 4.50, '2025-09-04'),
    (122, 1, 'Latte',            2, 4.50, '2025-10-01'),
    (123, 9, 'Cappuccino',       1, 4.00, '2025-11-30'),
    -- 2026
    (124, 5, 'Chai Latte',       1, 4.75, '2026-01-10'),
    (125, 1, 'Croissant',        1, 3.50, '2026-02-14'),
	(999, NULL, 'Walk-in Black Coffee', 1, 2.00, '2024-10-20'); -- systems break row for practice
 