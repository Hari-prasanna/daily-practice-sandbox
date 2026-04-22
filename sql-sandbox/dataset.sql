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
    (1,  'Emma Wilson',      'emma.w@mail.com',     'London',    '2024-01-15'),
    (2,  'Liam Chen',        'liam.c@mail.com',     'New York',  '2024-02-03'),
    (3,  'Sophia Rodriguez', 'sophia.r@mail.com',   'Madrid',    '2024-02-20'),
    (4,  'Noah Patel',       'noah.p@mail.com',     'Toronto',   '2024-03-11'),
    (5,  'Olivia Kim',       'olivia.k@mail.com',   'Seoul',     '2024-04-07'),
    (6,  'James Brown',      'james.b@mail.com',    'London',    '2024-05-19'),
    (7,  'Ava Müller',       'ava.m@mail.com',      'Berlin',    '2024-06-02'),
    (8,  'Ethan Johnson',    'ethan.j@mail.com',    'New York',  '2024-07-14'),
    (9,  'Isabella Rossi',   'isabella.r@mail.com', 'Rome',      '2024-08-25'),
    (10, 'Mason Garcia',     'mason.g@mail.com',    'Barcelona', '2024-09-30');
 
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
    (101, 1, 'Latte',            2, 4.50, '2024-10-01'),
    (102, 1, 'Blueberry Muffin', 1, 3.25, '2024-10-01'),
    (103, 2, 'Cappuccino',       1, 4.00, '2024-10-03'),
    (104, 4, 'Cold Brew',        3, 5.00, '2024-10-05'),
    (105, 4, 'Croissant',        2, 3.50, '2024-10-05'),
    (106, 5, 'Matcha Latte',     1, 5.25, '2024-10-08'),
    (107, 7, 'Espresso',         2, 3.00, '2024-10-10'),
    (108, 8, 'Flat White',       1, 4.25, '2024-10-12'),
    (109, 8, 'Chai Latte',       1, 4.75, '2024-10-12'),
    (110, 9, 'Americano',        2, 3.75, '2024-10-15'),
    (999, NULL, 'Walk-in Black Coffee', 1, 2.00, '2024-10-20'); -- systems break row for practice
 