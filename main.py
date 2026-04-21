class CustomerManager:
    def __init__(self):
        self.customers = {}
        self.tax_rate = 0.2
        self.tax_threshold = 100
        self.discount_threshold = 500

    def add_customer(self, name, purchases):
        if name in self.customers:
            self.customers[name].extend(purchases)
        else:
            self.customers[name] = purchases

    def add_purchase(self, name, purchase):
        self.add_customer(name, [purchase])

    def add_purchases(self, name, purchases):
        self.add_customer(name, purchases)

    def _purchase_price_with_tax(self, purchase):
        price = purchase["price"]
        if price > self.tax_threshold:
            return price * (1 + self.tax_rate)
        return price

    def _total_spend(self, purchases):
        total = 0
        for purchase in purchases:
            total += self._purchase_price_with_tax(purchase)
        return total

    def _discount_message(self, total_spend):
        if total_spend > self.discount_threshold:
            return "Eligible for discount"
        if total_spend > 300:
            return "Potential future discount customer"
        return "No discount"

    def _priority_message(self, total_spend):
        if total_spend > 1000:
            return "VIP Customer!"
        if total_spend > 800:
            return "Priority Customer"
        return None

    def generate_report(self):
        for customer_name, purchases in self.customers.items():
            total_spend = self._total_spend(purchases)
            print(customer_name)
            print(self._discount_message(total_spend))
            priority_message = self._priority_message(total_spend)
            if priority_message is not None:
                print(priority_message)

    def calculate_shipping_fee(self, purchases):
        return calculate_shipping_fee_for_heavy_items(purchases)


def _any_purchase_matches(purchases, predicate):
    for purchase in purchases:
        if predicate(purchase):
            return True
    return False

def calculate_shipping_fee_for_heavy_items(purchases):
    if _any_purchase_matches(purchases, lambda p: p.get("weight", 0) > 20):
        return 50
    return 20

def calculate_shipping_fee_for_fragile_items(purchases):
    if _any_purchase_matches(purchases, lambda p: p.get("fragile", False)):
        return 60
    return 25

flat_tax = 0.2
