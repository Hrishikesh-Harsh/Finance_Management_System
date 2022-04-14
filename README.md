## Finance_Management_System

PERSONAL FINANCE MANAGEMENT SYSTEM — FinMan
----------------------------------------------------------------------------------
-----------------------
CONTENTS OF THIS FILE:
-----------------------

1: Introduction
2: System Requirements
3: Installation & Execution
  3.1: Setup
  3.2: Input Instructions
  3.3: Using the Program
    3.3.1: As an Administrator
    3.3.2: As a User

----------------------
----------------
1: INTRODUCTION
----------------

FinMan is a menu-driven SQL-based software written in Python that allows multiple users to dynamically maintain information about their total cash flow across multiple possible accounts linked to various banks. 

With the help of this, a user can:

- Perform transactions
- Invest in funds
- Keep track of periodic inflow of salary/interest/income

...and many other things! 

An administrator can be employed at the server device which shall be running the centralised copy of this software 24-7 to make it possible for all the users to have a hassle-free experience. The administrator can perform finer operations like tracing the history of certain transactions or tracking users' accounts and performing administritative actions such as removing accounts.

Note that with each run of the software, the administrator HAS TO log in first. Otherwise, the server is not activated for use by everyone (this is because only the administrator has the database password, which is necessary for any operation). 

All operations can be performed with the aid of simple, elegantly-designed menus. A user-friendly experience has been ensured, along with a non-compromisable database system. The use of SHA-256 encryption for storing and managing passwords makes the system extremely reliable and secure.

Concurrency has also been handled to some extent by making use of mysql.connector library's commit() and rollback() functions appropriately.

-----------------------
2: SYSTEM REQUIREMENTS
-----------------------

- MySQL 8.0.28 [Any version from the MySQL-8 series should work fine]
- Python 3.10.4 [Any version from the Python-3 series should work fine]

The following Python-3 libraries need to be installed beforehand (if not preinstalled already) externally for the software to function appropriately. "pip install <package_name>" may be used in the terminal to do the same.

- audioop
- base64
- ctypes
- mysql.connector
- csv
- hashlib
- time
- datetime
- stdiomask
- fontstyle
- prettytable

The software internally requires a .csv file to be present in the same directory as the python executable. This is supplied in the package. Caution must be taken not to remove it. (Kindly follow steps provided in section 4.1 if AdminInfo.csv is removed or absent from directory).

Details about how to install and use this software has been discussed in the next section (section 3). Specifics regarding taking inputs from the user have been described in section 4.2 of this document. 

----------------------------
3: INSTALLATION & EXECUTION
----------------------------

-----------
3.1: Setup
-----------

This directory consists of four files:
- "FinMan.py", the python code
- "Prelims.sql", a .sql script
- "AdminInfo.csv", a helper file
- "README.md", this document


After extraction, first and foremost, the user must execute ALL the queries present in the Prelims.sql script file. This is ABSOLUTELY necessary, otherwise the required database and tables will not be created and the software will not run. To do so, one may open SQL Workbench and open the .sql file using its explorer and then running the entire script (Note: Run the entire script and not some selected part of it). This script will generate the required database along with its tables and some sample data. Once this is done, the software is ready to execute for the first time.

During first login, the Administrator must input THEIR SQL database password (password of MySQL Workbench on the side of the person using the software) CAREFULLY and CORRECTLY, because this password will thenceforth be taken as canon. Afterwards, the program will check the entered passwords against this firstly entered password only (the user gets three attempts to enter the password). If incorrectly entered (error messages will be displayed in every subsequent runs of the program), kindly delete the "AdminInfo.csv" file from the directory and then follow the re-creation steps for the file provided in the section below. The password is stored into "AdminInfo.csv" in SHA-256 encrypted format, along with some other details.

IMPORTANT: 
If AdminInfo.csv is removed or absent from the python executable's main directory, perform the following steps and then try running the program:

- Create a .txt file in the same directory as the python executable.
- Type a plaintext "0" (numeral zero, without quotes) into the .txt file (and nothing else).
- Save the file as "AdminInfo.csv" (make sure to save the extension of the filename correctly, too) in the directory of the python executable.
- Delete the .txt file (NOT the .csv file).

If the program still reports that AdminInfo.csv is absent, try relocating/moving the AdminInfo.csv to the default location of your command prompt or terminal (for instance, C:\User\Desktop>).

------------------------
3.2: Input Instructions
------------------------

Sample Data:

Some sample data has been added into the database through the script file that must be run before executing the python program. These sample data consist of users, their accounts, and loans/investments, etc that the users might have on those accounts. To use the sample data, one will require the passwords of the users (these passwords are internally stored in the database using the SHA-256 encryption algorithm, so it is secure). The sample users and their passwords are listed below:

+--------------------+--------------+
| USERNAME           | PASSWORD     |
+--------------------+--------------+
| Phil Hill          | Phil123      |
+--------------------+--------------+
| Alberto Ascari     | Alberto123   |
+--------------------+--------------+
| Stirling Moss      | Stirling123  |
+--------------------+--------------+
| John Surtees       | John123      |
+--------------------+--------------+
| Rene Arnoux        | Rene123      |
+--------------------+--------------+
| Alain Prost        | Alain123     |
+--------------------+--------------+
| Ayrton Senna       | Ayrton123    |
+--------------------+--------------+
| Michael Schumacher | Michael123   |
+--------------------+--------------+
| Sebastian Vettel   | Sebastian123 |
+--------------------+--------------+
| Lewis Hamilton     | Lewis123     |
+--------------------+--------------+

-----------------------
3.3: Using the Program
-----------------------

