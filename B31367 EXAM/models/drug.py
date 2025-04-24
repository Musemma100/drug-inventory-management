from datetime import date

class Drug:
    def __init__(self, name, drug_type, quantity, batch_number, expiry_date):
        self.name = name
        self.drug_type = drug_type
        self.__quantity = quantity
        self.batch_number = batch_number
        self.expiry_date = expiry_date

    def stock_in(self, amount):
        self.__quantity += amount

    def stock_out(self, amount):
        if amount <= self.__quantity:
            self.__quantity -= amount
        else:
            raise ValueError("Insufficient stock")

    def is_expired(self):
        return date.today() > self.expiry_date

    def is_low_stock(self):
        return self.__quantity < 10

    def get_quantity(self):
        return self.__quantity
