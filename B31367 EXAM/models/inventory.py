class Inventory:
    def __init__(self):
        self.drugs = {}

    def add_drug(self, drug):
        self.drugs[drug.batch_number] = drug

    def get_drug(self, batch_number):
        return self.drugs.get(batch_number)

    def all_drugs(self):
        return list(self.drugs.values())
