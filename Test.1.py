import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime

# -------------------- Product Class --------------------
class Product:
    def __init__(self, product_id, name, price, quantity, description=""):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description

    def __str__(self):
        return f"{self.name} - ${self.price:.2f} (Stock: {self.quantity})"


# -------------------- ShoppingCart Class --------------------
class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_to_cart(self, product, quantity):
        if quantity <= 0:
            return False, "Quantity must be greater than 0."
        if quantity > product.quantity:
            return False, f"Only {product.quantity} units of {product.name} available."

        if product in self.items:
            self.items[product]['quantity'] += quantity
        else:
            self.items[product] = {'price': product.price, 'quantity': quantity}

        product.quantity -= quantity
        return True, f"{quantity} units of {product.name} added."

    def remove_from_cart(self, product, quantity):
        if product not in self.items:
            return False, f"{product.name} not in cart."
        if quantity <= 0 or quantity > self.items[product]['quantity']:
            return False, "Invalid quantity."

        self.items[product]['quantity'] -= quantity
        product.quantity += quantity

        if self.items[product]['quantity'] == 0:
            del self.items[product]
        return True, f"{quantity} units of {product.name} removed."

    def clear_cart(self):
        for product, details in self.items.items():
            product.quantity += details['quantity']
        self.items.clear()

    def calculate_total(self):
        return sum(details['price'] * details['quantity'] for details in self.items.values())


# -------------------- User Class --------------------
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cart = ShoppingCart()
        self.history = []

    def add_order_to_history(self, order):
        self.history.append(order)


# -------------------- ShoppingCartApp Class --------------------
class ShoppingCartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopping Cart")

        self.users = {}
        self.current_user = None
        self.products = []
        self.load_products()

        self.create_login_frame()

    # -------------------- Frame Handling --------------------
    def create_login_frame(self):
        self.clear_frame()
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Username:").pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        tk.Label(self.login_frame, text="Password:").pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        tk.Button(self.login_frame, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.login_frame, text="Register", command=self.register).pack()

    def create_main_frame(self):
        self.clear_frame()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        tk.Label(self.main_frame, text=f"Welcome, {self.current_user.username}").pack()

        # Product Listbox
        self.product_listbox = tk.Listbox(self.main_frame, width=50, height=10)
        self.product_listbox.pack(pady=10)
        self.update_product_list()

        tk.Button(self.main_frame, text="Add to Cart", command=self.add_to_cart).pack(pady=5)
        tk.Button(self.main_frame, text="Remove from Cart", command=self.remove_from_cart).pack(pady=5)
        tk.Button(self.main_frame, text="View Cart", command=self.view_cart).pack(pady=5)
        tk.Button(self.main_frame, text="Checkout", command=self.checkout).pack(pady=5)
        tk.Button(self.main_frame, text="View History", command=self.view_history).pack(pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.logout).pack(pady=5)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # -------------------- Product Handling --------------------
    def load_products(self):
        self.products = [
            Product(1, "Laptop", 1000, 5, "High performance"),
            Product(2, "Phone", 500, 10, "Latest model"),
            Product(3, "Headphones", 100, 15, "Noise cancelling"),
            Product(4, "Smartwatch", 200, 7, "Water resistant"),
            Product(5, "Tablet", 300, 8, "Lightweight")
        ]

    def update_product_list(self):
        self.product_listbox.delete(0, tk.END)
        for product in self.products:
            self.product_listbox.insert(tk.END, str(product))

    def get_selected_product(self):
        selection = self.product_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a product.")
            return None
        index = selection[0]
        return self.products[index]

    # -------------------- User Handling --------------------
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users and self.users[username].password == password:
            self.current_user = self.users[username]
            self.create_main_frame()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users:
            messagebox.showerror("Error", "User already exists")
            return

        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters.")
            return

        self.users[username] = User(username, password)
        messagebox.showinfo("Success", "User registered successfully!")

    def logout(self):
        self.current_user = None
        self.create_login_frame()

    # -------------------- Cart Handling --------------------
    def add_to_cart(self):
        product = self.get_selected_product()
        if not product:
            return

        quantity = simpledialog.askinteger("Quantity", f"Enter quantity for {product.name}:")
        if quantity is None:
            return

        success, msg = self.current_user.cart.add_to_cart(product, quantity)
        messagebox.showinfo("Cart Update", msg)
        self.update_product_list()

    def remove_from_cart(self):
        product = self.get_selected_product()
        if not product:
            return

        quantity = simpledialog.askinteger("Quantity", f"Enter quantity to remove for {product.name}:")
        if quantity is None:
            return

        success, msg = self.current_user.cart.remove_from_cart(product, quantity)
        messagebox.showinfo("Cart Update", msg)
        self.update_product_list()

    def view_cart(self):
        cart = self.current_user.cart
        if not cart.items:
            messagebox.showinfo("Cart", "Your cart is empty.")
            return

        cart_details = "\n".join([f"{p.name}: {d['quantity']} x ${d['price']:.2f}" for p, d in cart.items.items()])
        total = cart.calculate_total()
        messagebox.showinfo("Cart", f"{cart_details}\n\nTotal: ${total:.2f}")

    def checkout(self):
        cart = self.current_user.cart
        if not cart.items:
            messagebox.showwarning("Checkout", "Cart is empty.")
            return

        total = cart.calculate_total()
        confirm = messagebox.askyesno("Checkout", f"Total: ${total:.2f}. Proceed?")

        if confirm:
            order = {"items": cart.items.copy(), "total": total, "date": datetime.datetime.now()}
            self.current_user.add_order_to_history(order)
            cart.clear_cart()
            messagebox.showinfo("Checkout", "Order placed successfully!")
            self.update_product_list()

    def view_history(self):
        if not self.current_user.history:
            messagebox.showinfo("History", "No past orders.")
            return

        history_details = "\n\n".join([f"{order['date']} - Total: ${order['total']:.2f}" for order in self.current_user.history])
        messagebox.showinfo("History", history_details)


# -------------------- Main Execution --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingCartApp(root)
    root.mainloop()
