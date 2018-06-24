DROP TABLE Pref_Flip_Five;

DROP TABLE Pref_Five;

CREATE TABLE Pref_Five (
   id CHAR(47)  PRIMARY KEY,
   processed BOOLEAN
);


DROP TABLE Pref_Five_Address;

CREATE TABLE Pref_Five_Address (
   id INT NOT NULL AUTO_INCREMENT,
   csp1 INT,
   csp2 INT,
   csp3 INT,
   csp4 INT,
   csp5 INT,
   flip INT,
   name varchar(255),
   processed BOOLEAN,
  PRIMARY KEY (id),
  UNIQUE KEY address (csp1, csp2, csp3, csp4, csp5, flip)
);


INSERT INTO Pref_Five_Address (csp1,csp2,csp3,csp4,csp5,flip,processed) VALUES (3,3,3,3,3,1,false);

SELECT * FROM Pref_Five_Address;



DROP TABLE Pref_Six_Address;

CREATE TABLE Pref_Six_Address (
   id INT NOT NULL AUTO_INCREMENT,
   csp1 INT,
   csp2 INT,
   csp3 INT,
   csp4 INT,
   csp5 INT,
   csp6 INT,
   flip INT,
   name varchar(255),
   processed BOOLEAN,
  PRIMARY KEY (id),
  UNIQUE KEY address (csp1, csp2, csp3, csp4, csp5, csp6, flip)
);

INSERT INTO Pref_Six_Address (csp1,csp2,csp3,csp4,csp5,csp6,flip,processed) VALUES (1,1,1,1,1,1,1,false);

SELECT COUNT(*) FROM Pref_Six_Address;

CREATE TABLE Pref_Flip_Five (
   id1 CHAR(47) NOT NULL,
   id2 CHAR(47) NOT NULL,
   flip1 int NOT NULL,
   flip2 int NOT NULL,
  CONSTRAINT FK_id1 FOREIGN KEY (id1)
    REFERENCES Pref_Five(id),
    CONSTRAINT FK_id2 FOREIGN KEY (id2)
    REFERENCES Pref_Five(id)
);

ALTER TABLE Pref_Flip_Five ADD UNIQUE pff_unique (id1, id2);

DELETE FROM Pref_Flip_Five;

DELETE FROM Pref_Five;

INSERT INTO Pref_Five (id,processed) VALUES ('31-30-29-28-27-26-25-24-23-22-21-20-19-18-17-16',false);

ALTER TABLE Pref_Five ADD COLUMN name VARCHAR(255) NOT NULL;

SELECT * FROM Pref_Five ORDER BY name;

SELECT COUNT(*) FROM Pref_Five;

SELECT * FROM Pref_Flip_Five;

SELECT COUNT(*) FROM Pref_Flip_Five;

SELECT * FROM Pref_Flip_Five WHERE (id1 = '31-30-29-28-27-26-25-24-23-22-21-20-19-18-17-15-16-14-13-12-11-10-9-8-7-6-5-4-3-2-1-0' OR id2 = '31-30-29-28-27-26-25-24-23-22-21-20-19-18-17-15-16-14-13-12-11-10-9-8-7-6-5-4-3-2-1-0') AND  (flip1=15 AND flip2=16);


SELECT * FROM Pref_Flip_Five where id2 = '31-30-29-28-27-26-25-24-23-22-21-20-19-18-17-15';



CREATE TABLE Pref_Five_T (
   id CHAR(47),
   processed BOOLEAN
);

DELETE FROM Pref_Five_T;

INSERT INTO Prev_Five_Z (id, processed) SELECT (id, processed) FROM Pref_Five;

CREATE TABLE Pref_Five_Z (
   idint INT AUTO_INCREMENT PRIMARY KEY,
   id CHAR(47)  UNIQUE,
   processed BOOLEAN
);

