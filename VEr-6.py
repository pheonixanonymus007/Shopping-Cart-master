import sys

class Product:
    def __init__(self, pid, name, price, stock):
        self.pid = pid
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.pid}. {self.name} - ₹{self.price} ({self.stock} in stock)"

class Store:
    def __init__(self, name):
        self.name = name
        self.products = []
        self.cart = []

    def add_product(self, product):
        self.products.append(product)

    def show_products(self):
        print(f"\n🧥 Welcome to {self.name} Collection 🧥")
        for product in self.products:
            print(product)

    def add_to_cart(self, pid, qty):
        for product in self.products:
            if product.pid == pid:
                if product.stock >= qty:
                    self.cart.append((product, qty))
                    product.stock -= qty
                    print(f"✅ Added {qty} x {product.name} to cart.")
                else:
                    print("❌ Not enough stock.")
                return
        print("❌ Product not found.")

    def show_cart(self):
        print("\n🛒 Your Cart:")
        if not self.cart:
            print("Cart is empty!")
            return 0
        total = 0
        for product, qty in self.cart:
            cost = product.price * qty
            total += cost
            print(f"- {product.name} x{qty} = ₹{cost}")
        print(f"Total = ₹{total}\n")
        return total

    def checkout(self):
        total = self.show_cart()
        if total > 0:
            print("💳 Processing payment...")
            print("🎉 Thank you for shopping with us!")
            self.cart.clear()

# 🔹 Load products from products.txt
def load_products_from_file(filename):
    products = []
    try:
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    pid, name, price, stock = parts
                    products.append(Product(int(pid), name, int(price), int(stock)))
    except FileNotFoundError:
        print(f"❌ File '{filename}' not found. Starting with empty store.")
    return products

# 🔹 Load users from users.txt
def load_users(filename):
    users = {}
    try:
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    username, password = parts
                    users[username] = password
    except FileNotFoundError:
        print(f"❌ File '{filename}' not found. No users available.")
    return users

# 🔹 Login function
def login(users):
    while True:
        print("\n===== Login =====")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        if username in users and users[username] == password:
            print(f"✅ Welcome, {username}!")
            return username
        else:
            print("❌ Invalid username or password. Try again.")

def main():
    store = Store("CLI Couture")

    # Load products
    for product in load_products_from_file("products.txt"):
        store.add_product(product)

    # Load users
    users = load_users("users.txt")

    current_user = None

    while True:
        # Force login if not logged in
        if not current_user:
            current_user = login(users)

        print("\n===== CLI Couture Menu =====")
        print("1. Show Products")
        print("2. Add to Cart")
        print("3. View Cart")
        print("4. Checkout")
        print("5. Logout")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            store.show_products()
        elif choice == "2":
            try:
                pid = int(input("Enter product ID: "))
                qty = int(input("Enter quantity: "))
                store.add_to_cart(pid, qty)
            except ValueError:
                print("❌ Invalid input.")
        elif choice == "3":
            store.show_cart()
        elif choice == "4":
            store.checkout()
        elif choice == "5":
            print(f"👋 Logged out, {current_user}.")
            current_user = None
        elif choice == "6":
            print("👋 Goodbye, stylish soul!")
            sys.exit()
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
