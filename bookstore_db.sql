SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

/* --------------------- CREATE ------------------------ */

CREATE OR REPLACE TABLE `Authors` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `FirstName` VARCHAR(45) NOT NULL,
  `LastName` VARCHAR(45) NOT NULL,
  `Gender` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`),
  UNIQUE (`ID`)
);

CREATE OR REPLACE TABLE `Publishers` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Company` VARCHAR(45) NOT NULL,
  `Years` INT NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE (`ID`),
  UNIQUE (`Company`)
);

CREATE OR REPLACE TABLE `Books` (
  `ISBN` INT NOT NULL AUTO_INCREMENT,
  `Title` VARCHAR(50) NOT NULL,
  `Genre` VARCHAR(45) NOT NULL,
  `Stock` INT NOT NULL,
  `Price` DECIMAL(5,2) NULL,
  `AID` INT NOT NULL,
  `PID` INT NOT NULL,
  PRIMARY KEY (`ISBN`),
  UNIQUE (`ISBN`),
  UNIQUE (`Title`),
  CONSTRAINT `fk_book_author`
    FOREIGN KEY (`AID`)
    REFERENCES `Authors` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_book_publisher`
    FOREIGN KEY (`PID`)
    REFERENCES `Publishers` (`ID`)
    ON DELETE NO ACTION
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

CREATE OR REPLACE TABLE `Orders` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Date` DATETIME NOT NULL,
  `total_price` DECIMAL(7,2) NOT NULL,
  `CID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE (`ID`),
  CONSTRAINT `fk_order_customer1`
    FOREIGN KEY (`CID`)
    REFERENCES `Customers` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

CREATE OR REPLACE TABLE `Order_Details` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `BookISBN` INT NOT NULL,
  `OID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_order_detail_book`
    FOREIGN KEY (`BookISBN`)
    REFERENCES `Books` (`ISBN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_detail_order1`
    FOREIGN KEY (`OID`)
    REFERENCES `Orders` (`ID`)
    ON DELETE NO ACTION
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
    Company, Years
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
    Date, total_price, CID
)
VALUES
(20240323, 26.78, (SELECT ID FROM Customers WHERE FirstName = 'Patrick' AND LastName = 'Kim')),
(20240331, 18.89, (SELECT ID FROM Customers WHERE FirstName = 'William' AND LastName = 'Chen')),
(20240402, 10.53, (SELECT ID FROM Customers WHERE FirstName = 'Patrick' AND LastName = 'Kim')),
(20240420, 83.60, (SELECT ID FROM Customers WHERE FirstName = 'Jane' And LastName = 'Smith'));

/* ------- Order_Details Table with Join ------- */

SET FOREIGN_KEY_CHECKS=1;
COMMIT;

/* Testing to make sure I still remember how to use github */