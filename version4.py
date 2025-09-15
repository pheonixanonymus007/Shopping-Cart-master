from abc import ABC, abstractmethod
import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# PRODUCT CLASS
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

    def __add__(self, other):
        if isinstance(other, Product):
            return self.price + other.price
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Product):
            return self.price - other.price
        return NotImplemented


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

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.address}"

    def add_to_cart(self, product, quantity=1):
        self.cart.add_product(product, quantity)

    def remove_from_cart(self, product, quantity=1):
        self.cart.remove_product(product, quantity)




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
        else:
            # Call the out_of_stock method of the app to handle it in the GUI thread
            app.out_of_stock(product.name, product.quantity)

    def remove_product(self, product, quantity=1):
        if not self.items:
            messagebox.showinfo("Empty Cart", "Your cart is empty.")
            return
        if product in self.items:
            if self.items[product]['quantity'] <= quantity:
                product.quantity += self.items[product]['quantity']
                del self.items[product]
            else:
                self.items[product]['quantity'] -= quantity
                product.quantity += quantity
        else:
            messagebox.showerror("Not in Cart", f"{product.name} is not in the cart.")

    def view_cart(self):
        if not self.items:
            print("Your cart is empty.")
        else:
            for item in self.items.values():
                product = item['product']
                quantity = item['quantity']
                print(f"{product.name} (x{quantity}): ${product.price * quantity}")

    def checkout(self):
        total = sum(item['product'].price * item['quantity'] for item in self.items.values())
        if total == 0:
            print("Your cart is empty. Add items to cart before checking out.")
            return False
        confirm = input(f"Your total is ${total}. Do you want to proceed with the checkout? (yes/y or no/n): ").strip().lower()
        if confirm in ['yes', 'y']:
            order = Order(self.items, total)
            self.items = {}
            return order
        elif confirm in ['no', 'n']:
            print("Checkout cancelled.")
            return False
        else:
            print("Invalid input. Please enter 'yes/y' or 'no/n'.")
            return False


# ABSTRACT CLASS
class Account(ABC):
    @abstractmethod
    def view_products(self):
        pass

    @abstractmethod
    def view_history(self):
        pass


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
        self.items = {product: {'product': product, 'quantity': details['quantity']} for product, details in items.items()}
        self.total = total

    def __str__(self):
        items_str = '\n'.join([f"{details['product'].name} (x{details['quantity']}): ${details['product'].price * details['quantity']}" for details in self.items.values()])
        return f"Date: {self.date}\nItems:\n{items_str}\nTotal: ${self.total}"


