class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        """
        A deposit method that accepts an amount and description. 
        If no description is given, it should default to an empty string. 
        The method should append an object to the ledger list in the form of {"amount": amount, "description": description}.
        """
        self.ledger.append({"amount": amount, "description": description})

    def get_balance(self):
        """
        A get_balance method that returns the current balance of the budget category based on the deposits and withdrawals that have occurred.
        """
        balance = 0
        for entry in self.ledger:
            balance += entry["amount"]
        return balance

    def check_funds(self, amount):
        """
        A check_funds method that accepts an amount as an argument. 
        It returns False if the amount is greater than the balance of the budget category and returns True otherwise. 
        This method should be used by both the withdraw method and transfer method.
        """
        return self.get_balance() >= amount

    def withdraw(self, amount, description=""):
        """
        A withdraw method that is similar to the deposit method, but the amount passed in should be stored in the ledger as a negative number. 
        If there are not enough funds, nothing should be added to the ledger. 
        This method should return True if the withdrawal took place, and False otherwise.
        """
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def transfer(self, amount, transfer_to):
        """
        A transfer method that accepts an amount and another budget category as arguments. 
        The method should add a withdrawal with the amount and the description "Transfer to [Destination Budget Category]". 
        The method should then add a deposit to the other budget category with the amount and the description "Transfer from [Source Budget Category]". 
        If there are not enough funds, nothing should be added to either ledgers. 
        This method should return True if the transfer took place, and False otherwise.
        """
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {transfer_to.name}")
            transfer_to.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def __str__(self):
        # Calculate the total width of the budget name field
        name_field_width = 30 - len(self.name)
    
        # Calculate the number of * characters to add to either side of the budget name
        name_field_padding = name_field_width // 2
    
        # Create the title line with the budget name centered
        title_line = "*" * name_field_padding + self.name + "*" * name_field_padding
    
        # Create a list of the ledger lines
        ledger_lines = []
        
        # Format the description and amount fields
        for entry in self.ledger:
            description = entry["description"][:23].ljust(23)
            amount_str = f'{entry["amount"]:7.2f}'
            ledger_lines.append(f'{description}{amount_str}')
    
        # Create the balance line
        balance_line = f'Total:{self.get_balance():7.2f}'
    
        # Return the budget display with all the lines separated by newlines
        return f'{title_line}\n' + '\n'.join(ledger_lines) + f'\n{balance_line}'



def create_spend_chart(categories):
    # Create the chart title
    title = 'Percentage spent by category\n'
    
    # Determine spend amounts for each category
    spend_amount = []
    for category in categories:
        spend = 0
        for item in category.ledger:
            if item['amount'] < 0:
                spend += item['amount']
        spend_amount.append(round(spend, 2))

    # Calculate the percentage of each
    total = sum(spend_amount)
    spend_percentage = list(map(lambda amount: int((((amount/total) * 10) // 1) * 10), spend_amount))

    chart = ''
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spend_percentage:
            if percent >= value:
                chart += ' o '
            else:
                chart += '   '
        chart += ' \n'

    footer = '    ' + '-' * ((3 * len(categories)) + 1) + '\n'
    descriptions = list(map(lambda category: category.name, categories))
    max_length = max(map(lambda name: len(name), descriptions))
    descriptions = list(map(lambda name: name.ljust(max_length), descriptions))

    for x in zip(*descriptions):
        footer += '    ' + "".join(map(lambda s: s.center(3), x)) + ' \n'

    return (title + chart + footer).rstrip('\n')