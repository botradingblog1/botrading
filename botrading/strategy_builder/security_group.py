
class SecurityGroup:
    def __init__(self, name):
        self.name = name
        self.security_map = {}  # symbol -> Security

    def __repr__(self):
        return f"SecurityGroup(name={self.name}, security_map={self.security_map})"

    def add_security(self, security, quantity):
        self.security_map[security.symbol] = security

    def remove_security(self, symbol):
        if symbol in self.security_map:
            del self.security_map[symbol]
        else:
            print(f"Error: {symbol} not found in security_map.")

    def list_security_map(self):
        return [security for security in self.security_map.values()]