# SHOPPINGCART APP CLASS
class ShoppingCartApp:
    def __init__(self):
        self.users = {}
        self.products = {}
        self.load_products()
        self.load_users()

        self.root = tk.Tk()
        self.root.title("Dia's Ice Cream Shop")
        self.root.geometry("600x600")
        self.current_user = None

    def load_products(self):
        try:
            with open('products.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            product_id, name, price, description, quantity = line.split(';')
                            self.products[product_id] = Product(product_id, name, float(price), description, int(quantity))
                        except ValueError as e:
                            print(f"Error parsing line: {line}\n{e}")
        except FileNotFoundError:
            print("Products file not found.")

    def load_users(self):
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        username, password, first_name, last_name, address = line.split(';')
                        self.users[username] = Customer(username, password, first_name, last_name, address)

                        self.load_cart(username)
                        self.load_history(username)
        except FileNotFoundError:
            print("Users file not found.")

    def save_products(self):
        with open('products.txt', 'w') as f:
            for product in self.products.values():
                f.write(f"{product.product_id};{product.name};{product.price};{product.description};{product.quantity}\n")

    def save_users(self):
        with open('users.txt', 'w') as f:
            for user in self.users.values():
                f.write(f"{user.username};{user.password};{user.first_name};{user.last_name};{user.address}\n")

    def register_user(self, username, password, first_name, last_name, address):
        if username in self.users:
            messagebox.showerror("Error", "Username already exists.")
        else:
            self.users[username] = Customer(username, password, first_name, last_name, address)
            self.save_users()
            messagebox.showinfo("Success", "User registered successfully.")
            self.show_login()

    def login_user(self, username, password):
        if username in self.users and self.users[username].password == password:
            self.current_user = self.users[username]
            self.user_menu(self.current_user)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

#dafault page  (self to call an attribute), (root for window in gui),
#  (tk as tkinter use for simple graphical interferance), (frame as container) ,(def is use for function or method)

    def run(self):
        self.show_main_menu()
        self.root.mainloop()

    def show_main_menu(self):
        self.clear_window()

        frame = tk.Frame(self.root)
        frame.pack(pady=150)

        tk.Label(frame, text="˚☽˚｡⋆｡❅*Welcome to my shop!˚☽˚｡⋆｡❅*", font=("Firacode", 20)).pack(pady=10)
        tk.Button(frame, text="Register 📑", command=self.show_register, width=25).pack(pady=10)
        tk.Button(frame, text="Login 🚹", command=self.show_login, width=25).pack(pady=10)
        tk.Button(frame, text="Exit ❌", command=self.root.quit, width=25).pack(pady=10)

#registration

    def show_register(self):
        self.clear_window()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Register", font=("Helvetica", 17)).pack(pady=10)

        tk.Label(frame, text="Username:").pack()
        username_entry = tk.Entry(frame)
        username_entry.pack()

        tk.Label(frame, text="Password:").pack()
        password_entry = tk.Entry(frame, show='*')
        password_entry.pack()

        tk.Label(frame, text="First Name:").pack()
        first_name_entry = tk.Entry(frame)
        first_name_entry.pack()

        tk.Label(frame, text="Last Name:").pack()
        last_name_entry = tk.Entry(frame)
        last_name_entry.pack()

        tk.Label(frame, text="Address:").pack()
        address_entry = tk.Entry(frame)
        address_entry.pack()

        def register_user_action():
            username = username_entry.get()
            password = password_entry.get()
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            address = address_entry.get()

            # Check for empty inputs
            if check_empty_inputs(username_entry, password_entry, first_name_entry, last_name_entry, address_entry):
                self.show_empty_input_error()
                return

            # Validate username (no spaces)
            if " " in username:
                messagebox.showerror("Error", "Username cannot contain spaces.")
                return

            # Validate password length (exactly 8 characters)
            if len(password) != 8:
                messagebox.showerror("Error", "Password must be exactly 8 characters long.")
                return

            self.register_user(username, password, first_name, last_name, address)

        tk.Button(frame, text="Register", command=register_user_action).pack(pady=10)
        tk.Button(frame, text="Back", command=self.show_main_menu).pack(pady=5)

#login

    def show_login(self):
        self.clear_window()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Login", font=("Helvetica", 17)).pack(pady=10)

        tk.Label(frame, text="Username:").pack()
        username_entry = tk.Entry(frame)
        username_entry.pack()

        tk.Label(frame, text="Password:").pack()
        password_entry = tk.Entry(frame, show='*')
        password_entry.pack()

        tk.Button(frame, text="Login", command=lambda: self.login_user(username_entry.get(), password_entry.get())).pack(pady=10)
        tk.Button(frame, text="Back", command=self.show_main_menu).pack(pady=5)

    def user_menu(self, user):
        if not user:
            return

        self.clear_window()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text=f"Welcome, {user.first_name} {user.last_name}", font=("Helvetica", 14)).pack(pady=10)


        tk.Button(frame, text="View Product List", command=lambda: self.view_products(user), width=20).pack(pady=10)
        tk.Button(frame, text="Add Products to Cart", command=lambda: self.add_to_cart(user), width=20).pack(pady=10)
        tk.Button(frame, text="Remove Products from Cart", command=lambda: self.remove_from_cart(user), width=20).pack(pady=10)
        tk.Button(frame, text="View Cart", command=lambda: self.view_cart(user), width=20).pack(pady=10)
        tk.Button(frame, text="View Shopping History", command=lambda: self.view_history(user), width=20).pack(pady=10)
        tk.Button(frame, text="Checkout", command=lambda: self.checkout(user), width=20).pack(pady=10)
        tk.Button(frame, text="Logout", command=lambda: self.logout(user), width=20).pack(pady=10)

