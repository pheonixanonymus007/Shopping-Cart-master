import sys, os, csv, getpass   # lazy one-liner import

# files for storing stuff
USERS_FILE = "users.txt"
PRODUCTS_FILE = "products.txt"


def clear_console():
    # windows = cls, mac/linux = clear
    os.system("cls" if os.name == "nt" else "clear")


def draw_logo():
    print("\n✨ Welcome to Diya's Cloth Shop ✨🛒\n")


def reset_screen():
    clear_console()
    draw_logo()


def read_users():
    creds = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            for line in f:
                if ":" in line:
                    usr, pwd = line.strip().split(":", 1)
                    creds[usr] = pwd
    return creds


def append_user(usr, pwd):
    with open(USERS_FILE, "a") as f:
        f.write(f"{usr}:{pwd}\n")


def load_products_from_file():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r", newline="") as f:
            rdr = csv.reader(f)
            return [[int(x[0]), x[1], int(x[2]), int(x[3])] for x in rdr if len(x) >= 4]
    # defaults if file missing
    default_items = [
        [1, "🧥 Hoodie", 1500, 10],
        [2, "👖 Jeans", 2000, 5],
        [3, "👟 Sneakers", 3000, 8],
        [4, "👕 T-Shirt", 800, 15],
    ]
    save_products(default_items)
    return default_items


def save_products(products):
    with open(PRODUCTS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(products)


class Shop:
    def __init__(self):
        self.items = load_products_from_file()
        self.cart = []   # format: [[product, qty], ...]

    def list_items(self):
        reset_screen()
        print("\n🧾 Available Products:")
        for pid, nm, price, stock in self.items:
            print(f"{pid}. {nm} - ₹{price} ({stock} left)")

    def add_item(self, pid, qty):
        reset_screen()
        for pr in self.items:
            if pr[0] == pid:
                if pr[3] >= qty:
                    self.cart.append([pr, qty])  # NOTE: duplicates not merged!
                    pr[3] -= qty
                    save_products(self.items)
                    print(f"\n✅ Added {qty} × {pr[1]}")
                    return
                else:
                    print("\n❌ Not enough stock")
                    return
        print("\n❌ Product not found")

    def remove_item(self, pid):
        reset_screen()
        for pr, q in list(self.cart):  # list() avoids runtime errors while removing
            if pr[0] == pid:
                self.cart.remove([pr, q])
                pr[3] += q
                save_products(self.items)
                print(f"\n🗑️ Removed {pr[1]}")
                return
        print("\n⚠️ Item not in cart")

    def show_cart(self):
        reset_screen()
        print("\n🛍️ Your Cart:")
        if not self.cart:
            print("Cart is empty.")
            return 0
        grand_total = 0
        for pr, q in self.cart:
            subtotal = pr[2] * q
            grand_total += subtotal
            print(f"- {pr[1]} ×{q} = ₹{subtotal}")
        print(f"\n📦 Total: ₹{grand_total}\n")
        return grand_total

    def do_checkout(self):
        amt = self.show_cart()
        if amt > 0:
            print("💳 Processing payment... \nThanks for shopping 🙏")
            self.cart.clear()
        else:
            print("❌ Nothing to checkout")


def login_flow():
    users = read_users()
    while True:
        reset_screen()
        print("===== 🔐 LOGIN PAGE =====\n1. Login\n2. Register\n3. Exit 🚪")
        choice = input("Choose: ")
        if choice == "1":
            usr = input("👤 Username: ")
            pwd = getpass.getpass("🔑 Password: ")
            if usr in users and users[usr] == pwd:
                print(f"\n✅ Welcome back, {usr}")
                return True
            else:
                print("\n❌ Wrong credentials")
                input("Press Enter...")
        elif choice == "2":
            new_usr = input("🆕 New username: ")
            if new_usr in users:
                print("\n❌ Username taken")
            else:
                new_pwd = getpass.getpass("🔑 New password: ")
                append_user(new_usr, new_pwd)
                users[new_usr] = new_pwd
                print("\n✅ Account created")
            input("Press Enter to continue...")
        elif choice == "3":
            sys.exit("\n👋 Goodbye!")
        else:
            input("Invalid option. Enter to retry...")


def main():
    if not login_flow():
        return
    shop = Shop()
    while True:
        reset_screen()
        print("===== 📋 MENU =====")
        print("1. Show Products\n2. Add to Cart\n3. Remove from Cart\n4. View Cart\n5. Checkout\n6. Exit")
        opt = input("Choose: ")
        if opt == "1":
            shop.list_items()
            input("Enter to continue...")
        elif opt == "2":
            try:
                pid = int(input("Product ID: "))
                qty = int(input("Quantity: "))
                shop.add_item(pid, qty)
            except ValueError:
                print("❌ Invalid input")
            input("Enter to continue...")
        elif opt == "3":
            try:
                pid = int(input("Product ID to remove: "))
                shop.remove_item(pid)
            except ValueError:
                print("❌ Invalid input")
            input("Enter to continue...")
        elif opt == "4":
            shop.show_cart()
            input("Enter to continue...")
        elif opt == "5":
            shop.do_checkout()
            input("Enter to continue...")
        elif opt == "6":
            sys.exit("\n👋 See you next time!")
        else:
            input("Invalid choice. Enter to retry...")


# run program
if __name__ == "__main__":
    main()
