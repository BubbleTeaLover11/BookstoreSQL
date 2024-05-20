-- Patrick Kim, William Chen
-- CS340
-- Date: 05/06/24

---------------------------------------------------------
-- CUSTOMERS
-- Get All customers for Browse Customer Page
SELECT FirstName AS First Name, LastName AS Last Name, Email AS E-mail FROM Customers;

-- Add new Customer
INSERT INTO Customers (FirstName, LastName, Email)
VALUES (:FirstNameInput, :LastNameInput, :EmailInput);

-- Delete A Customer
DELETE FROM Customers WHERE ID = :CustomerIDfromDropDown;

-- Update a Customer
-- No update to CID at the moment
-- Update based on ID
UPDATE Customers
SET FirstName="Foo", LastName="Bar", Email="Foobar@gmail.com"
WHERE ID = :CustomerIDfromDropDown;

---------------------------------------------------------
--ORDERS
-- Get All Orders and the customer name  For Browse Orders Page
SELECT Orders.ID AS OrderID, Date, CID as Customer ID
FROM Orders
    INNER JOIN Customers
    ON CID = Customers.ID;

-- Add New Order
INSERT INTO Orders (Date, CID)
VALUES (:DateInput, :CustomerIDfromDropDown)

---------------------------------------------------------
--ORDER DETAILS
-- Show All OrderDetails and show Order Id, Book Title, and Unit Price
SELECT Books.ISBN, OrderDetails.OID, OrderDetails.OrderQty AS Order Quantity, OrderDetails.UnitPrice AS Unit Price, (Unit Price * Quantity) AS LineTotal
    FROM OrderDetails
        INNER JOIN Books ON OrderDetails.BookISBN = Books.ISBN
        ORDER BY OrderDetails.OID, Books.ISBN;

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

-- Associate a Book with an Order (M:M addition)
INSERT INTO OrderDetails (BookISBN, OID, OrderQty, UnitPrice, LineTotal)
    VALUES (:book_ISBN_selected_from_Order_details_list, :order_ID_selected_from_Order_details_list, :OrderQtyInput, 
    (SELECT Price AS Uprice FROM Books WHERE :book_ISBN_selected_from_Order_details_list = ISBN) , :OrderQtyIpnut*Uprice)

-- Update Order Details
-- Subquery to retrieve book ID and Order ID
UPDATE OrderDetails
SET BookISBN=(SELECT ISBN FROM Books WHERE ID=2), OID=(SELECT ID FROM Orders WHERE ID=1), OrderQty=2, UnitPrice=2, LineTotal=OrderQty*UnitPrice
WHERE ID=1;

-- Dissassociate an Book from an Order (M:M deletion)
DELETE FROM OrderDetails
WHERE BookISBN = :book_ISBN_selected_from_Order_details_list AND OID = :order_ID_selected_from_Order_details_list;

---------------------------------------------------------
-- AUTHORS
-- Getting Authors
SELECT ID AS Author ID, FirstName as First Name, LastName as Last Name, Gender FROM Authors;

-- Create Author
INSERT INTO Authors (FirstName, LastName, Gender)
VALUES (:FirstNameInput, :LastNameInput, :GenderInput);

---------------------------------------------------------
-- BOOKS
-- Getting Books
-- Example of grabbing ISBN 1
SELECT Books.ISBN AS ISBN, Books.Title AS Title, Books.Genre AS Genre, Books.Stock AS Stock, Books.Price AS Price, CONCAT(Author.FirstName, '', Author.LastName) Publishers.Company AS Publisher
    FROM Books
        INNER JOIN Authors ON Authors.ID = Books.AID
        INNER JOIN Publishers ON Publishers.ID = Books.PID
    WHERE Books.ISBN = 1;

-- Create Book
INSERT INTO Books (Title, Genre, Stock, Price, AID, PID)
VALUES (:TitleInput, :GenreInput, :StockInput, :PriceInput, (SELECT ID FROM Author WHERE FirstName = "Foo" and LastName = "Bar"), (SELECT ID FROM Publishers WHERE Company = "Foo"));

---------------------------------------------------------
-- PUBLISHERS
-- Getting Publishers
SELECT ID AS Publisher ID, Company, Year as Year Founded  FROM Publishers;

-- Create Publisher
INSERT INTO Publishers (Company, Year)
VALUES (:CompanyInput, :YearInput);