#products

    def view_products(self, user):
        self.clear_window()

        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, pady=20)

        tk.Label(frame, text="Products", font=("Helvetica", 14)).pack(pady=10)

        # Use a Canvas with a Scrollbar for scrollable content
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame to hold the product cards inside the canvas
        product_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=product_frame, anchor="nw")

        for product in self.products.values():
            # Create a card frame for each product
            card_frame = tk.Frame(product_frame, relief=tk.GROOVE, borderwidth=2, padx=10, pady=10)
            card_frame.pack(pady=5, fill=tk.X, padx=10)

            tk.Label(card_frame, text=f"Product ID: {product.product_id}", font=("Helvetica", 10)).pack(anchor='w')
            tk.Label(card_frame, text=f"Name: {product.name}", font=("Helvetica", 12, "bold")).pack(anchor='w')
            tk.Label(card_frame, text=f"Price: ${product.price}", font=("Helvetica", 10)).pack(anchor='w')
            tk.Label(card_frame, text=f"Description: {product.description}", font=("Helvetica", 10)).pack(anchor='w')
            tk.Label(card_frame, text=f"Quantity Available: {product.quantity}", font=("Helvetica", 10)).pack(anchor='w')

        # Update the scroll region of the canvas
        product_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        tk.Button(frame, text="Back", command=lambda: self.user_menu(user)).pack(pady=10)

#cart

    def view_cart(self, user):
        self.clear_window()

        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, pady=20)

        tk.Label(frame, text="Your Cart", font=("Helvetica", 14)).pack(pady=10)

        if not user.cart.items:
            tk.Label(frame, text="Your cart is empty.").pack()
        else:
            canvas = tk.Canvas(frame)
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.configure(yscrollcommand=scrollbar.set)

            cart_frame = tk.Frame(canvas)
            canvas.create_window((0, 0), window=cart_frame, anchor="nw")

            for product, item_details in user.cart.items.items():
                quantity = item_details['quantity']
                item_total = product.price * quantity

                card_frame = tk.Frame(cart_frame, relief=tk.GROOVE, borderwidth=2, padx=10, pady=10)
                card_frame.pack(pady=5, fill=tk.X, padx=10)

                tk.Label(card_frame, text=f"Product: {product.name}", font=("Helvetica", 12, "bold")).pack(anchor='w')
                tk.Label(card_frame, text=f"Quantity: {quantity}", font=("Helvetica", 10)).pack(anchor='w')
                tk.Label(card_frame, text=f"Price per item: ${product.price}", font=("Helvetica", 10)).pack(anchor='w')
                tk.Label(card_frame, text=f"Item Total: ${item_total}", font=("Helvetica", 10)).pack(anchor='w')

            cart_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

        tk.Button(frame, text="Back", command=lambda: self.user_menu(user)).pack(pady=10)

