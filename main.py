class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
        if not self.check_funds(amount):
            return False
        self.ledger.append({'amount': -amount, 'description': description})
        return True

    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    def transfer(self, amount, category):
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, f'Transfer to {category.name}')
        category.deposit(amount, f'Transfer from {self.name}')
        return True

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        lines = [self.name.center(30, '*')]
        for item in self.ledger:
            description = item['description'][:23]
            amount = f"{item['amount']:.2f}"[:7]
            lines.append(f"{description:<23}{amount:>7}")
        lines.append(f"Total: {self.get_balance():.2f}")
        return "\n".join(lines)


def create_spend_chart(categories):
    spent = [
        sum(-item['amount'] for item in category.ledger if item['amount'] < 0)
        for category in categories
    ]
    total = sum(spent)

    if total == 0:
        percentages = [0] * len(categories)
    else:
        percentages = [int((s * 100 // total) // 10 * 10) for s in spent]

    lines = ["Percentage spent by category"]

    for level in range(100, -1, -10):
        row = f"{level:>3}|"
        for percent in percentages:
            row += " o " if percent >= level else "   "
        row += " "
        lines.append(row)

    lines.append("    " + "-" * (3 * len(categories) + 1))

    names = [category.name for category in categories]
    longest = max(len(name) for name in names)

    for i in range(longest):
        row = "     "
        for name in names:
            row += (name[i] if i < len(name) else " ") + "  "
        lines.append(row)

    return "\n".join(lines)


if __name__ == "__main__":
    food = Category('Food')
    food.deposit(1000, 'initial deposit')
    food.withdraw(10.15, 'groceries')
    food.withdraw(15.89, 'restaurant and more food for dessert')
    clothing = Category('Clothing')
    food.transfer(50, clothing)
    print(food)

    auto = Category('Auto')
    auto.deposit(1000, 'deposit')
    auto.withdraw(100, 'gas')
    print(create_spend_chart([food, clothing, auto]))
