from abc import ABC, abstractmethod
import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# PRODUCT CLASS
class Product:
    def __init__(self, product_id, name, price, description, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} (${self.price}): {self.description} - Quantity: {self.quantity}"

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.product_id == other.product_id
        return False

    def __hash__(self):
        return hash(self.product_id)


# SHOPPINGCART CLASS
class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_product(self, product, quantity=1):
        if product.quantity >= quantity:
            if product in self.items:
                self.items[product]['quantity'] += quantity
            else:
                self.items[product] = {'product': product, 'quantity': quantity}
            product.quantity -= quantity
            return True
        return False

    def remove_product(self, product, quantity=1):
        if not self.items:
            messagebox.showinfo("Empty Cart", "Your cart is empty.")
            return False
        if product in self.items:
            if self.items[product]['quantity'] <= quantity:
                product.quantity += self.items[product]['quantity']
                del self.items[product]
            else:
                self.items[product]['quantity'] -= quantity
                product.quantity += quantity
            return True
        else:
            messagebox.showerror("Not in Cart", f"{product.name} is not in the cart.")
            return False


# ABSTRACT CLASS
class Account(ABC):
    @abstractmethod
    def view_products(self):
        pass

    @abstractmethod
    def view_history(self):
        pass


# USER CLASS
class User:
    def __init__(self, username, password, first_name, last_name, address):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.cart = ShoppingCart()
        self.history = []

    def add_to_cart(self, product, quantity=1):
        return self.cart.add_product(product, quantity)

    def remove_from_cart(self, product, quantity=1):
        return self.cart.remove_product(product, quantity)


# CUSTOMER CLASS 
class Customer(User, Account):
    def view_products(self, products):
        for product in products:
            print(product)

    def view_history(self):
        if not self.history:
            print("No purchase history.")
        else:
            for order in self.history:
                print(order)


# ORDER CLASS
class Order:
    def __init__(self, items, total):
        self.date = datetime.datetime.now()
        self.items = {product: {'product': details['product'], 'quantity': details['quantity']}
                      for product, details in items.items()}
        self.total = total

    def __str__(self):
        items_str = '\n'.join([f"{d['product'].name} (x{d['quantity']}): ${d['product'].price * d['quantity']}"
                               for d in self.items.values()])
        return f"Date: {self.date}\nItems:\n{items_str}\nTotal: ${self.total}"


