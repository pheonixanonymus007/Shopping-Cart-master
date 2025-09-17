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
        total = 0
        for product, qty in self.cart:
            cost = product.price * qty
            total += cost
            print(f"- {product.name} x{qty} = ₹{cost}")
        print(f"Total = ₹{total}\n")
        return total

    def checkout(self):
        total = self.show_cart()
        print("💳 Processing payment...")
        print("🎉 Thank you for shopping with us!")
        self.cart.clear()

def main():
    store = Store("CLI Couture")
    store.add_product(Product(1, "Hoodie", 1500, 10))
    store.add_product(Product(2, "Jeans", 2000, 5))
    store.add_product(Product(3, "Shoes", 3000, 8))
    store.add_product(Product(4, "T-Shirt", 800, 15))

    while True:
        print("\n===== CLI Couture Menu =====")
        print("1. Show Products")
        print("2. Add to Cart")
        print("3. View Cart")
        print("4. Checkout")
        print("5. Exit")

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
            print("👋 Goodbye, stylish soul!")
            sys.exit()
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
