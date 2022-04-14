create database finman;

use finman;

-- User Info
create table user
(UserID INT Unsigned NOT NULL,
Name Varchar(256) NOT NULL,
Address Varchar(256) NOT NULL,
Salary INT Unsigned NOT NULL,
PrimaryAccount INT UNSIGNED NOT NULL,
Password Varchar(256) NOT NULL,
PRIMARY KEY (UserID));

-- Bank Info
create table bank
(BankID INT UNSIGNED NOT NULL,
Name Varchar(255) NOT NULL,
InterestRate Decimal(3,2) NOT NULL,
Established INT UNSIGNED NOT NULL,
Headquarters Varchar(256) NOT NULL,
primary key (BankID));

-- Branch Info
create table branch
(BranchID INT UNSIGNED NOT null,
Address Varchar(256) NOT NULL,
Manager Varchar(256) NOT NULL,
BankID INT UNSIGNED NOT NULL,
primary key (BranchID),
constraint FK_BNKID FOREIGN KEY (BankID) References bank(BankID));

-- User Accounts
create table accounts
(AccountID INT Unsigned NOT NULL,
Balance INT Unsigned NOT NULL,
UserID INT Unsigned NOT NULL,
BranchID INT UNSIGNED NOT NULL,
LastUpdate datetime DEFAULT current_timestamp,
PRIMARY KEY (AccountID),
CONSTRAINT FK_UID FOREIGN KEY (UserID) References user(UserID) ON DELETE CASCADE,
CONSTRAINT FK_BID FOREIGN KEY (BranchID) References branch(BranchID));


-- Types Of Loans
create table loantype
(TypeID INT UNSIGNED NOT NULL,
 LoanType Varchar(256) NOT NULL,
 primary key (TypeID));
 
 -- Details of LoanTypes in Banks
 create table loaninfo
(BankID INT UNSIGNED NOT NULL,
 TypeID INT unsigned NOT NULL,
 InterestRate decimal(4,2) NOT NULL,
 primary key (BankID,TypeID),
 foreign key FK_BKID (BankID) References bank (BankID));
 
 -- All Loans
 create table loans
(LoanID int unsigned, 
Amount int unsigned not null, 
EMI int unsigned not null, 
AmountLeft int unsigned not null,
StartDate date not null,
EndDate date not null, 
BranchID int unsigned Not null, 
TypeID int unsigned not null, 
AccountID int unsigned not null, 
LastUpdate datetime default current_timestamp, 
primary key (LoanID), 
foreign key (BranchID) references branch(BranchID),
foreign key (TypeID) references loantype(TypeID),
foreign key (AccountID) references Accounts(AccountID) on delete cascade);

-- Investment Schemes
create table schemes
(InvestmentID INT UNSIGNED NOT NULL,
Name varchar(256) NOT NULL,
RateOfReturn DECIMAL(4,2) NOT NULL,
primary key (InvestmentID));

-- Investments Made
create table investments
(InvestmentID int unsigned, 
AccountID int unsigned not null, 
InitialInvestment INT Unsigned NOT NULL,
CurrentAmount int unsigned not null,
StartDate date not null,
EndDate date not null,
LastUpdate datetime not null,
primary key (InvestmentID,AccountID),
foreign key (AccountID) references Accounts(AccountID) on delete cascade,
foreign key (InvestmentID) references schemes(InvestmentID));

-- Transaction History
create table transactions
(TransactionID INT AUTO_INCREMENT,
FromID INT UNSIGNED NOT NULL,
ToID INT UNSIGNED NOT NULL,
Amount INT UNSIGNED NOT NULL,
Purpose varchar(256),
Processed DATETIME NOT NULL,
primary key (TransactionID));


-- Preliminary Data Insertion

-- Users
insert into user values
(10001,"Phil Hill","3,Bonnington Rd,London", 30000,100011011,"9f22f6eb882235f3f9cd032f4fc1524ff0064d828d8123cb0a33c6fc135847a3"),
(10002,"Alberto Ascari","5, Kinglsey Rd, London",40000,100021012,"abe368d18e6ba4e76b027a0d06c8ea0e88281da869889fa74dfe08823ae1fb65"),
(10003,"Stirling Moss","15,Rothmann St,Birmingham",50000,100031022,"1c22a473f1ce015aca9faf4a2f1fcc89be0919c44603749419f05314e3b1b871"),
(10004,"John Surtees","7,Richardson Lane,Houston",70000,100041041,"370420e335f7a4d2ead6879991641792d5bdcde2db5d4fae3d976c2133732cda"),
(10005,"Rene Arnoux","12, Dupleix Avenue, Paris",65000,100051051,"f9a93efdc8ae78c5acb35706a86bffdfa224fbe22458eb878f3a7b217e0ab978"),
(10006,"Alain Prost","16,Jersey Lane,San Francisco",70000,100061061,"b575eb92cc5858ac96dd2f788fa6eb6ffcbc99fbeff502dad111d1da77cdbe0f"),
(10007,"Ayrton Senna","22,Interlagos St,Sao Paulo",	72000,100071071,"1cb732f8cfc410f5f5ce858247775d91b98db034d6972ea21890ea2e9e410744"),
(10008,"Michael Schumacher","20,Marlborough St,London",75000,100081081,"b5f382ea65fbd547f4b8f0e35995fba259066c2cedf60b35dfcffa358c8d03a9"),
(10009,"Sebastian Vettel","25,Leicester Lane,Detroit",65000,100091091,"762ff3fda60a5663e96ae208bf4b56f54b9d74e954147350193b59f16806b3fa"),
(10010,"Lewis Hamilton","23,Trafalgar Square Av,London",76000,100101101,"1d86c9a953839b0ee2550a73631f585124daada3c6fca07f6deef62899f08425");

