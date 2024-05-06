-- William Chen, Patrick Kim
-- CS 340
-- 5.1.2024

SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

/* --------------------- CREATE ------------------------ */

CREATE OR REPLACE TABLE `Authors` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `FirstName` VARCHAR(45) NOT NULL,
  `LastName` VARCHAR(45) NOT NULL,
  `Gender` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`),
  UNIQUE ('ID')
);

CREATE OR REPLACE TABLE `Publishers` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Company` VARCHAR(45) NOT NULL,
  `Year` INT NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE (`Company`)
);

-- DELETE AUTHOR and PUBLISHER if gone --
CREATE OR REPLACE TABLE `Books` (
  `ISBN` INT NOT NULL AUTO_INCREMENT,
  `Title` VARCHAR(50) NOT NULL,
  `Genre` VARCHAR(45) NOT NULL,
  `Stock` INT NOT NULL,
  `Price` DECIMAL(5,2) NULL,
  `AID` INT NOT NULL,
  `PID` INT NOT NULL,
  PRIMARY KEY (`ISBN`),
  UNIQUE (`Title`),
  CONSTRAINT `fk_book_author`
    FOREIGN KEY (`AID`)
    REFERENCES `Authors` (`ID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_book_publisher`
    FOREIGN KEY (`PID`)
    REFERENCES `Publishers` (`ID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
);

CREATE OR REPLACE TABLE `Customers` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `FirstName` VARCHAR(45) NOT NULL,
  `LastName` VARCHAR(45) NOT NULL,
  `Email` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE (`ID`),
  UNIQUE (`Email` ASC)
);

-- Want to set order customerID to NULL if updated --
CREATE OR REPLACE TABLE `Orders` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Date` DATETIME NOT NULL,
  `TotalPrice` DECIMAL(7,2) NOT NULL,
  `CID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_order_customer1`
    FOREIGN KEY (`CID`)
    REFERENCES `Customers` (`ID`)
    ON DELETE NO ACTION -- cannot be SET NULL since we have CID as NOT NULL --
    ON UPDATE NO ACTION
);

-- Deleting from OrderDetails if customerID and ISBN is deleted --
CREATE OR REPLACE TABLE `OrderDetails` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `BookISBN` INT NOT NULL,
  `OID` INT NOT NULL,
  `OrderQty` INT,
  `UnitPrice` DECIMAL(7,2),
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_order_detail_book`
    FOREIGN KEY (`BookISBN`)
    REFERENCES `Books` (`ISBN`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_detail_order1`
    FOREIGN KEY (`OID`)
    REFERENCES `Orders` (`ID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
);

/* --------------------- INSERTS ------------------------ */

INSERT INTO Authors (
    FirstName, LastName, Gender
)
VALUES
('Joanne', 'Rowling', 'Female'),
('Alex', 'MichaelIDes', 'Male'),
('Ray', 'Bradbury', 'Male'),
('Liu', 'Cixin', 'Male');

INSERT INTO Publishers (
    Company, Year
)
VALUES
('Scholastic Corporation', 1920),
('Macmillian Publishers', 1843),
('Ballantine Books', 1952);

INSERT INTO Customers (
    FirstName, LastName, Email
)
VALUES
('Patrick', 'Kim', 'kimpatr@oregonstate.edu'),
('William', 'Chen', 'chewill@oregonstate.edu'),
('Jane', 'Smith', 'jsmith@mail.com');

INSERT INTO Books (
    Title, Genre, Stock, Price, AID, PID
)
VALUES
("Harry Potter and the Sorcerer's Stone", 'Fantasy', 50, 7.00, 
(SELECT ID FROM Authors WHERE FirstName = 'Joanne' AND LastName = 'Rowling'),
(SELECT ID FROM Publishers WHERE Company = 'Scholastic Corporation')),
("The Silent Patient", 'Thriller', 123, 10.53, 
(SELECT ID FROM Authors WHERE FirstName = 'Alex' AND LastName = 'MichaelIDes'),
(SELECT ID FROM Publishers WHERE Company = 'Macmillian Publishers')),
("Farenheit 451", 'Sci-Fi', 451, 8.36, 
(SELECT ID FROM Authors WHERE FirstName = 'Ray' AND LastName = 'Bradbury'),
(SELECT ID FROM Publishers WHERE Company = 'Ballantine Books')),
("The Three-Body Problem", 'Sci-Fi', 333, 10.59, 
(SELECT ID FROM Authors WHERE FirstName = 'Liu' AND LastName = 'Cixin'),
(SELECT ID FROM Publishers WHERE Company = 'Macmillian Publishers')),
("The Fury", 'Thriller', 72, 16.19, 
(SELECT ID FROM Authors WHERE FirstName = 'Alex' AND LastName = 'MichaelIDes'),
(SELECT ID FROM Publishers WHERE Company = 'Macmillian Publishers'));

INSERT INTO Orders (
    Date, TotalPrice, CID
)
VALUES
(20240323, 26.78, (SELECT ID FROM Customers WHERE FirstName = 'Patrick' AND LastName = 'Kim')),
(20240331, 18.89, (SELECT ID FROM Customers WHERE FirstName = 'William' AND LastName = 'Chen')),
(20240402, 10.53, (SELECT ID FROM Customers WHERE FirstName = 'Patrick' AND LastName = 'Kim')),
(20240420, 83.60, (SELECT ID FROM Customers WHERE FirstName = 'Jane' And LastName = 'Smith'));

INSERT INTO OrderDetails (
    BookISBN, OID, OrderQty, UnitPrice
)
VALUES
((SELECT ISBN FROM Books WHERE Title = "The Three-Body Problem"),(SELECT ID FROM Orders WHERE ID = 1), 1, 10.59),
((SELECT ISBN FROM Books WHERE Title = "The Fury"),(SELECT ID FROM Orders WHERE ID = 1), 1, 16.19),
((SELECT ISBN FROM Books WHERE Title = "The Silent Patient"),(SELECT ID FROM Orders WHERE ID = 2), 1, 10.53),
((SELECT ISBN FROM Books WHERE Title = "Farenheit 451"),(SELECT ID FROM Orders WHERE ID = 2), 1, 8.36),
((SELECT ISBN FROM Books WHERE Title = "The Silent Patient"),(SELECT ID FROM Orders WHERE ID = 3), 1, 10.53),
((SELECT ISBN FROM Books WHERE Title = "Farenheit 451"),(SELECT ID FROM Orders WHERE ID = 4), 10, 8.36);


SET FOREIGN_KEY_CHECKS=1;
COMMIT;

/* Testing to make sure I still remember how to use github */