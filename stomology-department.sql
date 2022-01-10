CREATE DATABASE stomology-dep;

CREATE TABLE Admin(
    id int Not NULL Auto_Increment,
    UserName varchar(30),
    Password varchar(20),
    PRIMARY KEY(id)
);

CREATE TABLE USERS(
    id int Not NULL Auto_Increment,
    FName Varchar(20),
    MidName Varchar(20),
    LName Varchar(20),
    Image Varchar(100),
    UserName varchar(30),
    Password varchar(20),
    Email varchar(100),
    Phone varchar(20),
    PRIMARY KEY(id)
);

CREATE TABLE Site_Information(
Title Varchar(100),
    Address Varchar(100),
    Email Varchar(100),
    Phone varchar(20) ,
    Short_description Varchar(500),
    Long_description Varchar(1000),
    Icon Varchar(50)
);
CREATE TABLE Slider(
    ID INT Not NULL Auto_Increment,
    Image Varchar(500),
    Title Varchar(500),
    Description Varchar(500),
    PRIMARY KEY(ID)
);
CREATE TABLE Rates(
    Rating int ,
    Review Varchar(500),
    UserID int ,
    FOREIGN KEY( UserID) REFERENCES USERS(id) 
);

CREATE TABLE Doctors(    
    id INT Not NULL AUTO_INCREMENT,
    SSN INT Not NULL,
    FName Varchar(20),
    MidName Varchar(20),
    LName Varchar(20),
    Age int,
    Gender Varchar(10),
    Phone varchar(20),
    Email Varchar(100),
    Degree Varchar(50),
    Password Varchar(10),
    Image varchar(100),
    PRIMARY KEY(id)
   );

CREATE TABLE Treatments(
    id int Not NULL AUTO_INCREMENT,
    Image Varchar(100), 
    Name Varchar(200),
    cost int,
    Duration int,
    Description varchar(500),
    PRIMARY KEY(id)
);

CREATE TABLE Appointments(
    id int Not NULL AUTO_INCREMENT,
    SSN int Not NULL,
     FName Varchar(20),
    MidName Varchar(20),
    LName Varchar(20),
    Age int,
    Gender Varchar(20),
    Date date ,
    Status Varchar(20),
    UserID int  Not NULL ,
    DoctorID int Not NULL,
    ServiceID int Not NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(UserID) REFERENCES USERS (id), 
    FOREIGN KEY(DoctorID) REFERENCES Doctors (id) ,
    FOREIGN KEY(ServiceID) REFERENCES Treatments (id) 
);

insert into admin values (101,"Admin",12345);
insert into site_information values ("website","address","email","01123232","xx","xxxxx","icon.png")