-- Banks
insert into bank values
(101,'Bank Of India',3.90,1906,'Mumbai'),
(102,'State Bank Of India',4.20,1955,'Mumbai'),
(103,'JP Morgan Chase', 4.50, 2000, 'New York'),
(104, 'Standard Chartered Bank', 3.25, 1969, 'London'),
(105, 'Wells Fargo & Co', 3.80, '1852', 'New York'),
(106, 'Citigroup Inc.', 3.90, '1998', 'New York'),
(107, 'Morgan Stanley', 3.70, '1935', 'New York'),
(108, 'HSBC', 3.60, '1865', 'Hong Kong'),
(109, 'UBS Grp AG', 3.85, '1998', 'Winterthur'),
(110, 'Santander Grp', 3.95, '1857', 'Santander');


-- Branches
insert into branch values
(1011, '15,Park Lane,Delhi','Rakesh Jha',101),
(1012, '11,Bose St,Kolkata','JC Ganguly',101),
(1021, '17,Garden Park Rd,Indore','Sanket Mishra',102),
(1022, '18,Hiland Park,Bangalore','Feroz Shah',102),
(1031, '13,Coventry St,Atlanta','Jack Hobbs',103),
(1032, '19,Donnington Lane,Boston','Ken Smith',103),
(1072, '20,Old Kent Rd,London','Jody Schekter',107),
(1041, '21,Whitechapel Lane,Detroit','James Hunt',104),
(1042, '28,Pentonville Rd,Silverstone','Alan Jones',104),
(1051, '1,Euston Av,Phoenix','Nelson Piquet',105),
(1061, '12,Whitehall Garden Lane,Las Vegas','Gerhard Berger',106),
(1071, '25,Vine St,Glasgow','Nigel Mansell',107),
(1081, '10,Fleet St,Dublin','Mario Andretti',108),
(1091, '27,Coventry St,Bern','Jacques Villeneuve',109),
(1101, '26,Brixton Rd,Madrid','Mark Webber',110);


-- Accounts
insert into accounts (AccountID,Balance,UserID,BranchID) values
(100011011,120000,10001,1011),
(100011021,160000,10001,1021),
(100021012,120000,10002,1012),
(100021031,120000,10002,1031),
(100031022,120000,10003,1022),
(100031032,120000,10003,1032),
(100041041,190000,10004,1041),
(100051051,210000,10005,1051),
(100061061,420000,10006,1061),
(100071071,510000,10007,1071),
(100081081,360000,10008,1081),
(100091091,630000,10009,1091),
(100101101,740000,10010,1101),
(100041042,195000,10004,1042),
(100071072,620000,10007,1072),
(100051072,250000,10005,1072),
(100061051,460000,10006,1051),
(100081041,390000,10008,1041),
(100091071,680000,10009,1071),
(100101061,710000,10010,1061);

-- Loan Types
 insert into loantype values
 (1,'Personal'),
 (2,'Business'),
 (3,'Education'),
 (4,'Agricultural'),
 (5,'Vehicle'),
 (6,'Home');

-- Loan Info
insert into loaninfo
 values
 (101,1,21.10),
 (101,2,17.20),
 (101,3,15.5),
 (101,4,9.6),
 (101,5,8.2),
 (101,6,6.9),
 (102,1,20.10),
 (102,2,17.25),
 (102,3,15.20),
 (102,4,9.2),
 (102,5,8.8),
 (102,6,7.3),
 (103,1,20.90),
 (103,2,17.05),
 (103,3,14.8),
 (103,6,7.0),
 (104,1,20.95),
 (104,2,17.00),
 (104,3,14.55),
 (104,6,7.3),
  (105,1,20.50),
 (105,2,17.2),
 (105,3,14.45),
 (105,6,7.2),
  (106,1,20.70),
 (106,2,17.35),
 (106,3,14.95),
 (106,6,7.0),
  (107,1,20.50),
 (107,2,17.55),
 (107,3,14.65),
 (107,6,7.15),
  (108,1,20.60),
 (108,2,17.15),
 (108,3,14.6),
 (108,6,7.1),
  (109,1,20.95),
 (109,2,17.0),
 (109,3,14.7),
 (109,6,7.0),
  (110,1,20.70),
 (110,2,17.10),
 (110,3,14.85),
 (110,6,7.05);
 
 -- Loans of Users
