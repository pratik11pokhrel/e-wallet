import wallet
import csv

TRANSACTION_RECORDS = 'account_transactions.csv'
USER_RECORDS = 'user_records.csv'


class Account:

    ''' This class provides multiple functionalities for a pre-existing user account. A UserID, and a transaction account is first needed to be able use this 
    class. The User ID can be generated from the Customer class, and the transacion account can be created using the NewAccount class.

    Usage:
        uid = 1001
        account_number = 3330000407 (optional)
        myaccount = Account(uid,account_number)

    Returns:
        An account object with functions to view details, deposit, withdraw, and transfer money.

    Example 1 (passing both UID and Account number):

        myaccount = Account(1001, 3330000407)

        myaccount.deposit(100)
        > Deposits money (Rs. 100) to account number 1001.

        myaccount.withdraw(50)
        > Withdraws money (Rs. 50) from account number 1001.


    Example 2 (without passing in the Account number):

        youraccount = newAccount(1002)

        youraccount.deposit(100)
        youraccount.view_balance()
        youraccount.view_account_details()

    '''

    _attributes = ("UID", "Account Number", "Balance")

    def __init__(self, usr_id, acc_number=None):

        self.usr_id = usr_id
        self.acc_number = acc_number
        if self.acc_number is None:
            self.acc_number = self._get_account_number()

    def _get_account_number(self, uid=None):

        if not uid:
            uid = self.usr_id
        with open(TRANSACTION_RECORDS, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row:
                    if int(row[0]) == int(uid):
                        return row[1]
        print("Account not found. Please create a new account using the newAccount option.")

    def view_account_details(self):

        with open(TRANSACTION_RECORDS, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row:
                    if int(row[0]) == int(self.usr_id):
                        details = dict(zip(self._attributes[1:], row[1:]))

        for keys, values in details.items():
            print("{} : {}".format(keys, values))

    def view_balance(self, uid=None):

        if not uid:
            uid = self.usr_id

        with open(TRANSACTION_RECORDS, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row:
                    if int(row[0]) == int(uid):
                        return row[2]
        print("Error occurred. Please contact support.")


    def deposit(self, amount):
        try:
            with open ("account_transactions.csv", 'r+', newline='') as file:
                reader = csv.reader(file)
                next(reader) 
                rows = list(reader)
                if not rows:
                    print("Transaction records are empty. Please create a new account using the newAccount option.")
                    return
                for row in rows:
                    if row and int(row[0]) == int(self.usr_id):
                        current_balance = int(row[2])
                        updated_balance = current_balance + amount
                        row[2] = updated_balance
                        file.seek(0)  # Move file pointer to the beginning
                        file.truncate()  # Clear the remaining content in the file
                        writer = csv.writer(file)
                        writer.writerow(['UID', 'ACNumber', 'Balance'])
                        writer.writerows(rows)

                        break
                else:
                    print("Account not found. Please create a new account using the newAccount option.")
                    return

            print(f"Deposited: Rs. {amount}")
            print(f"Updated Balance: Rs. {updated_balance}")
        except FileNotFoundError:
            print("Error: File not found.")
        except ValueError:
            print("Error: Invalid value encountered.")




    def withdraw(self, amount):
        try:
            with open("account_transactions.csv", 'r+', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                rows = list(reader)
                if not rows:
                    print("Transaction records are empty. Please create a new account using the newAccount option.")
                    return
                for row in rows:
                    if row and int(row[0]) == int(self.usr_id):
                        current_balance = int(row[2])
                        if amount <= current_balance:
                            updated_balance = current_balance - amount
                            row[2] = updated_balance
                            file.seek(0)  # Move file pointer to the beginning
                            file.truncate()  # Clear the remaining content in the file
                            writer = csv.writer(file)
                            writer.writerow(['UID', 'ACNumber', 'Balance'])
                            writer.writerows(rows)

                            break
                        else:
                            print("Insufficient balance.")
                            return
                else:
                    print("Account not found. Please create a new account using the newAccount option.")
                    return

            print(f"Deposited: Rs. {amount}")
            print(f"Updated Balance: Rs. {updated_balance}")
            
            
        except FileNotFoundError:
            print("Error: File not found.")
        except ValueError:
            print("Error: Invalid value encountered.")


    def transfer_funds(self, uid, amount):
        try:
            with open("account_transactions.csv", 'r+', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                rows = list(reader)
                if not rows:
                    print("Transaction records are empty. Please create a new account using the newAccount option.")
                    return
                from_account_found = False
                to_account_found = False
                for row in rows:
                    if row and int(row[0]) == int(self.usr_id):
                        current_balance = int(row[2])
                        if amount <= current_balance:
                            updated_balance = current_balance - amount
                            row[2] = updated_balance
                            from_account_found = True
                            break
                        else:
                            print("Insufficient balance.")
                            return
                else:
                    print("Account not found. Please create a new account using the newAccount option.")
                    return

                for row in rows:
                    if row and int(row[0]) == int(uid):
                        current_balance = int(row[2])
                        updated_balance = current_balance + amount
                        row[2] = updated_balance
                        to_account_found = True
                        break

                if not from_account_found:
                    print("Account not found. Please create a new account using the newAccount option.")
                    return

                if not to_account_found:
                    print("To-account not found.")
                    return

                file.seek(0)  # Move file pointer to the beginning
                file.truncate()  # Clear the remaining content in the file
                writer = csv.writer(file)
                writer.writerow(['UID', 'ACNumber', 'Balance'])
                writer.writerows(rows)


            print(f"Transferred: Rs. {amount} from account number {self.usr_id} to account number {uid}")
            print(f"Updated Balance for account number {self.usr_id}: Rs. {updated_balance}")
            print(f"Updated Balance for account number {uid}: Rs. {updated_balance}")
        
        except FileNotFoundError:
            print("Error: File not found.")
        except ValueError:
            print("Error: Invalid value encountered.")
