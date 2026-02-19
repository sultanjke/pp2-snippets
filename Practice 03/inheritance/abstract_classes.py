# =============================================================
# Abstract Base Classes (ABC)
# =============================================================
# An abstract class defines a "contract" — it declares methods
# that ALL child classes MUST implement. You cannot create an
# instance of an abstract class directly.
# =============================================================

from abc import ABC, abstractmethod


# Abstract base class — cannot be instantiated on its own
class Shape(ABC):
    def __init__(self, color="black"):
        self.color = color

    @abstractmethod
    def area(self):
        """Every shape must calculate its own area."""
        pass

    @abstractmethod
    def perimeter(self):
        """Every shape must calculate its own perimeter."""
        pass

    # Concrete method — inherited as-is by all children
    def describe(self):
        return (
            f"{self.__class__.__name__} (color={self.color}) | "
            f"area={self.area():.2f}, perimeter={self.perimeter():.2f}"
        )


# Each child MUST implement area() and perimeter(), otherwise
# Python raises TypeError when you try to instantiate it.

class Circle(Shape):
    PI = 3.14159

    def __init__(self, radius, color="black"):
        super().__init__(color)
        self.radius = radius

    def area(self):
        return Circle.PI * self.radius ** 2

    def perimeter(self):
        return 2 * Circle.PI * self.radius


class Rectangle(Shape):
    def __init__(self, width, height, color="black"):
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, side_a, side_b, side_c, color="black"):
        super().__init__(color)
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    def area(self):
        # Heron's formula
        s = self.perimeter() / 2
        return (s * (s - self.side_a) * (s - self.side_b) * (s - self.side_c)) ** 0.5

    def perimeter(self):
        return self.side_a + self.side_b + self.side_c


# Trying to instantiate the abstract class raises an error
print("--- Abstract class cannot be instantiated ---")
try:
    shape = Shape()
except TypeError as error:
    print(f"  Error: {error}")

# Child classes work because they implement all abstract methods
shapes = [
    Circle(radius=5, color="red"),
    Rectangle(width=4, height=7, color="blue"),
    Triangle(side_a=3, side_b=4, side_c=5, color="green"),
]

print(f"\n--- Shapes ---")
for shape in shapes:
    print(f"  {shape.describe()}")


# ---- Practical Application: Payment Processing System ----
# The abstract class ensures every payment method implements
# process() and validate(), so the system stays consistent.

class PaymentMethod(ABC):
    def __init__(self, account_holder):
        self.account_holder = account_holder

    @abstractmethod
    def validate(self):
        """Check if the payment method is valid."""
        pass

    @abstractmethod
    def process(self, amount):
        """Process a payment of the given amount."""
        pass

    def receipt(self, amount):
        method_name = self.__class__.__name__
        return f"  Receipt: ${amount:.2f} charged via {method_name} for {self.account_holder}"


class CreditCard(PaymentMethod):
    def __init__(self, account_holder, card_number, expiry_date):
        super().__init__(account_holder)
        self.card_number = card_number
        self.expiry_date = expiry_date

    def validate(self):
        # Simple check: card number must be 16 digits
        is_valid = len(self.card_number.replace("-", "")) == 16
        return is_valid

    def process(self, amount):
        if not self.validate():
            return f"  FAILED: Invalid card for {self.account_holder}"
        masked_card = "****-" + self.card_number[-4:]
        return f"  Charged ${amount:.2f} to card {masked_card}"


class BankTransfer(PaymentMethod):
    def __init__(self, account_holder, bank_name, account_number):
        super().__init__(account_holder)
        self.bank_name = bank_name
        self.account_number = account_number

    def validate(self):
        return len(self.account_number) >= 8

    def process(self, amount):
        if not self.validate():
            return f"  FAILED: Invalid account for {self.account_holder}"
        return f"  Transferred ${amount:.2f} via {self.bank_name}"


class DigitalWallet(PaymentMethod):
    def __init__(self, account_holder, wallet_id, balance):
        super().__init__(account_holder)
        self.wallet_id = wallet_id
        self.balance = balance

    def validate(self):
        return self.balance > 0

    def process(self, amount):
        if not self.validate() or amount > self.balance:
            return f"  FAILED: Insufficient wallet balance for {self.account_holder}"
        self.balance -= amount
        return f"  Deducted ${amount:.2f} from wallet {self.wallet_id} (remaining: ${self.balance:.2f})"


# Process payments through different methods using the same interface
payment_methods = [
    CreditCard("Sultan", "4532-1234-5678-9012", "12/27"),
    BankTransfer("Alice", "Kaspi Bank", "KZ12345678"),
    DigitalWallet("Bob", "wallet_bob_42", balance=200.00),
]

order_amount = 75.00

print(f"\n--- Processing ${order_amount:.2f} payments ---")
for method in payment_methods:
    print(method.process(order_amount))
    print(method.receipt(order_amount))