insert into loans
values
(1000310221,100000,9268,111218,'2022-03-01','2023-03-01',1022,1,100031022,'2022-03-01 12:00:20'),
(1000310321,2000000,23221,2786569,'2022-03-01','2026-03-01',1032,6,100031032,'2022-03-01 12:00:20'),
(1000110111,50000,4324,51888,'2022-03-01','2023-03-01',1011,4,100011011,'2022-03-01 12:00:20'),
(1000110211,500000,24769,0,'2020-03-01','2022-03-01',1021,2,100011021,'2022-03-01 12:00:20'),
(1000510721,800000,23312,1118990,'2022-04-10','2026-04-10',1072,2,100051072,now()),
(1000710721,70000,3580,85920,'2022-04-10','2024-04-10',1072,1,100071072,now()),
(1000410411,500000,11777,706630,'2022-04-10','2027-04-10',1041,3,100041041,now()),
(1000810411,1200000,14119,1694310,'2022-04-10','2032-04-10',1041,6,100081041,now()),
(1000910911,1600000,18577,2229580,'2022-04-10','2032-04-10',1091,6,100091091,now()),
(1001011011,600000,14944,896630,'2022-04-10','2027-04-10',1101,2,100101101,now());

-- Investment Schemes
insert into schemes
values
(111,'JP Morgan Prime Money Market Fund',16.10),
(112,'National Pension Scheme',9.00),
(113,'GOI Public Provident Fund',7.80),
(114,'Senior Citizens Saving Scheme (SCSS)',8.50),
(115,'RBI Bond',7.75),
(116,'Highland Park Towers',17.20),
(117,'Post Office Monthly Income Scheme(POMIS)',7.60),
(118,'Aditya Birla SunLife Gold Funds',9.20),
(119,'Mahindra Finance',6.50),
(120,'Sundial Prudential Bonds',8.50);

-- Investments
insert into investments values
(113,100011011,100000,100000,'2022-03-01','2037-03-01','2022-03-01 12:00:00'),
(117,100021012,50000,50000,'2022-03-01','2027-03-01','2022-03-01 12:00:00'),
(119,100031032,200000,200000,'2022-03-01','2032-03-01','2022-03-01 12:00:00'),
(111,100041041,250000,250000,'2022-03-01','2027-03-01','2022-03-01 12:00:00'),
(112,100051051,500000,500000,'2022-03-01','2052-03-01','2022-03-01 12:00:00'),
(114,100061061,700000,700000,'2022-03-01','2027-03-01','2022-03-01 12:00:00'),
(115,100071071,350000,350000,'2022-03-01','2029-03-01','2022-03-01 12:00:00'),
(116,100081081,1500000,1500000,'2022-03-01','2027-03-01','2022-03-01 12:00:00'),
(118,100091091,200000,200000,'2022-03-01','2030-03-01','2022-03-01 12:00:00'),
(118,100101101,150000,150000,'2022-03-01','2025-03-01','2022-03-01 12:00:00'),
(120,100071072,50000,50000,'2022-03-01','2027-03-01','2022-03-01 12:00:00'),
(116,100041042,2000000,2000000,'2022-03-01','2030-03-01','2022-03-01 12:00:00'),
(111,100011011,150000,150000,'2022-03-01','2027-03-01','2022-03-01 12:00:00'),
(115,100041041,250000,250000,'2022-03-01','2028-03-01','2022-03-01 12:00:00'),
(118,100081081,240000,240000,'2022-03-01','2027-03-01','2022-03-01 12:00:00');

-- Transactions
insert into transactions values
(1000001,100011011,100021012,2000,'Phone Repairs','2022-01-01 12:00:00'),
(1000002,100011011,100021031,1500,'Dinner Party','2022-02-01 12:00:00'),
(1000003,100011011,100031022,200,'Snacks','2022-03-01 12:00:00'),
(1000004,100031032,100011011,3000,'Dress','2022-04-01 12:00:00'),
(1000005,100041041,100011011,1000,'Sunday Outing','2022-04-05 12:00:00'),
(1000006,100071071,100041042,2500,'Groceries','2022-01-01 12:00:00'),
(1000007,100071071,100051051,15000,'School Supplies','2022-02-01 12:00:00'),
(1000008,100071071,100061061,600,'Cinema (Paradiso)','2022-03-01 12:00:00'),
(1000009,100061061,100071071,5000,'House Repairs','2022-04-01 12:00:00'),
(1000010,100101101,100071071,10000,'Festive Shopping','2022-04-05 12:00:00'),
(1000011,100091091,100101101,20000,'Weekend Trip','2022-01-01 12:00:00'),
(1000012,100091091,100081081,4000,'Go Karting','2022-02-01 12:00:00'),
(1000013,100091091,100041042,2000,'Dinner Date','2022-03-01 12:00:00'),
(1000014,100031032,100091091,30000,'Skiing','2022-04-01 12:00:00'),
(1000015,100051051,112,500000,'National Pension Scheme','2022-03-01 12:00:00');