#add to cart

    def add_to_cart(self, user):
        self.clear_window()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Add to Cart", font=("Helvetica", 14)).pack(pady=10)

        tk.Label(frame, text="Product ID:").pack()
        product_id_entry = tk.Entry(frame)
        product_id_entry.pack()

        tk.Label(frame, text="Quantity:").pack()
        quantity_entry = tk.Entry(frame)
        quantity_entry.pack()

        def add_to_cart_action():
            product_id = product_id_entry.get()
            quantity_str = quantity_entry.get()

            # Check for empty inputs
            if check_empty_inputs(product_id_entry, quantity_entry):
                self.show_empty_input_error()
                return

            # Validate quantity input
            try:
                quantity = int(quantity_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity. Please enter a number.")
                return

            if product_id in self.products:
                product = self.products[product_id]
                if product.quantity >= quantity:
                    user.add_to_cart(product, quantity)
                    self.save_products()
                    self.save_cart(user.username)  # Save cart for the specific user
                    messagebox.showinfo("Success", "Product added to cart.")
                else:
                    self.out_of_stock(product.name, product.quantity)  # Show out-of-stock message
            else:
                messagebox.showerror("Error", "Invalid product ID.")
            self.user_menu(user)

        tk.Button(frame, text="Add", command=add_to_cart_action).pack(pady=10)
        tk.Button(frame, text="Back", command=lambda: self.user_menu(user)).pack(pady=5)

#remove from cart

    def remove_from_cart(self, user):
        self.clear_window()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Remove from Cart", font=("Helvetica", 14)).pack(pady=10)

        tk.Label(frame, text="Product ID:").pack()
        product_id_entry = tk.Entry(frame)
        product_id_entry.pack()

        tk.Label(frame, text="Quantity:").pack()
        quantity_entry = tk.Entry(frame)
        quantity_entry.pack()

        def remove_from_cart_action():
            product_id = product_id_entry.get()
            quantity_str = quantity_entry.get()

            # Check for empty inputs
            if check_empty_inputs(product_id_entry, quantity_entry):
                self.show_empty_input_error()
                return

            # Validate quantity input
            try:
                quantity = int(quantity_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity. Please enter a number.")
                return

            # Check if product ID exists and quantity is valid
            if product_id in self.products:
                product = self.products[product_id]
                if quantity > 0 and quantity <= product.quantity:
                    user.remove_from_cart(product, quantity)
                    self.save_products()
                    self.save_cart(user.username)  # Save cart for the specific user
                    messagebox.showinfo("Success", "Product removed from cart.")
                else:
                    messagebox.showerror("Error", "Invalid quantity. Please enter a valid quantity.")
            else:
                messagebox.showerror("Error", "Invalid product ID.")
            self.user_menu(user)

        tk.Button(frame, text="Remove", command=remove_from_cart_action).pack(pady=10)
        tk.Button(frame, text="Back", command=lambda: self.user_menu(user)).pack(pady=5)

#check out

    def checkout(self, user):
        self.clear_window()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Checkout", font=("Helvetica", 14)).pack(pady=10)

        total = sum(item['product'].price * item['quantity'] for item in user.cart.items.values())
        if total == 0:
            tk.Label(frame, text="Your cart is empty. Add items to cart before checking out.").pack()
        else:
            confirm = messagebox.askyesno("Checkout", f"Your total is ${total}. Do you want to proceed with the checkout?")
            if confirm:
                order = Order(user.cart.items, total)
                user.cart.items = {}
                user.history.append(order)
                self.save_products()
                self.save_history(user.username)
                self.save_cart(user.username)  # Save cart for the specific user
                messagebox.showinfo("Success", f"Order placed. Total: ${order.total}")
                self.user_menu(user)
            else:
                messagebox.showinfo("Cancelled", "Checkout cancelled.")
                self.user_menu(user)

#history

    def view_history(self, user):
        self.clear_window()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Purchase History", font=("Helvetica", 14)).pack(pady=10)

        if not user.history:
            tk.Label(frame, text="No purchase history.").pack()
        else:
            history_list_frame = tk.Frame(frame)
            history_list_frame.pack()

            scrollbar = tk.Scrollbar(history_list_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            history_listbox = tk.Listbox(history_list_frame, yscrollcommand=scrollbar.set, width=50)
            for order in user.history:
                history_listbox.insert(tk.END, str(order))
            history_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

            scrollbar.config(command=history_listbox.yview)

        tk.Button(frame, text="Back", command=lambda: self.user_menu(user)).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_history(self, username):
        try:
            with open(f'{username}_history.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:  # Skip empty lines
                        try:
                            date_str, items_str, total_str = line.split(';')
                            items = {}
                            for item_str in items_str.split(','):
                                product_id, quantity_str = item_str.split(':')
                                quantity = int(quantity_str)
                                if product_id in self.products:
                                    items[self.products[product_id]] = {'product': self.products[product_id], 'quantity': quantity}
                            total = float(total_str)
                            order = Order(items, total)
                            order.date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
                            self.users[username].history.append(order)
                        except ValueError as e:
                            print(f"Error parsing line: {line}\n{e}")
        except FileNotFoundError:
            print(f"History file for {username} not found.")

    def save_history(self, username):
        with open(f'{username}_history.txt', 'w') as f:
            for order in self.users[username].history:
                items_str = ','.join([f"{item['product'].product_id}:{item['quantity']}" for item in order.items.values()])
                f.write(f"{order.date.strftime('%Y-%m-%d %H:%M:%S.%f')};{items_str};{order.total}\n")

    def load_cart(self, username):
        try:
            with open(f'{username}_cart.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            product_id, quantity_str = line.split(';')
                            quantity = int(quantity_str)
                            if product_id in self.products:
                                self.users[username].cart.add_product(self.products[product_id], quantity)
                        except ValueError as e:
                            print(f"Error parsing line: {line}\n{e}")
        except FileNotFoundError:
            print(f"Cart file for {username} not found.")

    def save_cart(self, username):
        with open(f'{username}_cart.txt', 'w') as f:
            for product, details in self.users[username].cart.items.items():
                f.write(f"{product.product_id};{details['quantity']}\n")

    def logout(self, user):
        self.save_history(user.username)
        self.save_cart(user.username)
        self.current_user = None
        self.show_main_menu()

    def out_of_stock(self, product_name, available_quantity):
        messagebox.showerror("Out of Stock",
                           f"Sorry, only {available_quantity} of {product_name} are available.")

    def show_empty_input_error(self):
        messagebox.showerror("Error", "Please fill in all required fields.")

# Helper function outside of the class
def check_empty_inputs(*entries):
    for entry in entries:
        if not entry.get():
            return True
    return False

# MAIN EXECUTION
if __name__ == "__main__":
    app = ShoppingCartApp()
    app.run()