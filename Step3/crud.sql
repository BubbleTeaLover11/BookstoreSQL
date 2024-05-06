-- Patrick Kim, William Chen
-- CS340
-- Date: 05/06/24

-- Get All customers for Browse Customer Page
SELECT * FROM Customers;

-- Add new Customer
INSERT INTO Customers (FirstName, LastName, Email)
VALUES (:FirstNameInput, :LastNameInput, :EmailInput);

-- Delete A Customer
DELETE FROM Customers WHERE ID = :CID_selected_from_browse_customers_page

-- Update a Customer
-- No update to CID at the moment
-- Update based on ID
UPDATE Customers
SET FirstName="Foo", LastName="Bar", Email="Foobar@gmail.com"
WHERE ID=1

---------------------------------------------------------
--ORDERS
-- Get All Orders and the customer name  For Browse Orders Page
SELECT Orders.ID, Date, CONCAT(Customers.FirstName, ' ', Customers.LastName) AS FullName
FROM Orders
    INNER JOIN Customers
    ON CID = Customers.ID;

---------------------------------------------------------
--ORDER DETAILS
-- Show All OrderDetails and show Order Id, Book Title, and Unit Price
SELECT OrderDetails.OID, Books.title, OrderDetails.UnitPrice
    FROM OrderDetails
        INNER JOIN Books ON OrderDetails.BookISBN = Books.ISBN
        ORDER BY OrderDetails.OID, Books.title;

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

-- Update Order Details
-- Subquery to retrieve book ID and Order ID
UPDATE OrderDetails
SET BookISBN=(SELECT ID FROM Books WHERE ID=2), OID=(SELECT ID FROM Orders WHERE ID=1), OrderQty=2, UnitPrice=2, LineTotal=OrderQty*UnitPrice
WHERE ID=1;
-- Authors
-- Getting Authors
SELECT * FROM Authors;

-- Create Author
INSERT INTO Authors (FirstName, LastName, Gender)
VALUES (:FirstNameInput, :LastNameInput, :GenderInput);

-- Books
-- Getting Books
-- Example of grabbing ISBN 1
SELECT Books.ISBN AS ISBN, Books.Title AS Title, Books.Genre AS Genre, Books.Stock AS Stock, Books.Price AS Price, Author.FirstName, Author.LastName, Publishers.Company 
    FROM Books
        INNER JOIN Authors ON Authors.ID = Books.AID
        INNER JOIN Publishers ON Publishers.ID = Books.PID
        WHERE Books.ISBN = 1
ORDER BY Books.ISBN desc;

-- Create Book
INSERT INTO Books (Title, Genre, Stock, Price, AID, PID)
VALUES (:Title, :Genre, :Stock, :Price, (SELECT ID FROM Author WHERE FirstName = "Foo" and LastName = "Bar"), (SELECT ID FROM Publishers WHERE Company = "Foo"));

-- Publishers
-- Getting Authors
SELECT * FROM Publishers;

-- Create Publisher
INSERT INTO Publishers (Company, Year)
VALUES (:CompanyInput, :YearInput);