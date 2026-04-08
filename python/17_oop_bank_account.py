# Python Program 17: OOP — Bank Account System
# Author: Lydia S. Makiwa
# Description: Demonstrates classes, encapsulation, and methods

class BankAccount:
    bank_name = "Lydia National Bank"
    total_accounts = 0

    def __init__(self, owner, balance=0):
        self.__owner   = owner          # private attribute
        self.__balance = balance
        BankAccount.total_accounts += 1
        self.__transactions = []

    def deposit(self, amount):
        if amount <= 0:
            print("❌ Deposit amount must be positive.")
            return
        self.__balance += amount
        self.__transactions.append(f"+R{amount:.2f}")
        print(f"✅ Deposited R{amount:.2f}. Balance: R{self.__balance:.2f}")

    def withdraw(self, amount):
        if amount > self.__balance:
            print(f"❌ Insufficient funds! Balance: R{self.__balance:.2f}")
            return
        self.__balance -= amount
        self.__transactions.append(f"-R{amount:.2f}")
        print(f"✅ Withdrew R{amount:.2f}. Balance: R{self.__balance:.2f}")

    def get_balance(self):
        return self.__balance

    def statement(self):
        print(f"\n{'='*35}")
        print(f"  {BankAccount.bank_name}")
        print(f"  Account Holder: {self.__owner}")
        print(f"  Balance: R{self.__balance:.2f}")
        print(f"  Transactions: {', '.join(self.__transactions) or 'None'}")
        print(f"{'='*35}")

    @classmethod
    def get_total_accounts(cls):
        return cls.total_accounts


# Demo
acc1 = BankAccount("Lydia Makiwa", 1000)
acc2 = BankAccount("Alice Johnson", 500)

acc1.deposit(500)
acc1.withdraw(200)
acc1.withdraw(2000)
acc1.statement()

print(f"\nTotal accounts: {BankAccount.get_total_accounts()}")