INSERT INTO Pref_Five_T (id, processed) VALUES ('31-30-29-27-23-15-28-26-22-14-25-21-13-19-11-23', 0);

SELECT * FROM Pref_Five_Z;

DROP TABLE Pref_Flip_Six;

DROP TABLE Pref_Six;

CREATE TABLE Pref_Six (
   id CHAR(95)  PRIMARY KEY,
   processed BOOLEAN
);


CREATE TABLE Pref_Flip_Six (
   id1 CHAR(95) NOT NULL,
   id2 CHAR(95) NOT NULL,
   flip1 int NOT NULL,
   flip2 int NOT NULL,
  CONSTRAINT FK_six_id1 FOREIGN KEY (id1)
    REFERENCES Pref_Six(id),
    CONSTRAINT FK_six_id2 FOREIGN KEY (id2)
    REFERENCES Pref_Six(id)
);

ALTER TABLE Pref_Flip_Six ADD UNIQUE pf_six_unique (id1, id2);

ALTER TABLE Pref_Six DROP COLUMN name;

ALTER TABLE Pref_Six ADD COLUMN name VARCHAR(255) UNIQUE;

INSERT INTO Pref_Six (id,processed) VALUES ('63-62-61-60-59-58-57-56-55-54-53-52-51-50-49-48-47-46-45-44-43-42-41-40-39-38-37-36-35-34-33-32', false);


SELECT COUNT(*) FROM Pref_Six WHERE processed = false;

SELECT COUNT(*) FROM Pref_Six WHERE name IS NOT NULL;

SELECT COUNT(*) FROM Pref_Six;

SELECT COUNT(*) FROM Pref_Flip_Six;



DROP TABLE Pref_Flip_Seven;

DROP TABLE Pref_Seven;

CREATE TABLE Pref_Seven (
   id VARCHAR(225)  PRIMARY KEY,
   processed BOOLEAN
);


CREATE TABLE Pref_Flip_Seven (
   id1 VARCHAR(225) NOT NULL,
   id2 VARCHAR(225) NOT NULL,
   flip1 int NOT NULL,
   flip2 int NOT NULL,
  CONSTRAINT FK_seven_id1 FOREIGN KEY (id1)
    REFERENCES Pref_Seven(id),
    CONSTRAINT FK_seven_id2 FOREIGN KEY (id2)
    REFERENCES Pref_Seven(id)
);


INSERT INTO Pref_Seven (id,processed) VALUES ('127-126-125-124-123-122-121-120-119-118-117-116-115-114-113-112-111-110-109-108-107-106-105-104-103-102-101-100-99-98-97-96-95-94-93-92-91-90-89-88-87-86-85-84-83-82-81-80-79-78-77-76-75-74-73-72-71-70-69-68-67-66-65-64
', false);

SELECT COUNT(*) FROM Pref_Seven WHERE processed = false;

SELECT * FROM Pref_Seven LIMIT 500;

SELECT id, name FROM Pref_Five LIMIT 600;


SELECT id FROM Pref_Seven WHERE processed = False LIMIT 5000;


SELECT DISTINCT flip1, flip2 from Pref_Flip_Six;


SELECT * FROM Pref_Flip_Six WHERE flip1 = 4 and flip2 = 3;


SELECT * FROM Pref_Flip_Five WHERE flip1 = 4 and flip2 = 3;


UPDATE Pref_Five SET name='BBBB2-BBBB2-BBBB2-BBBB2-BBBB2' WHERE id='31-30-29-27-23-15-28-26-22-14-25-21-13-19-11-24';

SELECT * FROM Pref_Five WHERE id='31-30-29-27-23-15-28-26-22-14-25-21-13-19-11-24';

SELECT COUNT(*) FROM Pref_Six WHERE name IS NULL;


SELECT id, name FROM Pref_Six;


SELECT * FROM PREF_FIVE WHERE id = '31-30-29-28-27-26-25-23-15-24-22-14-21-13-20-12';