# SHOPPINGCART APP CLASS
class ShoppingCartApp:
    def __init__(self):
        self.users = {}
        self.products = {}
        self.root = tk.Tk()
        self.root.title("Dia's Ice Cream Shop")
        self.root.geometry("600x600")
        self.current_user = None

        self.load_products()
        self.load_users()

    # ---------- DATA HANDLING ----------
    def load_products(self):
        try:
            with open('products.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        pid, name, price, desc, qty = line.split(';')
                        self.products[pid] = Product(pid, name, float(price), desc, int(qty))
        except FileNotFoundError:
            print("Products file not found.")

    def save_products(self):
        with open('products.txt', 'w') as f:
            for p in self.products.values():
                f.write(f"{p.product_id};{p.name};{p.price};{p.description};{p.quantity}\n")

    def load_users(self):
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        u, pw, fn, ln, addr = line.split(';')
                        self.users[u] = Customer(u, pw, fn, ln, addr)
                        self.load_cart(u)
                        self.load_history(u)
        except FileNotFoundError:
            print("Users file not found.")

    def save_users(self):
        with open('users.txt', 'w') as f:
            for u in self.users.values():
                f.write(f"{u.username};{u.password};{u.first_name};{u.last_name};{u.address}\n")

    def load_cart(self, username):
        try:
            with open(f"{username}_cart.txt", 'r') as f:
                for line in f:
                    pid, qty = line.strip().split(';')
                    qty = int(qty)
                    if pid in self.products:
                        self.users[username].cart.add_product(self.products[pid], qty)
        except FileNotFoundError:
            pass

    def save_cart(self, username):
        with open(f"{username}_cart.txt", 'w') as f:
            for p, d in self.users[username].cart.items.items():
                f.write(f"{p.product_id};{d['quantity']}\n")

    def load_history(self, username):
        try:
            with open(f"{username}_history.txt", 'r') as f:
                for line in f:
                    date_str, items_str, total_str = line.strip().split(';')
                    items = {}
                    for s in items_str.split(','):
                        pid, qty = s.split(':')
                        if pid in self.products:
                            items[self.products[pid]] = {'product': self.products[pid], 'quantity': int(qty)}
                    order = Order(items, float(total_str))
                    order.date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
                    self.users[username].history.append(order)
        except FileNotFoundError:
            pass

    def save_history(self, username):
        with open(f"{username}_history.txt", 'w') as f:
            for o in self.users[username].history:
                items_str = ','.join([f"{i['product'].product_id}:{i['quantity']}" for i in o.items.values()])
                f.write(f"{o.date.strftime('%Y-%m-%d %H:%M:%S.%f')};{items_str};{o.total}\n")

    # ---------- AUTH ----------
    def register_user(self, u, pw, fn, ln, addr):
        if u in self.users:
            messagebox.showerror("Error", "Username already exists.")
        else:
            self.users[u] = Customer(u, pw, fn, ln, addr)
            self.save_users()
            messagebox.showinfo("Success", "Registered successfully.")
            self.show_login()

    def login_user(self, u, pw):
        if u in self.users and self.users[u].password == pw:
            self.current_user = self.users[u]
            self.user_menu(self.current_user)
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def logout(self, user):
        self.save_history(user.username)
        self.save_cart(user.username)
        self.current_user = None
        self.show_main_menu()

    # ---------- GUI SCREENS ----------
    def run(self):
        self.show_main_menu()
        self.root.mainloop()

    def clear_window(self):
        for w in self.root.winfo_children():
            w.destroy()

    def show_main_menu(self):
        self.clear_window()
        f = tk.Frame(self.root)
        f.pack(pady=150)
        tk.Label(f, text="˚☽˚｡⋆｡❅*Welcome to my shop!˚☽˚｡⋆｡❅*", font=("Helvetica", 20)).pack(pady=10)
        tk.Button(f, text="Register 📑", command=self.show_register, width=25).pack(pady=10)
        tk.Button(f, text="Login 🚹", command=self.show_login, width=25).pack(pady=10)
        tk.Button(f, text="Exit ❌", command=self.root.quit, width=25).pack(pady=10)

    def show_register(self):
        self.clear_window()
        f = tk.Frame(self.root)
        f.pack(pady=20)
        tk.Label(f, text="Register", font=("Helvetica", 17)).pack(pady=10)

        entries = {}
        for label in ["Username", "Password", "First Name", "Last Name", "Address"]:
            tk.Label(f, text=f"{label}:").pack()
            show = '*' if label == "Password" else None
            entries[label] = tk.Entry(f, show=show)
            entries[label].pack()

        def action():
            u, pw, fn, ln, addr = [entries[k].get() for k in entries]
            if not all([u, pw, fn, ln, addr]):
                self.show_empty_input_error()
                return
            if " " in u:
                messagebox.showerror("Error", "Username cannot contain spaces.")
                return
            if len(pw) != 8:
                messagebox.showerror("Error", "Password must be exactly 8 chars.")
                return
            self.register_user(u, pw, fn, ln, addr)

        tk.Button(f, text="Register", command=action).pack(pady=10)
        tk.Button(f, text="Back", command=self.show_main_menu).pack(pady=5)

    def show_login(self):
        self.clear_window()
        f = tk.Frame(self.root)
        f.pack(pady=20)
        tk.Label(f, text="Login", font=("Helvetica", 17)).pack(pady=10)
        tk.Label(f, text="Username:").pack()
        u = tk.Entry(f)
        u.pack()
        tk.Label(f, text="Password:").pack()
        p = tk.Entry(f, show="*")
        p.pack()
        tk.Button(f, text="Login", command=lambda: self.login_user(u.get(), p.get())).pack(pady=10)
        tk.Button(f, text="Back", command=self.show_main_menu).pack(pady=5)

    def user_menu(self, user):
        self.clear_window()
        f = tk.Frame(self.root)
        f.pack(pady=20)
        tk.Label(f, text=f"Welcome, {user.first_name} {user.last_name}", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(f, text="View Product List", command=lambda: self.view_products(user), width=25).pack(pady=5)
        tk.Button(f, text="Add Products to Cart", command=lambda: self.add_to_cart(user), width=25).pack(pady=5)
        tk.Button(f, text="Remove Products from Cart", command=lambda: self.remove_from_cart(user), width=25).pack(pady=5)
        tk.Button(f, text="View Cart", command=lambda: self.view_cart(user), width=25).pack(pady=5)
        tk.Button(f, text="View Shopping History", command=lambda: self.view_history(user), width=25).pack(pady=5)
        tk.Button(f, text="Checkout", command=lambda: self.checkout(user), width=25).pack(pady=5)
        tk.Button(f, text="Logout", command=lambda: self.logout(user), width=25).pack(pady=5)

    def view_products(self, user):
        self.clear_window()
        f = tk.Frame(self.root)
        f.pack(pady=20)
        tk.Label(f, text="Products", font=("Helvetica", 14)).pack(pady=10)
        lb = tk.Listbox(f, width=60, height=12)
        for p in self.products.values():
            lb.insert(tk.END, str(p))
        lb.pack()
        tk.Button(f, text="Back", command=lambda: self.user_menu(user)).pack(pady=10)

    # ---------- CART ----------
    def view_cart(self, user):
        self.clear_window()
        f = tk.Frame(self.root)
        f.pack(pady=20)
        tk.Label(f, text="Your Cart", font=("Helvetica", 14)).pack(pady=10)

        if not user.cart.items:
            tk.Label(f, text="Your cart is empty.").pack()
        else:
            lb = tk.Listbox(f, width=60, height=10)
            total = 0
            for item in user.cart.items.values():
                p, q = item['product'], item['quantity']
                total += p.price * q
                lb.insert(tk.END, f"{p.name} (x{q}): ${p.price * q}")
            lb.pack()
            tk.Label(f, text=f"Total: ${total:.2f}", font=("Helvetica", 12, "bold")).pack(pady=10)

        bf = tk.Frame(f)
        bf.pack(pady=10)
        tk.Button(bf, text="🔄 Refresh", command=lambda: self.view_cart(user)).pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="💳 Checkout", command=lambda: self.checkout(user)).pack(side=tk.LEFT, padx=5)

        def clear_cart():
            if user.cart.items and messagebox.askyesno("Clear Cart", "Empty your cart?"):
                for item in list(user.cart.items.values()):
                    item['product'].quantity += item['quantity']
                user.cart.items.clear()
                self.save_products()
                self.save_cart(user.username)
                self.view_cart(user)

        tk.Button(bf, text="🗑 Clear Cart", command=clear_cart).pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="⬅ Back", command=lambda: self.user_menu(user)).pack(side=tk.LEFT, padx=5)

    def add_to_cart(self, user):
        self.clear_window()
        f = tk.Frame(self.root)
        f.pack(pady=20)
        tk.Label(f, text="Add to Cart", font=("Helvetica", 14)).pack(pady=10)

        lb = tk.Listbox(f, width=60, height=10)
        keys = list(self.products.keys())
        for pid in keys:
            lb.insert(tk.END, str(self.products[pid]))
        lb.pack()

        tk.Label(f, text="Quantity:").pack()
        q_entry = tk.Entry(f)
        q_entry.pack()

        def action(q_override=None):
            sel = lb.curselection()
            if not sel:
                messagebox.showerror("Error", "Select a product.")
                return
            pid = keys[sel[0]]
            p = self.products[pid]
            q = q_override or int(q_entry.get() or 0)
            if q <= 0:
                messagebox.showerror("Error", "Quantity must be >0.")
                return
            if user.add_to_cart(p, q):
                self.save_products()
                self.save_cart(user.username)
                messagebox.showinfo("Added", f"{q}x {p.name} added.")
                self.add_to_cart(user)
            else:
                self.out_of_stock(p.name, p.quantity)

        tk.Button(f, text="Add", command=lambda: action()).pack(pady=10)
        tk.Button(f, text="Back", command=lambda: self.user_menu(user)).pack(pady=5)
        lb.bind("<Double-1>", lambda e: action(q_override=1))

    def remove_from_cart(self, user):
        self.clear_window()
        f = tk.Frame(self.root)
        f.pack(pady=20)
        tk.Label(f, text="Remove from Cart", font=("Helvetica", 14)).pack(pady=10)

        items = list(user.cart.items.values())
        lb = tk.Listbox(f, width=60, height=10)
        for it in items:
            lb.insert(tk.END, f"{it['product'].name} (x{it['quantity']}): ${it['product'].price * it['quantity']}")
        lb.pack()

        if not items:
            tk.Label(f, text="Your cart is empty.").pack()
            tk.Button(f, text="Back", command=lambda: self.user_menu(user)).pack(pady=10)
            return

        tk.Label(f, text="Quantity to Remove:").pack()
        q_entry = tk.Entry(f)
        q_entry.pack()

        def action(q_override=None):
            sel = lb.curselection()
            if not sel:
                messagebox.showerror("Error", "Select an item.")
                return
            prod = items[sel[0]]['product']
            q = q_override or int(q_entry.get() or 0)
            if q <= 0:
                messagebox.showerror("Error", "Quantity must be >0.")
                return
            if user.remove_from_cart(prod, q):
                self.save_products()
                self.save_cart(user.username)
                messagebox.showinfo("Removed", f"Removed {q}x {prod.name}.")
                self.remove_from_cart(user)
            else:
                messagebox.showerror("Error", "Invalid quantity.")

        tk.Button(f, text="Remove", command=lambda: action()).pack(pady=10)
        tk.Button(f, text="Back", command=lambda: self.user_menu(user)).pack(pady=5)
        lb.bind("<Double-1>", lambda e: action(q_override=1))

    def view_history(self, user):
        self.clear_window()
        f = tk.Frame(self.root)
        f.pack(pady=20)
        tk.Label(f, text="Purchase History", font=("Helvetica", 14)).pack(pady=10)
        if not user.history:
            tk.Label(f, text="No purchase history.").pack()
        else:
            lb = tk.Listbox(f, width=60, height=12)
            for o in user.history:
                lb.insert(tk.END, str(o))
            lb.pack()
        tk.Button(f, text="Back", command=lambda: self.user_menu(user)).pack(pady=10)

    # ---------- HELPERS ----------
    def checkout(self, user):
        total = sum(i['product'].price * i['quantity'] for i in user.cart.items.values())
        if total == 0:
            messagebox.showinfo("Empty", "Cart is empty.")
            return
        if messagebox.askyesno("Checkout", f"Your total is ${total}. Proceed?"):
            order = Order(user.cart.items, total)
            user.cart.items = {}
            user.history.append(order)
            self.save_products()
            self.save_history(user.username)
            self.save_cart(user.username)
            messagebox.showinfo("Done", f"Order placed! Total: ${order.total}")
            self.view_cart(user)

    def out_of_stock(self, name, qty):
        messagebox.showerror("Out of Stock", f"Only {qty} of {name} left.")

    def show_empty_input_error(self):
        messagebox.showerror("Error", "Please fill in all fields.")


# ---------- MAIN ----------
if __name__ == "__main__":
    app = ShoppingCartApp()
    app.run()
