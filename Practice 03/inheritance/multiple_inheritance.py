# =============================================================
# Multiple Inheritance
# =============================================================
# A child class can inherit from MORE than one parent.
# Python uses the Method Resolution Order (MRO) to decide
# which parent's method to call when there's a conflict.
# =============================================================


# Two independent parent classes
class Swimmer:
    def __init__(self):
        self.can_swim = True

    def swim(self):
        return f"{self.name} swims through the water."


class Flyer:
    def __init__(self):
        self.can_fly = True

    def fly(self):
        return f"{self.name} soars through the sky."


# Duck inherits from BOTH Swimmer and Flyer
class Duck(Swimmer, Flyer):
    def __init__(self, name):
        self.name = name
        Swimmer.__init__(self)
        Flyer.__init__(self)

    def quack(self):
        return f"{self.name} says: Quack!"


donald = Duck("Donald")
print(donald.swim())
print(donald.fly())
print(donald.quack())
print(f"Can swim: {donald.can_swim}, Can fly: {donald.can_fly}")


# ---- MRO: Method Resolution Order ----
# When multiple parents have the same method name, Python follows
# the MRO (left-to-right, depth-first) to pick one.

class A:
    def greet(self):
        return "Hello from A"

class B(A):
    def greet(self):
        return "Hello from B"

class C(A):
    def greet(self):
        return "Hello from C"

class D(B, C):
    pass  # Doesn't override greet — which parent wins?


instance_d = D()
print(f"\n--- MRO demonstration ---")
print(f"D.greet() -> {instance_d.greet()}")  # B wins (listed first)
print(f"MRO: {[cls.__name__ for cls in D.__mro__]}")


# ---- Cooperative multiple inheritance with super() ----
# super() follows the MRO chain so every parent gets called once.

class Base:
    def __init__(self):
        self.initialized_by = ["Base"]

class Left(Base):
    def __init__(self):
        super().__init__()
        self.initialized_by.append("Left")

class Right(Base):
    def __init__(self):
        super().__init__()
        self.initialized_by.append("Right")

class Child(Left, Right):
    def __init__(self):
        super().__init__()
        self.initialized_by.append("Child")


child_obj = Child()
print(f"\n--- Cooperative super() chain ---")
print(f"Init order: {child_obj.initialized_by}")
print(f"MRO: {[cls.__name__ for cls in Child.__mro__]}")


# ---- Practical Application: Role-Based User System ----
# Mixin classes add specific capabilities; the final class
# combines them into a complete user role.

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def display_info(self):
        return f"{self.username} ({self.email})"


# Mixins — small focused classes that add one capability each
class ContentCreatorMixin:
    def create_post(self, title):
        return f"[POST] '{title}' created by {self.username}"

    def edit_post(self, title):
        return f"[EDIT] '{title}' edited by {self.username}"


class ModeratorMixin:
    def ban_user(self, target_username):
        return f"[BAN] {self.username} banned {target_username}"

    def delete_post(self, title):
        return f"[DELETE] '{title}' removed by {self.username}"


class AnalyticsMixin:
    def view_analytics(self):
        return f"[ANALYTICS] {self.username} accessed the dashboard"


# Combining mixins to build different roles
class Editor(User, ContentCreatorMixin):
    role = "Editor"

class Moderator(User, ModeratorMixin):
    role = "Moderator"

class Admin(User, ContentCreatorMixin, ModeratorMixin, AnalyticsMixin):
    role = "Admin"


editor = Editor("sultan", "sultan@example.com")
moderator = Moderator("alice_mod", "alice@example.com")
admin = Admin("super_admin", "admin@example.com")

print(f"\n--- Role-Based Actions ---")
print(f"\n  {editor.role}: {editor.display_info()}")
print(f"    {editor.create_post('Python Tips')}")

print(f"\n  {moderator.role}: {moderator.display_info()}")
print(f"    {moderator.ban_user('spammer42')}")
print(f"    {moderator.delete_post('Spam Post')}")

print(f"\n  {admin.role}: {admin.display_info()}")
print(f"    {admin.create_post('Announcement')}")
print(f"    {admin.delete_post('Bad Content')}")
print(f"    {admin.view_analytics()}")
