
class Portfolio:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.groups = {}

    def __repr__(self):
        return f"Portfolio(name={self.name}, owner={self.owner}, groups={self.groups})"

    def add_group(self, group):
        if group.name in self.groups:
            print(f"Error: Group {group.name} already exists.")
        else:
            self.groups[group.name] = group

    def remove_group(self, group_name):
        if group_name in self.groups:
            del self.groups[group_name]
        else:
            print(f"Error: Group {group_name} not found.")

    def get_total_market_value(self):
        total_value = 0
        for group in self.groups.values():
            total_value += group.get_market_value()
        return total_value

    def list_holdings(self):
        all_holdings = []
        for group_name, group in self.groups.items():
            for security, quantity in group.list_holdings():
                all_holdings.append((group_name, security, quantity))
        return all_holdings

