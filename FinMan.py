from audioop import add
import base64
from ctypes import addressof
import mysql.connector
import csv
import hashlib
import time
import datetime
import stdiomask
import fontstyle
from prettytable import PrettyTable
 

connection=""


""" Misc and Helper Functions """

def strikethrough(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result
 
def view_all_branch(databasePassword):
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        sql_select_query = """select * from branch"""
 
        cursor.execute(sql_select_query)
        record = cursor.fetchall()
       
        print("\n[",cursor.rowcount,"Records Found...]\n")
       
        # print(tabulate(record, headers=["BranchID","Address","Manager","BankID"]))
       
        x=PrettyTable()
        x.field_names=["BranchID","Address","Manager","BankID"]
       
        for row in record:
            x.add_row(row)
           
        print(x)
   
    except mysql.connector.Error as error:
        print("Failed to Get Branches {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
   
    # print("\n")
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
 
 
    return
 
def view_investment_schemes(databasePassword):
    # Code to come
 
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        query = """select InvestmentID,Name,RateOfReturn from schemes"""
 
        cursor.execute(query)
        record = cursor.fetchall()
       
        print("\n[",cursor.rowcount," Records Found...]\n")
       
        # print(tabulate(record, headers=["UserID", "Name", "Address", "Salary"]))
       
        x=PrettyTable()
        x.field_names=["InvestmentID","Scheme Name","Rate Of Return (Expected)"]
       
        for row in record:
            x.add_row(row)
           
        print(x)
 
    except mysql.connector.Error as error:
        print("Failed to Fetch Records {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
 
    # done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    # print("\n",done,"\n")
    return
 
def verify_user(userID,databasePassword):
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        sql_select_query = """select Password from user where UserID = %s"""
 
        cursor.execute(sql_select_query, (userID,))
        record = cursor.fetchall()
       
        if(len(record)==0):
            return ""
 
        pw=record[0][0]
   
    except mysql.connector.Error as error:
        print("Failed to Verify {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
           
    return pw
 
def get_username(databasePassword,userID):
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        sql_select_query = """select Name from user where UserID = %s"""
       
        cursor.execute(sql_select_query, (userID,))
        record = cursor.fetchall()
       
        name=record[0][0]
   
    except mysql.connector.Error as error:
        print("Failed to Get record {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
    return name
 
def get_balance(accountID,databasePassword):
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        query = """select Balance from accounts where AccountID = %s"""
       
        cursor.execute(query, (accountID,))
        record = cursor.fetchall()

        if(len(record)==0):
            return 0;

        balance=record[0][0]
   
    except mysql.connector.Error as error:
        print("Failed to Get Balance {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

    return balance
 
def update_balances(databasePassword):
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
        cursor=connection.cursor()
       
        query="""update accounts as a, (select a.AccountID as id, u.salary as salary, TIMESTAMPDIFF(MONTH, a.LastUpdate, NOW()) as months
                        from accounts as a, user as u
                        where TIMESTAMPDIFF(MONTH, a.LastUpdate, NOW()) >= 1 and a.AccountID = u.PrimaryAccount) as sub
                        set a.Balance = a.Balance + sub.salary*sub.months where a.AccountID = sub.id;"""
 
        cursor.execute(query)
        connection.commit()
 
        query="""update accounts as a, (select AccountID, branch.BranchID, bank.BankID, InterestRate
                from accounts inner join branch on accounts.BranchID = branch.BranchID inner join bank on branch.BankID = bank.bankID) as sub
                set a.Balance = a.Balance * POWER((1 + sub.InterestRate/(100*12)),TIMESTAMPDIFF(MONTH, a.LastUpdate, NOW())), a.LastUpdate = NOW()
                where TIMESTAMPDIFF(MONTH, a.LastUpdate, NOW()) >= 1;"""
 
        cursor.execute(query)
        connection.commit()
        cursor.execute(query)
        connection.commit()
 
    except mysql.connector.Error as error:
        print("Failed To Update Records as per Month: {}".format(error))
        connection.rollback()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
 
 
    return
       
def update_all_loans(databasePassword):
    # Code to come
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
        cursor=connection.cursor()
       
        query="""Update loans
                set AmountLeft = AmountLeft - (((Select DATEDIFF(CURRENT_TIMESTAMP,LastUpdate)) DIV 30)*(Select EMI))
                where AmountLeft > 100 and TIMESTAMPDIFF(MONTH, LastUpdate, NOW()) >= 1"""
 
        cursor.execute(query)
        connection.commit()
 
        query="""Update loans as ln inner join accounts as ac on ln.AccountID=ac.AccountID
                set ac.Balance=ac.Balance-(Select DATEDIFF(CURRENT_TIMESTAMP,ln.LastUpdate) DIV 30)*(Select ln.EMI)
                where ln.AmountLeft > 100 and TIMESTAMPDIFF(MONTH, ln.LastUpdate, NOW()) >= 1"""
 
        cursor.execute(query)
        connection.commit()
 
        query="""Update loans
                set LastUpdate = current_timestamp()
                where AmountLeft > 100 and TIMESTAMPDIFF(MONTH,LastUpdate, NOW()) >= 1"""
 
        cursor.execute(query)
        connection.commit()
 
    except mysql.connector.Error as error:
        print("Failed To Update Records: {}".format(error))
        connection.rollback()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
 
    # done = fontstyle.apply('[Records Refreshed and Updated]', 'bold/green/2UNDERLINE')
    # print(done,"\n")
    return
 
def update_all_investments(databasePassword):
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
        cursor=connection.cursor()
       
        query="""Update investments as i
                inner join schemes as s
                on i.InvestmentID=s.InvestmentID
                set i.CurrentAmount
                = i.CurrentAmount * power((1+s.RateOfReturn/(12*100)),timestampdiff(month,i.LastUpdate,now())),
                i.LastUpdate=now() where TIMESTAMPDIFF(MONTH, LastUpdate, NOW()) >= 1"""
 
        cursor.execute(query)
        connection.commit()

        query="""update accounts as a
                inner join investments as i
                on a.AccountID=i.AccountID
                set a.Balance=a.Balance+i.CurrentAmount 
                where i.EndDate<=now()"""

        cursor.execute(query)
        connection.commit()

        query="""insert into transactions (FromID,ToID,Amount,Purpose,Processed)
                (Select i.InvestmentID,i.AccountID,i.CurrentAmount,concat(s.Name,' Maturity'),now()
                from investments as i
                inner join
                schemes as s
                on s.InvestmentID=i.InvestmentID
                where i.EndDate<=now())"""

        cursor.execute(query)
        connection.commit()

        query="""delete from investments
                where EndDate<=now();"""

        cursor.execute(query)
        connection.commit()
 
    except mysql.connector.Error as error:
        print("Failed To Update Records: {}".format(error))
        connection.rollback()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return
 
def verify_account(userID,accountID,databasePassword):
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        query = """select UserID from accounts where AccountID = %s"""
 
        cursor.execute(query, (accountID,))
        record = cursor.fetchall()
 
        if(len(record)==0):
            return False    
 
        idr=str(record[0][0])
   
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
 
    if(idr==userID):
        return True
    elif(idr!=userID):
        return False
 
def user_exists(userID,databasePassword):
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        query = """select UserID from user where UserID = %s"""
 
        cursor.execute(query, (userID,))
        record = cursor.fetchall()
   
    except mysql.connector.Error as error:
        print("Failed to Get Details {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
 
    if(len(record)==0):
        return False
    else:
        return True

def account_exists(accountID,databasePassword):
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        query = """select AccountID from accounts where AccountID = %s"""
 
        cursor.execute(query, (accountID,))
        record = cursor.fetchall()
   
    except mysql.connector.Error as error:
        print("Failed to Get Details {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
 
    if(len(record)==0):
        return False
    else:
        return True
 

""" User Functions """
 
def view_my_accounts(userID,databasePassword):
    # Code to come
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        sql_select_query = """select ac.AccountID,ac.Balance,ac.BranchID,bk.Name,ac.LastUpdate from
                                accounts as ac
                                inner join
                                branch as br
                                on ac.BranchID=br.BranchID
                                inner join
                                bank as bk
                                on br.BankID=bk.BankID
                                where ac.UserID=%s"""
 
        cursor.execute(sql_select_query,(userID,))
        record = cursor.fetchall()
       
        print("\n[",cursor.rowcount," Records Found...]\n")
       
        #print(tabulate(record, headers=["AccountID","Balance(Rs.)","BranchID","BankName","LastUpdate"]))
       
        x=PrettyTable()
        x.field_names=["AccountID","Balance(Rs.)","BranchID","BankName","LastUpdate"]
       
        for row in record:
            x.add_row(row)
           
        print(x)
   
    except mysql.connector.Error as error:
        print("Failed to View Accounts {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
   
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
   
    return
 
def view_my_account(userID, accountID,databasePassword):
    # Code to come
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        sql_select_query = """select ac.AccountID,ac.Balance,ac.BranchID,bk.Name,ac.LastUpdate from
                                accounts as ac
                                inner join
                                branch as br
                                on ac.BranchID=br.BranchID
                                inner join
                                bank as bk
                                on br.BankID=bk.BankID
                                where ac.UserID=%s
                                and ac.accountID=%s"""
 
        query=(userID,accountID)
        cursor.execute(sql_select_query,query)
        record = cursor.fetchall()
       
        print("\n[",cursor.rowcount," Records Found...]\n")
       
        # print(tabulate(record, headers=["AccountID","Balance(Rs.)","BranchID","BankName","LastUpdate"]))
       
        x=PrettyTable()
        x.field_names=["AccountID","Balance(Rs.)","BranchID","BankName","LastUpdate"]
       
        for row in record:
            x.add_row(row)
           
        print(x)
   
    except mysql.connector.Error as error:
        print("Failed to View Accounts {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
   
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
 
    return
 
def view_my_loans(userID,databasePassword):
    # Code to come
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        query = """select ln.LoanID,ln.Amount,ln.EMI,ln.AmountLeft,ln.StartDate,ln.EndDate,ln.BranchID,lt.LoanType
                    from loans as ln
                    inner join
                    loantype as lt
                    on ln.TypeID=lt.TypeID
                    inner join accounts as ac
                    on ln.AccountID=ac.AccountID
                    where ac.UserID=%s"""
 
        cursor.execute(query,(userID,))
        record = cursor.fetchall()
       
        print("\n[",cursor.rowcount," Records Found...]\n")
       
        # print(tabulate(record, headers=["BankID","Address","Manager","Name","InterestRate","Established","Headquarters"]))
       
        x=PrettyTable()
        x.field_names=["LoanID","Amount(Rs.)","EMI(Rs.)","Amount Left(Rs.)","Start Date","End Date","BranchID","Loan Type"]
                           
        for row in record:
            x.add_row(row)
           
        print(x)
   
    except mysql.connector.Error as error:
        print("Failed to View Loans {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
 
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
    return
 
def view_loan(accountID,databasePassword):
    # Code to come
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        query = """select ln.LoanID,ln.Amount,ln.EMI,ln.AmountLeft,ln.StartDate,ln.EndDate,ln.BranchID,lt.LoanType
                    from loans as ln
                    inner join
                    loantype as lt
                    on ln.TypeID=lt.TypeID
                    where ln.AccountID=%s"""
 
        cursor.execute(query,(accountID,))
        record = cursor.fetchall()
       
        print("\n[",cursor.rowcount," Records Found...]\n")
       
        # print(tabulate(record, headers=["BankID","Address","Manager","Name","InterestRate","Established","Headquarters"]))
       
        x=PrettyTable()
        x.field_names=["LoanID","Amount(Rs.)","EMI(Rs.)","Amount Left(Rs.)","Start Date","End Date","BranchID","Loan Type"]
                           
        for row in record:
            x.add_row(row)
           
        print(x)
   
    except mysql.connector.Error as error:
        print("Failed to View Loans {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
 
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
    return

def bank_info(databasePassword):
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        query = """select * from bank"""
 
        cursor.execute(query)
        record = cursor.fetchall()
       
        print("\n[",cursor.rowcount," Records Found...]\n")
       
        # print(tabulate(record, headers=["BankID","Address","Manager","Name","InterestRate","Established","Headquarters"]))
       
        x=PrettyTable()
        x.field_names=["BankID","Name","Savings Rate","Estd.","Headquarters"]
       
        for row in record:
            x.add_row(row)
           
        print(x)
   
    except mysql.connector.Error as error:
        print("Failed to View Records {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
   
    # print("\n")
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
 
    return

def branch_info(branchID,databasePassword):
    # Code to come
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        sql_select_query = """select BankID,Address,Manager,Name,InterestRate,Established,Headquarters from branch natural join bank where branchID=%s"""
 
        cursor.execute(sql_select_query,(branchID,))
        record = cursor.fetchall()
       
        print("\n[",cursor.rowcount," Records Found...]\n")
       
        # print(tabulate(record, headers=["BankID","Address","Manager","Name","InterestRate","Established","Headquarters"]))
       
        x=PrettyTable()
        x.field_names=["BankID","Address","Manager","Bank Name","Savings Rate","Estd.","Headquarters"]
       
        for row in record:
            x.add_row(row)
           
        print(x)
   
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
   
    # print("\n")
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
 
 
    return
 
def send_money(userID, fromID, toID, amount, databasePassword):
    # Code to come
    if(verify_account(userID, fromID, databasePassword)):
        currentBalance=get_balance(fromID,databasePassword)
 
        if(((int)(currentBalance)-(int)(amount))<1000):
            message="[Rs. 1000 Minimum Balance must be maintained!]"
            note = fontstyle.apply(message, 'bold/red/2UNDERLINE')
            print("\n",note,"\n")
            return
        
        message=input("Message/Purpose : ")

        try:
            connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
            query = """update accounts set Balance = Balance - %s where AccountID = %s"""
            record=(amount,fromID)
            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()
           
            query = """update accounts set Balance = Balance + %s where AccountID = %s""" #perform calc outside query
            record=(amount,toID)
            cursor.execute(query,record)
            connection.commit()

            query = """INSERT INTO transactions (FromID,ToID,Amount,Purpose,Processed)
                        VALUES (%s, %s, %s, %s, now())"""
       
            cursor=connection.cursor()
            record = (fromID,toID,amount,message)
            cursor.execute(query, record)
            connection.commit()

            message="[Payment Successful!]"+' \u2713'
            note = fontstyle.apply(message, 'bold/Green/2UNDERLINE')
            print("\n",note,"\n")
           
        except mysql.connector.Error as error:
            print("Failed to Send Money {}".format(error))
            connection.rollback()
         
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                #print("MySQL connection is closed")
 
        done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
        print("\n",done,"\n")
        return
    else:
        message="[Wrong AccountID!]"
        note = fontstyle.apply(message, 'bold/red/2UNDERLINE')
        print("\n",note,"\n")
        return
 
def invest_money(userID,databasePassword):
    # Code to come
    view_investment_schemes(databasePassword)
    message="[NOTE: Few Investments are subject to Market Risks.\n The Rates of Returns are dependent on Market Conditions and may Change.\n Please make Informed and Calculated Decisions]"
    note = fontstyle.apply(message, 'bold/red/2UNDERLINE')
    print("\n",note,"\n")
 
    investmentID=input("InvestmentID : ")
    amount=input("Initial Amount(Rs) : ")
    accountID=input("AccountID : ")
 
    verification=verify_account(userID,accountID,databasePassword)
    if(verification==False):
        message="[Wrong Account Number!]"
        note = fontstyle.apply(message, 'bold/red/2UNDERLINE')
        print("\n",note,"\n")
        return
       
 
    currentBalance=get_balance(accountID,databasePassword)
 
    if(((int)(currentBalance)-(int)(amount))<1000):
        message="[Rs. 1000 Minimum Balance must be maintained!]"
        note = fontstyle.apply(message, 'bold/red/2UNDERLINE')
        print("\n",note,"\n")
        return
 
    endDate=input("End Date (YYYY-MM-DD) (Min 6 Months) : ")
 
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
        query = """INSERT INTO investments VALUES (%s, %s, %s, %s, curdate(), %s, now()) """
       
        cursor=connection.cursor()
        record = (investmentID,accountID,amount,amount,endDate)
        cursor.execute(query, record)
        connection.commit()
 
        balance=(int)(currentBalance)-(int)(amount)
        query="""Update accounts set Balance=%s where AccountID=%s"""
        record=(balance,accountID)
 
        cursor.execute(query,record)
        connection.commit()
 
        query="""select Name from schemes where InvestmentID=%s"""
        cursor.execute(query,(investmentID,))
 
        record=cursor.fetchall()
 
        plan=record[0][0]
 
        query = """INSERT INTO transactions (FromID,ToID,Amount,Purpose,Processed)
                VALUES (%s, %s, %s, %s, now())"""
       
        cursor=connection.cursor()
        record = (accountID,investmentID,amount,plan)
        cursor.execute(query, record)
        connection.commit()
 
        message="[Investment Done!]"+' \u2713'
        note = fontstyle.apply(message, 'bold/Green/2UNDERLINE')
        print("\n",note,"\n")
 
    except mysql.connector.Error as error:
        print("Failed to Complete Investment {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
 
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
    return
 
def view_my_investments(userID,databasePassword):
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        query = """select i.AccountID,s.Name,i.InitialInvestment,i.CurrentAmount,i.EndDate
                    from investments as i
                    inner join
                    schemes as s
                    on i.InvestmentID=s.InvestmentID
                    where i.AccountID in (select AccountID from accounts where UserID=%s);"""
 
        cursor.execute(query,(userID,))
        record = cursor.fetchall()
       
        print("\n[",cursor.rowcount," Records Found...]\n")
       
        # print(tabulate(record, headers=["BankID","Address","Manager","Name","InterestRate","Established","Headquarters"]))
       
        x=PrettyTable()
        x.field_names=["AccountID","Scheme Name","Initial Investment","Current Amount","End Date(YYYY-MM-DD)"]
                           
        for row in record:
            x.add_row(row)
           
        print(x)
   
    except mysql.connector.Error as error:
        print("Failed to View Loans {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
 
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
    return

def withdraw_investment(userID,databasePassword):
    accountID=input("AccountID : ")
 
    verification=verify_account(userID,accountID,databasePassword)
    if(verification==False):
        message="[Wrong Account Number!]"
        note = fontstyle.apply(message, 'bold/red/2UNDERLINE')
        print("\n",note,"\n")
        return
    
    view_investment_schemes(databasePassword)

    investmentID=input("\nInvestmentID : ")

    message="[WARNING : Withdrawing From Investment Schemes Before Maturity May Lead to Forfeiture of Interest]"
    note = fontstyle.apply(message, 'bold/red/2UNDERLINE')
    print("\n",note,"\n")

    permission=input("Are you sure you want to continue[Y/N]? ")

    if(permission!='Y'):
        return
    
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
        cursor=connection.cursor()

        query="""select InitialInvestment from investments 
                where InvestmentID=%s and AccountID=%s"""
        params=(investmentID,accountID)
        cursor.execute(query,params)
 
        record=cursor.fetchall()
        amt=record[0][0]

        query = """Update accounts set Balance=Balance+
                (Select InitialInvestment from investments 
                where InvestmentID=%s and AccountID=%s)
                where AccountID=%s"""

        params=(investmentID,accountID,accountID)
        cursor.execute(query,params)
 
        query = """Delete from investments where InvestmentID=%s  and AccountID = %s"""

        params=(investmentID,accountID)
        cursor.execute(query,params)
        connection.commit()
        
        query="""select Name from schemes where InvestmentID=%s"""
        cursor.execute(query,(investmentID,))
 
        record=cursor.fetchall()
 
        plan=record[0][0]
        plan=plan+" Withdrawal"

        query = """INSERT INTO transactions (FromID,ToID,Amount,Purpose,Processed)
                VALUES (%s, %s, %s, %s, now())"""
       
        cursor=connection.cursor()
        record = (investmentID,accountID,amt,plan)
        cursor.execute(query, record)
        connection.commit()

        message="[Withdrawn Successfully! Principal Returned to Account.]"+' \u2713'
        note = fontstyle.apply(message, 'bold/yellow/2UNDERLINE')
        print("\n",note,"\n")
       
    except mysql.connector.Error as error:
        print("Failed to Withdraw: {}".format(error))
        connection.rollback()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
           
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
 
    return

def view_transaction_history(accountID, startDate, endDate, databasePassword):
    # Code to come
    message="[NOTE: Does not Track Fixed Periodic Inflow/Outflow of Salary/Interest/EMI]"
    note = fontstyle.apply(message, 'bold/yellow/2UNDERLINE')
    print("\n",note,"\n")
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        query = """create table TempHist
                  (TransactionID INT UNSIGNED NOT NULL,
                   Debit INT UNSIGNED,
                   Credit INT UNSIGNED,
                   Purpose varchar(256),
                   Processed datetime NOT NULL)"""
 
        result=cursor.execute(query)
       
        query="""Insert into TempHist (TransactionID,Debit,Purpose,Processed)
                (Select TransactionID,Amount,Purpose,Processed
                from transactions where FromID=%s
                and Processed>=%s AND Processed<=%s)"""
       
        params=(accountID,startDate,endDate)
        cursor.execute(query, params)
        connection.commit()
 
        query="""Insert into TempHist (TransactionID,Credit,Purpose,Processed)
                (Select TransactionID,Amount,Purpose,Processed
                from transactions where ToID=%s
                and Processed>=%s AND Processed<=%s)"""
       
        cursor.execute(query,params)
        connection.commit()
       
        query="""Update TempHist
                set Debit=0
                where Debit IS NULL"""
 
        cursor.execute(query)
        connection.commit()
 
        query="""Update TempHist
                set Credit=0
                where Credit IS NULL"""
 
        cursor.execute(query)
        connection.commit()
 
        query="""Select * from TempHist"""
 
        cursor.execute(query)
        record = cursor.fetchall()
 
        x=PrettyTable()
        x.field_names=["TransactionID","Debit","Credit","Description","Date/Time"]
                           
        for row in record:
            x.add_row(row)
        print(x)
 
        print("\n")
        query="""Select Sum(Debit),Sum(Credit) from TempHist"""
 
        cursor.execute(query)
        record = cursor.fetchall()
 
        x=PrettyTable()
        x.field_names=["Total Amount Debited","Total Amount Credited"]
                           
        for row in record:
            x.add_row(row)
        print(x)
 
        query="""drop table TempHist"""
        cursor.execute(query)
 
    except mysql.connector.Error as error:
        print("Failed to Complete Task {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
    return

def view_loan_rates(databasePassword):
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        sql_select_query = """select bk.Name,ln.InterestRate
                                from bank as bk
                                inner join
                                loaninfo as ln
                                on ln.BankID=bk.BankID
                                inner join
                                loantype as lt
                                on lt.TypeID=ln.TypeID
                                where lt.TypeID=%s"""
 
        print("Select Option for Interest Rates\n")
        menu = [["1", "Personal"], ["2", "Business"],["3","Education"],["4","Agricultural"],["5","Vehicle"],["6","Home"]]
        x=PrettyTable()
        x.field_names=["S.No.", "Option"]
        for row in menu:
            x.add_row(row)
        print(x)
 
        choice=input("\nChoice : ")
       
        cursor.execute(sql_select_query,(choice,))
        record = cursor.fetchall()
       
        print("\n[",cursor.rowcount," Records Found...]\n")
       
        # print(tabulate(record, headers=["BankID","Address","Manager","Name","InterestRate","Established","Headquarters"]))
       
        x=PrettyTable()
        x.field_names=["BankName","InterestRate"]
       
        for row in record:
            x.add_row(row)
           
        print(x)
   
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
   
    # print("\n")
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
    return
 
 
""" Admin Functions """
 
def add_user(userID,databasePassword):
    # code to come
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
        mySql_insert_query = """INSERT INTO user (UserID, Name, Address, Salary, PrimaryAccount, Password)
                                VALUES (%s, %s, %s, %s, %s, %s) """
 
        name=input("Name : ")
        address=input("Address : ")
        salary=input("Salary(Rs.) : ")
        primaryAccountID=input("Primary AccountID : ")
        # password=getpass.getpass(prompt="Password : ")
        password = stdiomask.getpass()
       
        encPassword=hashlib.sha256(password.encode()).hexdigest()
       
        cursor=connection.cursor()
        record = (userID, name, address, salary, primaryAccountID,encPassword)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
       
        message="[User Added!]"+' \u2713'
        note = fontstyle.apply(message, 'bold/Green/2UNDERLINE')
        print("\n",note,"\n")
   
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
   
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
 
 
    return
 
def add_account(accountID,databasePassword):
    # code to come
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
        mySql_insert_query = """INSERT INTO accounts (AccountID, Balance, UserID, BranchID, LastUpdate)
                                VALUES (%s, %s, %s, %s, %s) """
 
        balance=input("Balance : ")
        #interestRate=input("Interest Rate : ")
        userID=input("UserID : ")
        branchID=input("BranchID : ")
        #encPassword=hashlib.sha256(password.encode()).hexdigest()
       
        cursor=connection.cursor()
        record = (accountID,balance,userID,branchID,timestamp)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
       
        message="[Account Added!]"+' \u2713'
        note = fontstyle.apply(message, 'bold/Green/2UNDERLINE')
        print("\n",note,"\n")
   
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
   
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
 
 
    return
   
def remove_account(accountID,databasePassword):
    # Code to come
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
        cursor=connection.cursor()
 
        transferAccountID=input("Transfer Balance to(AccountID) : ")
 
        sql_update_query = """Update accounts set Balance=Balance+(Select Balance from (Select Balance from accounts where AccountID=%s) as bnc)"""
        cursor.execute(sql_update_query,(transferAccountID,))
 
        sql_Delete_query = """Delete from accounts where AccountID = %s"""
       
        cursor.execute(sql_Delete_query,(accountID,))
        connection.commit()
       
        message="[Account Deleted!]"+' \u2713'
        note = fontstyle.apply(message, 'bold/Green/2UNDERLINE')
        print("\n",note,"\n")
       
    except mysql.connector.Error as error:
        print("Failed to delete record from table: {}".format(error))
        connection.rollback()
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
           
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
 
 
    return
 
def update_user(userID,databasePassword):
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
        cursor=connection.cursor()
       
        menu = [["1", "Update Name"], ["2", "Update Address"], ["3","Update Salary/Fixed Income"], ["4","Change Primary AccountID"]]
        x=PrettyTable()
        x.field_names=["S.No.", "Option"]
        for row in menu:
            x.add_row(row)
        print(x)
 
        choice=int(input("\nChoice : "))
 
        param=()
        if(choice==1):
            sql_query="""update user set Name=%s where UserID=%s"""
            name=input("\nNew Name : ")
            param=(name,userID)
        elif(choice==2):
            sql_query="""update user set Address=%s where UserID=%s"""
            address=input("\nNew Address : ")
            param=(address,userID)
        elif(choice==3):
            sql_query="""update user set Salary=%s where UserID=%s"""
            salary=input("\nNew Salary : ")
            param=(salary,userID)
        elif(choice==4):
            sql_query="""update user set PrimaryAccount=%s where UserID=%s"""
            primaryAccountID=input("\nNew Primary AccountID : ")
            param=(primaryAccountID,userID)
 
        cursor.execute(sql_query,param)
        connection.commit()
        print("\n[",cursor.rowcount,"Records Updated]\n")
       
    except mysql.connector.Error as error:
        print("Failed to Update record from table: {}".format(error))
        connection.rollback()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
           
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
   
    return
 
def view_user_accounts(userID,databasePassword):
    # Code to come
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        sql_select_query = """select AccountID,Balance,BranchID,LastUpdate from accounts where UserId=%s"""
 
       
        cursor.execute(sql_select_query, (userID,))
        record = cursor.fetchall()
       
        print("\n[",cursor.rowcount," Records Found...]\n")
       
        # print(tabulate(record, headers=["AccountID","Balance","BranchID","LastUpdated"]))
       
        x=PrettyTable()
        x.field_names=["AccountID","Balance(Rs.)","BranchID","LastUpdated"]
       
        for row in record:
            x.add_row(row)
           
        print(x)
   
    except mysql.connector.Error as error:
        print("Failed to Fetch Records {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
 
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
 
 
    return
 
def view_account_info(accountID, databasePassword):

    verification=account_exists(accountID,databasePassword)
    if(verification==False):
        done = fontstyle.apply('AccountID Doesn\'t Exist', 'bold/red/2UNDERLINE')
        print("\n",done,"\n")

    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        query = """select UserID,Name,Address,Salary,PrimaryAccount from user where UserID=
                    (select UserID from accounts where accountID=%s)"""
 
       
        cursor.execute(query, (accountID,))
        record = cursor.fetchall()
 
        # print(tabulate(record, headers=["AccountID","Balance","BranchID","LastUpdated"]))
       
        x=PrettyTable()
        x.field_names=["UserID","Name","Address","Salary/Fixed Income(Rs.)","Primary AccountID"]
       
        for row in record:
            x.add_row(row)
           
        print(x)
   
    except mysql.connector.Error as error:
        print("Failed to Fetch Records {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
 
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
 
 
    return
 
def search_user(databasePassword):
    # Code to come
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()

        menu = [["1", "Search By UserID"],["2","Search by Name"]]
        x=PrettyTable()
        x.field_names=["S.No.", "Option"]
        for row in menu:
            x.add_row(row)
        print(x)

        choice=int(input("\nChoice : "))

        if(choice==1):
            userID=input("\nUserID : ")
            query = """select UserID,Name,Address,Salary,PrimaryAccount from user where UserID=%s"""
            cursor.execute(query,(userID,))
        elif(choice==2):
            name=input("\nName : ")
            name="%"+name+"%"
            query = """select UserID,Name,Address,Salary,PrimaryAccount from user where Name like %s"""
            cursor.execute(query,(name,))
        else:
            return
 
        record = cursor.fetchall()
       
        print("\n[",cursor.rowcount," Records Found...]\n")
       
        # print(tabulate(record, headers=["UserID", "Name", "Address", "Salary"]))
       
        x=PrettyTable()
        x.field_names=["UserID", "Name", "Address", "Salary/Fixed Monthly Income","Primary AccountID"]
       
        for row in record:
            x.add_row(row)
           
        print(x)
   
    except mysql.connector.Error as error:
        print("Failed to Fetch Records {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
   
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
 
 
    return

def view_users(databasePassword):
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        sql_select_query = """select UserID,Name,Address,Salary,PrimaryAccount from user"""
 
        cursor.execute(sql_select_query)
        record = cursor.fetchall()
       
        print("\n[",cursor.rowcount," Records Found...]\n")
       
        # print(tabulate(record, headers=["UserID", "Name", "Address", "Salary"]))
       
        x=PrettyTable()
        x.field_names=["UserID", "Name", "Address", "Salary/Fixed Monthly Income","Primary AccountID"]
       
        for row in record:
            x.add_row(row)
           
        print(x)
   
    except mysql.connector.Error as error:
        print("Failed to Fetch Records {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
   
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
 
 
    return

def view_branch_info(bankID,databasePassword):
    # Code to come
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        sql_select_query = """select Name from bank where BankID=%s"""
        cursor.execute(sql_select_query,(bankID,))
        record = cursor.fetchall()
       
        print("Name : ",record[0][0])
       
        sql_select_query = """select BranchID,Address,Manager from branch where BankID=%s"""
 
        cursor.execute(sql_select_query,(bankID,))
        record = cursor.fetchall()
       
        print("\n[",cursor.rowcount,"Records Found...]\n")
       
        # print(tabulate(record, headers=["BranchID","Address","Manager"]))
       
        x=PrettyTable()
        x.field_names=["BranchID","Address","Manager"]
       
        for row in record:
            x.add_row(row)
           
        print(x)
   
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
   
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
 
 
    return
 
def view_loan_amount(branchID,databasePassword):
    # Code to come
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        query = """select sum(Amount) from loans where BranchID=%s"""
 
        cursor.execute(query,(branchID,))
        record = cursor.fetchall()
       
        x=PrettyTable()
        x.field_names=["Total Loan Amount in Selected Branch (in Rs.)"]
       
        for row in record:
            x.add_row(row)
           
        print(x)
   
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
   
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
 
 
    return
 
def view_all_transaction_history(startDate,endDate,databasePassword):
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
       
        query="""select * from transactions
                where Processed>=%s and Processed<=%s"""

        params=(startDate,endDate)
        cursor.execute(query,params)
        record = cursor.fetchall()
 
        x=PrettyTable()
        x.field_names=["TransactionID","From","To", "Amount","Purpose","Date/Time"]
                           
        for row in record:
            x.add_row(row)
        print(x)

    except mysql.connector.Error as error:
        print("Failed to Complete Task {}".format(error))
        connection.rollback()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
    return
 
def view_linked_investments(databasePassword):
 
    view_investment_schemes(databasePassword)
 
    investmentID=input("InvestmentID : ")
 
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        sql_select_query = """select AccountID,InitialInvestment,CurrentAmount from investments where InvestmentID=%s"""
        cursor.execute(sql_select_query,(investmentID,))
        record = cursor.fetchall()
 
        print("\n[",cursor.rowcount,"Records Found...]\n")
       
        # print(tabulate(record, headers=["BranchID","Address","Manager"]))
       
        x=PrettyTable()
        x.field_names=["AccountID","Initial Investment","Current Amount"]
       
        for row in record:
            x.add_row(row)
           
        print(x)
   
    except mysql.connector.Error as error:
        print("Failed to Fetch Records {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
   
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
 
 
    return
 
def trace_transactions(transactionID,databasePassword):
    try:
        connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
       
        cursor=connection.cursor()
        query="""select FromID,ToID,Amount,Purpose,Processed from transactions where TransactionID=%s"""
 
        cursor.execute(query,(transactionID,))
        record=cursor.fetchall()
 
        x=PrettyTable()
        x.field_names=["From","To","Amount","Description","Time"]
        for row in record:
            x.add_row(row)
        print(x)
 
        if(len(record)==0):
            message="[Transaction Doesn't Exist!]"
            note = fontstyle.apply(message, 'bold/red/2UNDERLINE')
            print("\n",note,"\n")
            return
 
        account1=record[0][0]
        account2=record[0][1]
 
        query="""Select u.UserID,u.Name,u.Address,u.Salary,u.PrimaryAccount
                from accounts as a
                inner join
                user as u
                on a.UserID=u.UserID
                where a.AccountID=%s"""
 
        cursor.execute(query,(account1,))
        record=cursor.fetchall()
        x=PrettyTable()
        x.field_names=["UserID","Name","Address","Salary/Fixed Income","Primary AccountID"]
        print("\nSender:")
        for row in record:
            x.add_row(row)
        print(x)
 
        if(len(str(account2))==3):
            query="""Select Name,RateOfReturn
                    from schemes
                    where InvestmentID=%s"""
 
            cursor.execute(query,(account2,))
            record=cursor.fetchall()
            x=PrettyTable()
            x.field_names=["Scheme Name","Rate Of Return"]
            print("\nReceiver:")
            for row in record:
                x.add_row(row)
            print(x)
       
        else:
            query="""Select u.UserID,u.Name,u.Address,u.Salary,u.PrimaryAccount
                    from accounts as a
                    inner join
                    user as u
                    on a.UserID=u.UserID
                    where a.AccountID=%s"""
 
            cursor.execute(query,(account2,))
            record=cursor.fetchall()
            x=PrettyTable()
            x.field_names=["UserID","Name","Address","Salary/Fixed Income","Primary AccountID"]
            print("\nReceiver:")
            for row in record:
                x.add_row(row)
            print(x)
 
    except mysql.connector.Error as error:
        print("Failed to Get Records {}".format(error))
        connection.rollback()
         
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
   
    done = fontstyle.apply('[Done!]', 'bold/green/2UNDERLINE')
    print("\n",done,"\n")
 
    return
 
 
""" Controller Functions """
 
def user(databasePassword,userID):
    connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
   
    name=get_username(databasePassword,userID)
    name = fontstyle.apply(name, 'bold/darkcyan/2UNDERLINE')
    print("\n\nWelcome ",name,"..!\n")
    # print("\n")
   
    #MostBeautifulMenuTemplateEver
    menu = [["1", "View All My Accounts"], ["2", "View My Account"], ["3", "View All My Loans"], ["4", "View My Loan"], ["5","View Banks Linked to Us"],["6", "View Branch Info"],
            ["7", "View Investment Schemes"], ["8","View Loan Rates"],["9", "Transfer Money/Funds"], ["10","Invest Money"],["11","View My Investments"],
            ["12","Withdraw Investment"],["13", "List Transaction History"], ["14", "Return"]]
 
    x=PrettyTable()
    x.field_names=["S.No.", "Option"]
    for row in menu:
        x.add_row(row)
    print(x)
   
 
    print("\n")
 
    actionChoice=int(input("Choice : "))
   
    if(actionChoice==1):
        print("\n")
        #userID=input("UserID : ")
        view_my_accounts(userID,databasePassword)
   
    elif(actionChoice==2):
        print("\n")
        accountID=input("AccountID : ")
        verification=verify_account(userID,accountID,databasePassword)
        if(verification==False):
            message="[Wrong Account Number!]"
            note = fontstyle.apply(message, 'bold/red/2UNDERLINE')
            print("\n",note,"\n")
        else:
            view_my_account(userID,accountID,databasePassword)
 
    elif(actionChoice==3):
        print("\n")
        view_my_loans(userID,databasePassword)
 
    elif(actionChoice==4):
        print("\n")
        accountID=input("AccountID : ")
        verification=verify_account(userID,accountID,databasePassword)
        if(verification==False):
            message="[Wrong Account Number!]"
            note = fontstyle.apply(message, 'bold/red/2UNDERLINE')
            print("\n",note,"\n")
        else:
            view_loan(accountID,databasePassword)
    
    elif(actionChoice==5):
        print("\n")
        # branchID=input("BranchID : ")
        bank_info(databasePassword)

    elif(actionChoice==6):
        print("\n")
        branchID=input("BranchID : ")
        branch_info(branchID,databasePassword)
 
    elif(actionChoice==7):
        print("\n")
        #branchID=input("BranchID : ")
        view_investment_schemes(databasePassword)
        message="[NOTE: Few Investments are subject to Market Risks.\n The Rates of Returns are dependent on Market Conditions and may Change.\n Please make Informed and Calculated Decisions]"
        note = fontstyle.apply(message, 'bold/red/2UNDERLINE')
        print("\n",note,"\n")
 
    elif(actionChoice==8):
        print("\n")
        view_loan_rates(databasePassword)

    elif(actionChoice==9):
        print("\n")
        fromID=input("Your AccountID : ")
        toID=input("Receiver's AccountID : ")
        accountExists=account_exists(toID,databasePassword)

        if(accountExists==False):
            message="[AccountID Doesn't Exist!]"
            note = fontstyle.apply(message, 'bold/red/2UNDERLINE')
            print("\n",note,"\n")
        else:
            amt=input("Amount(Rs.) : ")
            send_money(userID,fromID,toID,amt,databasePassword)
 
    elif(actionChoice==10):
        print("\n")
        invest_money(userID,databasePassword)
   
    elif(actionChoice==11):
        print("\n")
        view_my_investments(userID,databasePassword)

    elif(actionChoice==12):
        print("\n")
        withdraw_investment(userID,databasePassword)
 
    elif(actionChoice==13):
        print("\n")
        accountID=input("AccountID : ")
        verification=verify_account(userID,accountID,databasePassword)
        if(verification==False):
            message="[Wrong Account Number!]"
            note = fontstyle.apply(message, 'bold/red/2UNDERLINE')
            print("\n",note,"\n")
        else:
            startDate=input("Start Date (YYYY-MM-DD) : ")
            endDate=input("End Date (YYYY-MM-DD) : ")
            view_transaction_history(accountID,startDate,endDate,databasePassword)
 
    elif(actionChoice==14):
        print("\n")
        return
       
    return
 
def admin(databasePassword):
    connection = mysql.connector.connect(host='localhost',database='finman',user='root',password=databasePassword)
   
    welcome = fontstyle.apply('Welcome Admin...!', 'bold/blue/2UNDERLINE')
    print("\n",welcome,"\n")#Blackie, Bulbs, Venom
    # print("\n")
    update_all_loans(databasePassword)
    update_balances(databasePassword)
    update_all_investments(databasePassword)
    
    done = fontstyle.apply('[All Records Refreshed and Updated]', 'bold/green/2UNDERLINE')
    print(done,"\n")
   
    #MostBeautifulMenuTemplateEver
    menu = [["1", "Add User"], ["2", "Add Account"], ["3", "Remove Account"], ["4","Update User Info"],["5", "View User Accounts"], ["6", "View All Users"],
            ["7","View User Info Linked to an Account"],["8","Search For User"],["9", "View Branch Info(Of Bank)"], ["10", "View Loan Amounts in a Branch"],
            ["11", "List Transaction History"], ["12","View Accounts Linked to an Investment"],["13","Trace Transactions with TransactionID"],
            ["14", "View Investment Schemes"], ["15", "Refresh/Update all records"], ["16", "Return"]]
 
    x=PrettyTable()
    x.field_names=["S.No.", "Option"]
    for row in menu:
        x.add_row(row)
    print(x)
   
    # print("\n")
    print("\n")
    actionChoice=int(input("Choice : "))
   
    if(actionChoice==1):
        print("\n")
        num=int(input("No. of Users : "))
        print("\n")
        i=0
        while(i<num):
            userID=input("UserID : ")
            add_user(userID,databasePassword)
            i=i+1
 
        done = fontstyle.apply('[Users Added]'+' \u2713', 'bold/blue/2UNDERLINE')
        print("\n", done, "\n")
   
    elif(actionChoice==2):
        print("\n")
        num=int(input("No. of Accounts : "))
        print("\n")
        i=0
        print("[Branch Info : ]\n")
        view_all_branch(databasePassword)
        while(i<num):
            accountID=input("AccountID : ")
            add_account(accountID,databasePassword)
            i=i+1
 
        done = fontstyle.apply('[Accounts Added]', 'bold/blue/2UNDERLINE')
        print("\n", done, "\n")
   
    elif(actionChoice==3):
        print("\n")
        accountID=input("AccountID : ")
        remove_account(accountID,databasePassword)
 
        done = fontstyle.apply('[Account Removed]', 'bold/blue/2UNDERLINE')
        print("\n", done, "\n")
 
    elif(actionChoice==4):
        print("\n")
        userID=input("UserID : ")
        update_user(userID,databasePassword)
 
        done = fontstyle.apply('[User Info Updated]', 'bold/blue/2UNDERLINE')
        print("\n", done, "\n")
       
    elif(actionChoice==5):
        print("\n")
        userID=input("UserID : ")
        view_user_accounts(userID,databasePassword)
       
    elif(actionChoice==6):
        view_users(databasePassword)
   
    elif(actionChoice==7):
        print("\n")
        accountID=input("AccountID : ")
        view_account_info(accountID,databasePassword)

    elif(actionChoice==8):
        print("\n")
        search_user(databasePassword)
 
    elif(actionChoice==9):
        print("\n")
        bankID=input("BankID : ")
        view_branch_info(bankID,databasePassword)
 
    elif(actionChoice==10):
        print("\n")
        branchID=input("BranchID : ")
        view_loan_amount(branchID,databasePassword)
    
    elif(actionChoice==11):
        print("\n")
        startDate=input("From(YYYY-MM-DD) : ")
        endDate=input("To(YYYY-MM-DD) : ")
        view_all_transaction_history(startDate,endDate,databasePassword)
    
    elif(actionChoice==12):
        print("\n")
        view_linked_investments(databasePassword)
 
    elif(actionChoice==13):
        print("\n")
        transactionID=input("TransactionID : ")
        trace_transactions(transactionID,databasePassword)
 
    elif(actionChoice==14):
        print("\n")
        view_investment_schemes(databasePassword)
        
    elif(actionChoice==15):
        print("\n")
        update_all_loans(databasePassword)
        update_balances(databasePassword)
        update_all_investments(databasePassword)
        done = fontstyle.apply('[All Records Refreshed and Updated]', 'bold/green/2UNDERLINE')
        print(done,"\n")
       
    elif(actionChoice==16):
        print("\n")
        return
    # Code to come
    return
 
if __name__ == "__main__":
   
    print(" ___  _        __  __                     ___            _ __  ___ .  .    ")
    print("| __|(_) _ _  |  \/  | __ _  _ _         / __| ___  _ _ | '_ \\  |  |\\/|")
    print("| _| | || ' \ | |\/| |/ _` || ' \       | (__ / _ \| '_|| .__/")
    print("|_|  |_||_||_||_|  |_|\__/_||_||_|       \___|\___/|_|  |_|   ")
   
    welcome = fontstyle.apply('WELCOME TO FINMAN CORP\u2122...!', 'bold/blue/2UNDERLINE')
    print("\n",welcome,"\n") #Blackie, Bulbs, Venom
    # print("\n")

    p69 = strikethrough("  An ERP that actually works :)")
    print(p69)


    p2 = fontstyle.apply('\u2713 '+'[Seamless, Hassle-free Experience]', 'bold/cyan/2UNDERLINE')
    print(p2)
    
    p3 = fontstyle.apply('\u2713 '+'[Features Like Never Before]', 'bold/cyan/2UNDERLINE')
    print(p3)

    p4 = fontstyle.apply('\u2713 '+'[Get Everything Done with Few Button Presses]', 'bold/cyan/2UNDERLINE')
    print(p4,"\n")

    p5 = fontstyle.apply('[Administrator\'s Side : ]', 'bold/cyan/2UNDERLINE')
    print(p5)

    p6 = fontstyle.apply('\u2713 '+'[Track Users and Their Accounts with ease]', 'bold/cyan/2UNDERLINE')
    print(p6)

    p7 = fontstyle.apply('\u2713 '+'[Track Bank Branches and Related Info]', 'bold/cyan/2UNDERLINE')
    print(p7)

    p8 = fontstyle.apply('\u2713 '+'[Track Transactions and Their History]', 'bold/cyan/2UNDERLINE')
    print(p8,"\n")

    p9 = fontstyle.apply('[User\'s Side : ]', 'bold/cyan/2UNDERLINE')
    print(p9)

    p10 = fontstyle.apply('\u2713 '+'[Keep Track of Multiple Accounts with ease]', 'bold/cyan/2UNDERLINE')
    print(p10)

    p11 = fontstyle.apply('\u2713 '+'[Efficient Handling of Periodic Inflow/Outflow of Funds(EMI,Income,Interests)]', 'bold/cyan/2UNDERLINE')
    print(p11)

    p12 = fontstyle.apply('\u2713 '+'[Transfer Funds and Invest Money with Ease]', 'bold/cyan/2UNDERLINE')
    print(p12)

    p13 = fontstyle.apply('\u2713 '+'[Track Investments and Transactions]', 'bold/cyan/2UNDERLINE')
    print(p13,"\n")

    p1 = fontstyle.apply('[NOTE: At Least ONE Administrator LogIn Required]', 'bold/yellow/2UNDERLINE')
    print(p1,"\n")
    exitChoice=1
    databasePassword=""
   
    line=[]
    with open('AdminInfo.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            line.append(row)
    #header = next(csvreader)
    file.close()
   
    while exitChoice==1:
       
        # print("1. Log In as Administrator")
        # print("2. Log In as User\n")
       
        #MostBeautifulMenuTemplateEver
        menu = [["1", "Login as Administrator"], ["2", "Login as User"]]
        x=PrettyTable()
        x.field_names=["S.No.", "Option"]
        for row in menu:
            x.add_row(row)
        print(x)
       
        logChoice=int(input("\nChoice: "))
       
        # print("\n")
       
        if(logChoice==1):
           
            i=0
            while(i<3):
                # databasePassword=getpass.getpass(prompt="DataBase Password : ")
                print("Database ", end = '')
                databasePassword = stdiomask.getpass()
                pw=hashlib.sha256(databasePassword.encode()).hexdigest()

                if(line[0][0]=="0"):
                    first=["1",pw]
                    with open('AdminInfo.csv', 'w') as csvfile:  
                        csvwriter = csv.writer(csvfile) 
                        csvwriter.writerow(first)

                    while True:
                        print
                        admin(databasePassword)
                        #MostBeautifulMenuTemplateEver
                        menu = [["1", "More Actions"], ["2", "Logout"]]
                        x=PrettyTable()
                        x.field_names=["S.No.", "Option"]
                        for row in menu:
                            x.add_row(row)
                        print(x)
                    
                        # print("\n1. More Actions")
                        # print("2. Log Out\n")
                    
                        actionChoice=int(input("\nChoice : "))
                        # print("\n")
                        if(actionChoice!=1):
                            print("\n[Logging Out...]\n")
                            break
                    break

                elif(line[0][0]=="1"):
                    ext=line[0][1]
                    if(pw==ext):
                        while True:
                            print
                            admin(databasePassword)
                            #MostBeautifulMenuTemplateEver
                            menu = [["1", "More Actions"], ["2", "Logout"]]
                            x=PrettyTable()
                            x.field_names=["S.No.", "Option"]
                            for row in menu:
                                x.add_row(row)
                            print(x)
                        
                            # print("\n1. More Actions")
                            # print("2. Log Out\n")
                        
                            actionChoice=int(input("\nChoice : "))
                            # print("\n")
                            if(actionChoice!=1):
                                message="[Logging Out...]"
                                note = fontstyle.apply(message, 'bold/purple/2UNDERLINE')
                                print("\n",note,"\n") 
                                break
                        break
                    else:
                        i=i+1
                        j=str(3-i)
                        message="[Wrong Password! "+j+" Tries Left]"
                        note = fontstyle.apply(message, 'bold/red/2UNDERLINE')
                        print("\n",note,"\n")
    
                        if i==3:
                            continue

        else:
            userID=""
            userID=input("User ID : ")
            userExists=user_exists(userID,databasePassword)
 
            if(userExists==True):
                i=0
            else:
                message="[User Does Not Exist!]"
                note = fontstyle.apply(message, 'bold/red/2UNDERLINE')
                print("\n",note,"\n")
                i=3
 
            while(i<3):
                # userPassword=getpass.getpass(prompt="Password : ")
                userPassword = stdiomask.getpass()
                pw=hashlib.sha256(userPassword.encode()).hexdigest()
               
                verification=verify_user(userID,databasePassword)
                if (pw==verification):
                    while True:
                        user(databasePassword,userID)
                       
                        #MostBeautifulMenuTemplateEver
                        menu = [["1", "More Actions"], ["2", "Logout"]]
                        x=PrettyTable()
                        x.field_names=["S.No.", "Option"]
                        for row in menu:
                            x.add_row(row)
                        print(x)
                       
                        actionChoice=int(input("\nChoice : "))
                        # print("\n")
                        if(actionChoice!=1):
                            message="[Logging Out...]"
                            note = fontstyle.apply(message, 'bold/purple/2UNDERLINE')
                            print("\n",note,"\n") 
                            break
                    break
                else:
                    i=i+1
                    j=str(3-i)
                    message="[Wrong Password! "+j+" Tries Left]"
                    note = fontstyle.apply(message, 'bold/red/2UNDERLINE')
                    print("\n",note,"\n")
                    if i==3:
                        continue
       
       
        menu = [["1", "Login Again"], ["2", "Exit"]]
        x=PrettyTable()
        x.field_names=["S.No.", "Option"]
        for row in menu:
            x.add_row(row)
        print(x)
       
        exitChoice=int(input("\nChoice : "))
        # print("\n")
   
    message="[Exiting...]"
    note = fontstyle.apply(message, 'bold/purple/2UNDERLINE')
    print("\n",note,"\n")    
    # Code to come
