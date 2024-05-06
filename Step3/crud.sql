--CUSTOMERS

-- Get All customers for Browse Customer Page
SELECT * FROM Customers;

-- Add new Customer
INSERT INTO Customers (FirstName, LastName, Email)
VALUES (:FirstNameInput, :LastNameInput, :EmailInput);

-- Delete A Customer
DELETE FROM Customers WHERE ID = :CID_selected_from_browse_customers_page

--ORDERS

-- Get All Orders and the customer name  For Browse Orders Page
SELECT Orders.ID, Date, CONCAT(Customers.FirstName, ' ', Customers.LastName) AS FullName
FROM Orders
    INNER JOIN Customers
    ON CID = Customers.ID;

-- Show All OrderDetails and show Order Id, Book Title, and Unit Price
SELECT OrderDetails.OID, Books.title, OrderDetails.UnitPrice
    FROM OrderDetails
        INNER JOIN Books ON OrderDetails.BookISBN = Books.ISBN
        ORDER BY OrderDetails.OID, Books.title;


--ORDER DETAILS

-- Show Invoice Slip Data (Filtered by Order, Currently showing OID = 1)
-- Header 
SELECT Orders.ID, CONCAT(Customers.FirstName, ' ', Customers.LastName) AS FullName, CURDATE() AS CurrentDate, Orders.TotalPrice
    FROM Customers
        INNER JOIN Orders ON Customers.ID = Orders.CID
        WHERE Orders.ID = 1;
-- Body
SELECT Books.ISBN, Books.Title, OrderDetails.LineTotal, OrderDetails.OrderQty, OrderDetails.UnitPrice
    FROM OrderDetails
        INNER JOIN Books ON OrderDetails.BookISBN = Books.ISBN
        WHERE OrderDetails.OID = 1;