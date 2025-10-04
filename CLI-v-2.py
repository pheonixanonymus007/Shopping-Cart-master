import sys, os, csv, getpass

USERS_FILE, PRODUCTS_FILE = "users.txt", "products.txt"

def clear_screen():
    """
    Clears the console screen.
    Uses 'cls' for Windows and 'clear' for Unix-based systems.
    """
    os.system("cls" if os.name == "nt" else "clear")

def show_logo():
    """
    Prints the ASCII art logo and a welcome message for the store.
    """
    print("""   
    __| |_______________________________________________________________________________| |__
__   _______________________________________________________________________________   __
  | |                                                                               | |  
  | |██████╗ ██╗██╗   ██╗ █████╗ ███████╗                                           | |  
  | |██╔══██╗██║╚██╗ ██╔╝██╔══██╗██╔════╝                                           | |  
  | |██║  ██║██║ ╚████╔╝ ███████║███████╗                                           | |  
  | |██║  ██║██║  ╚██╔╝  ██╔══██║╚════██║                                           | |  
  | |██████╔╝██║   ██║   ██║  ██║███████║                                           | |  
  | |╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝                                           | |  
  | |                                                                               | |  
  | | ██████╗██╗      ██████╗ ████████╗██╗  ██╗    ███████╗██╗  ██╗ ██████╗ ██████╗ | |  
  | |██╔════╝██║     ██╔═══██╗╚══██╔══╝██║  ██║    ██╔════╝██║  ██║██╔═══██╗██╔══██╗| |  
  | |██║     ██║     ██║   ██║   ██║   ███████║    ███████╗███████║██║   ██║██████╔╝| |  
  | |██║     ██║     ██║   ██║   ██║   ██╔══██║    ╚════██║██╔══██║██║   ██║██╔═══╝ | |  
  | |╚██████╗███████╗╚██████╔╝   ██║   ██║  ██║    ███████║██║  ██║╚██████╔╝██║     | |  
  | | ╚═════╝╚══════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     | |  
__| |_______________________________________________________________________________| |__
__   _______________________________________________________________________________   __
  | |                                                                               | |  
    """)
    print("\n✨ Welcome to Diya's cloth shop ✨\n")

def refresh_screen():
    """
    Clears the screen and then displays the store logo.
    """
    clear_screen()
    show_logo()

def load_users():
    """
    Reads user credentials from the 'users.txt' file.
    Returns:
        A dictionary where keys are usernames and values are passwords.
    """
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            for line in f:
                if ":" in line:
                    u, p = line.strip().split(":", 1)
                    users[u] = p
    return users

def save_user(u, p):
    """
    Appends a new user's username and password to the 'users.txt' file.
    """
    with open(USERS_FILE, "a") as f:
        f.write(f"{u}:{p}\n")

def load_products():
    """
    Loads product data from 'products.txt'.
    """
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r", newline='') as f:
            return [[int(r[0]), r[1], int(r[2]), int(r[3])] for r in csv.reader(f) if len(r) >= 4]
    products = [
        [1, "Hoodie", 1500, 10],
        [2, "Jeans", 2000, 5],
        [3, "Sneakers", 3000, 8],
        [4, "T-Shirt", 800, 15]
    ]
    save_products(products)
    return products

def save_products(products):
    """
    Writes the current list of products to 'products.txt'.
    """
    with open(PRODUCTS_FILE, "w", newline='') as f:
        csv.writer(f).writerows(products)

class Store:
    def __init__(self):
        self.products = load_products()
        self.cart = []
   
    def show_products(self):
        refresh_screen()
        print("\n🧥 Product List:")
        for pid, name, price, stock in self.products:
            print(f"{pid}. {name} - ₹{price} ({stock} left)")

    def add_to_cart(self, pid, qty):
        refresh_screen()
        for p in self.products:
            if p[0] == pid:
                if p[3] >= qty:
                    self.cart.append([p, qty])
                    p[3] -= qty
                    save_products(self.products)
                    print(f"\n✅ Added {qty} x {p[1]}")
                    return
                else:
                    print("\n❌ Not enough stock.")
                    return
        print("\n❌ Product not found.")
   
    def remove_from_cart(self, pid):
        refresh_screen()
        for item in self.cart:
            p, q = item
            if p[0] == pid:
                self.cart.remove(item)
                p[3] += q
                save_products(self.products)
                print(f"\n🗑️ Removed {p[1]}")
                return
        print("\n❌ Item not in cart.")
   
    def show_cart(self):
        refresh_screen()
        print("\n🛒 Your Cart:")
        if not self.cart:
            print("Cart is empty.")
            return 0
        total = 0
        for p, q in self.cart:
            cost = p[2] * q
            total += cost
            print(f"- {p[1]} x{q} = ₹{cost}")
        print(f"Total = ₹{total}\n")
        return total
   
    def checkout(self):
        total = self.show_cart()
        if total:
            print("💳 Processing...\n🎉 Thank you for shopping!")
            self.cart.clear()
        else:
            print("❌ Nothing to checkout.")

def login_menu():
    users = load_users()
    while True:
        refresh_screen()
        print("===== LOGIN PAGE =====\n1. Login\n2. Register\n3. Exit")
        c = input("Choose: ")
        if c == "1":
            u = input("Username: ")
            p = getpass.getpass("Password: ")
            if u in users and users[u] == p:
                print(f"\n✅ Welcome, {u}!")
                return True
            else:
                print("\n❌ Invalid.")
                input("Enter to retry...")
        elif c == "2":
            u = input("New username: ")
            if u in users:
                print("\n❌ Taken.")
            else:
                p = getpass.getpass("New password: ")
                save_user(u, p)
                users[u] = p
                print("\n✅ Registered.")
            input("Enter to continue...")
        elif c == "3":
            sys.exit("\n👋 Goodbye!")
        else:
            input("\n❌ Invalid. Enter to retry...")

def main():
    if not login_menu():
        return
    s = Store()
    while True:
        refresh_screen()
        print("===== MENU =====\n1. Show Products\n2. Add to Cart\n3. Remove from Cart\n4. View Cart\n5. Checkout\n6. Exit")
        c = input("Choose: ")
        if c == "1":
            s.show_products()
            input("Enter to continue...")
        elif c == "2":
            try:
                s.add_to_cart(int(input("Product ID: ")), int(input("Quantity: ")))
            except:
                print("\n❌ Invalid.")
            input("Enter to continue...")
        elif c == "3":
            try:
                s.remove_from_cart(int(input("Product ID to remove: ")))
            except:
                print("\n❌ Invalid.")
            input("Enter to continue...")
        elif c == "4":
            s.show_cart()
            input("Enter to continue...")
        elif c == "5":
            s.checkout()
            input("Enter to continue...")
        elif c == "6":
            sys.exit("\n👋 Goodbye, Come again")
        else:
            input("\n❌ Invalid. Enter to retry...")

