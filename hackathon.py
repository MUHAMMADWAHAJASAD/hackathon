import random
import os

class Account:
    def __init__(self, number, holder):
        self.number = number
        self.holder = holder
        self.balance = 0
        self.history = []
        self.withdrawal_count = 0
        
    def add(self, amount):
        if amount > 0:
            self.balance += amount
            self.log(f"Deposit: +${amount}")
            return True
        return False
    
    def sub(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.withdrawal_count += 1
            receipt_id = f"WD{self.number}{self.withdrawal_count}"
            self.log(f"Withdrawal: -${amount}")
            self._save_withdrawal_receipt(amount, receipt_id)
            return True
        return False
    
    def get_balance(self):
        return self.balance
    
    def log(self, description):
        self.history.append(f"{description} - Balance: ${self.balance}")
    
    def show_history(self):
        return "\n".join(self.history)
    
    def _save_withdrawal_receipt(self, amount, receipt_id):
        receipt_content = f"""
=== Withdrawal Receipt ===
Receipt ID: {receipt_id}
Account: {self.number}
Account Holder: {self.holder}
Amount: ${amount}
Remaining Balance: ${self.balance}
========================
"""
        # Ensure the directory exists
        if not os.path.exists('withdrawals'):
            os.makedirs('withdrawals')
        
        # Save the receipt as "receipt.txt"
        filename = "withdrawals/receipt.txt"
        with open(filename, "w") as f:
            f.write(receipt_content)

class Bank:
    def __init__(self):
        self.accounts = {}
    
    def new_account(self, holder):
        number = str(random.randint(10000, 99999))
        while number in self.accounts:
            number = str(random.randint(10000, 99999))
        
        account = Account(number, holder)
        self.accounts[number] = account
        return number
    
    def get(self, number):
        return self.accounts.get(number)
    
    def transfer(self, from_acc, to_acc, amount):
        sender = self.get(from_acc)
        receiver = self.get(to_acc)
        
        if sender and receiver and sender.sub(amount):
            receiver.add(amount)
            return True
        return False
    
    def total_balance(self):
        return sum(acc.balance for acc in self.accounts.values())
    
    def total_accounts(self):
        return len(self.accounts)

def main():
    bank = Bank()
    
    while True:
        print("\n=== Banking Menu ===")
        print("1. New Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Transfer")
        print("6. Statement")
        print("7. Admin: Total Balance")
        print("8. Admin: Account Count")
        print("9. Exit")
        
        choice = input("Choice (1-9): ")
        
        if choice == '1':
            name = input("Name: ")
            num = bank.new_account(name)
            print(f"Account created! Number: {num}")
        
        elif choice in ['2', '3', '4', '5', '6']:
            num = input("Account number: ")
            acc = bank.get(num)
            
            if acc:
                if choice == '2':
                    amt = float(input("Deposit amount: $"))
                    if acc.add(amt):
                        print("Success!")
                    else:
                        print("Invalid amount!")
                
                elif choice == '3':
                    amt = float(input("Withdrawal amount: $"))
                    if acc.sub(amt):
                        print("Success! Receipt saved in withdrawals/receipt.txt.")
                    else:
                        print("Insufficient funds or invalid amount!")
                
                elif choice == '4':
                    print(f"Balance: ${acc.get_balance()}")
                
                elif choice == '5':
                    to_acc = input("Recipient account: ")
                    amt = float(input("Amount: $"))
                    if bank.transfer(num, to_acc, amt):
                        print("Transfer complete!")
                    else:
                        print("Transfer failed!")
                
                elif choice == '6':
                    print("\n=== Statement ===")
                    print(acc.show_history())
            else:
                print("Account not found!")
        
        elif choice == '7':
            print(f"Total in bank: ${bank.total_balance()}")
        
        elif choice == '8':
            print(f"Total accounts: {bank.total_accounts()}")
        
        elif choice == '9':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