IMPORTANT: The .py code can be run on any standard IDE (Pycharm, VSCode, etc) or using any command line executor such as Windows powershell or Linux command-line terminal. If run on cmd, the appropriate formatting that makes the frontend possible may not be visible at all. Therefore, preferably use a standard IDE for this project.

As an Administrator:

Multiple flexible operations are made available to the Administrator. They are listed as follows:

+---------------------+-----------------------------------------------------------------+
| Add user            | Allows the Administrator to enter details about 'n' new users,  |
|                     | assign them passwords, and then add them to the database.       |
|                     | This enables the individuals to log in thereafter.              |
+---------------------+-----------------------------------------------------------------+
| Add account         | Lets the Administrator add an Account at some Branch for a      |
|                     | user via their UserID.                                          |
+---------------------+-----------------------------------------------------------------+
| Remove account      | Allows the Administrator to remove an Account from a user's     |
|                     | inventory.                                                      |
+---------------------+-----------------------------------------------------------------+
| Update user info    | Allows the Administrator to edit the info (name, address,       |
|                     | salary, primary account) of a user which has already been       |
|                     | added.                                                          |
+---------------------+-----------------------------------------------------------------+
| View user accounts  | Lists all the accounts registered for a particular user (via    |
|                     | their UserID).                                                  |
+---------------------+-----------------------------------------------------------------+
| View all users      | Displays a list of all the users registered on the platform.    |
+---------------------+-----------------------------------------------------------------+
| View User Info      | Finds all info about the user who owns the account having       |
| Linked to an        | ID as entered by the Administrator                              |
| Account             |                                                                 |
+---------------------+-----------------------------------------------------------------+
| Search For User     | Finds all info about a user via either their UserID or Name.    |
+---------------------+-----------------------------------------------------------------+
| View Branch Info    | Lists all the branches for a particular bank via their BankID.  |
+---------------------+-----------------------------------------------------------------+
| View Loan Amounts   | Displays the total amount of loan that has been availed from    |
| In A Branch         | a particular branch.                                            |
+---------------------+-----------------------------------------------------------------+
| View Transaction    | Displays all the transactions performed using the software      |
| History             | between the dates entered by the admin (does not report         |
|                     | periodic inflow of salary/interest/other fixed income).         |
+---------------------+-----------------------------------------------------------------+
| View Accounts       | Displays all the accounts that have invested in a particular    |
| Linked to an        | scheme.                                                         |
| Investment          |                                                                 |
+---------------------+-----------------------------------------------------------------+
| Trace Transactions  | Returns all information (sender/receiver details, amount, etc)  |
| with TransactionID  | about a particular transaction.                                 |
+---------------------+-----------------------------------------------------------------+
| View Investment     | Displays all the schemes available and their expected           |
| Schemes             | rates of return.                                                |
+---------------------+-----------------------------------------------------------------+
| Refresh all Records | Updates all records with the periodic changes in amounts        | 
|                     | (salary, interests from bank/investments, fixed income, EMI     |
|                     | from loans). Note that these amounts are by default             |
|                     | auto-updated whenever the Administrator logs into the server.   |
|                     | This is just a manual option to do the same.           |
+---------------------+-----------------------------------------------------------------+

As a User:

Various operations are performable by the user. They are elaborated in the following table:

+------------------+-----------------------------------------------------------------+
| View all my      | Displays the information of all accounts registered by the user |
| Accounts         | on the software.                                                |
+------------------+-----------------------------------------------------------------+
| View my Account  | Displays all information about a particular account registered  |
|                  | by the user, via its AccountID.                                 |
+------------------+-----------------------------------------------------------------+
| View all my      | Displays entire information about all loans availed by the      |
| Loans            | user (if any).                                                  |
+------------------+-----------------------------------------------------------------+
| View my Loan     | Displays entire information about a particular loan availed by  |
|                  | the user, via its LoanID.                                       |
+------------------+-----------------------------------------------------------------+
| View Banks       | Lists all the banks (and their relevant information) linked to  |
| Linked to us     | the software for the user's convenience.                        |
+------------------+-----------------------------------------------------------------+
| View Branch Info | Reports all relevant information about a particular branch via  |
|                  | its BranchID.                                                   |
+------------------+-----------------------------------------------------------------+
| View Investment  | Displays all the investment schemes that are available          |
| Schemes          | on the software for the user's knowledge.                       |
+------------------+-----------------------------------------------------------------+
| View Loan Rates  | Returns the rates of interest offered by various banks for      |
|                  | different kinds of loans, as requested by the user.             |
+------------------+-----------------------------------------------------------------+
| Transfer Money   | Allows the user to perform a transaction: send some amount of   |
|                  | money from one of their accounts to another account             |
|                  | (both via AccountID). If successful, this is then updated on    |
|                  | the transaction history.                                        |
+------------------+-----------------------------------------------------------------+
| Invest Money     | Gives the user the option to invest into a scheme for a         |
|                  | specified duration.                                             |
+------------------+-----------------------------------------------------------------+
| View My          | Lists all the information about the investments that the user   |
| Investments      | has made.                                                       |
+------------------+-----------------------------------------------------------------+
| Withdraw         | Lets the user withdraw (prematurely) the initial amount         |
| Investment       | (the principal) they had invested into a scheme.                |
+------------------+-----------------------------------------------------------------+
| List Transaction | Displays a list of all the transactions that have involved a    |
| History          | particular account of the user between the two dates entered.   |
+------------------+-----------------------------------------------------------------+

Note: An registered account must necessarily have a minimum balance of Rs. 1000 at all times. 

----------------------------------------------------------------------------------
