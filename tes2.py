# Add this import at the top with other imports
from tkinter import ttk

# Add this method to the ShoppingCartApp class
def show_product_selection(self):
    # Clear previous content
    for widget in self.root.winfo_children():
        widget.destroy()

    # Create main frame
    main_frame = ttk.Frame(self.root)
    main_frame.pack(fill='both', expand=True, padx=10, pady=5)

    # Create Treeview for products
    columns = ('ID', 'Name', 'Price', 'Description', 'Stock')
    product_tree = ttk.Treeview(main_frame, columns=columns, show='headings')

    # Define column headings
    for col in columns:
        product_tree.heading(col, text=col)
        product_tree.column(col, width=100)

    # Add products to the treeview
    for product in self.products.values():
        product_tree.insert('', 'end', values=(
            product.product_id,
            product.name,
            f"${product.price:.2f}",
            product.description,
            product.quantity
        ))

    product_tree.pack(pady=10, fill='both', expand=True)

    # Create frame for quantity selection and buttons
    control_frame = ttk.Frame(main_frame)
    control_frame.pack(fill='x', pady=5)

    # Quantity selector
    ttk.Label(control_frame, text="Quantity:").pack(side='left', padx=5)
    quantity_var = tk.StringVar(value="1")
    quantity_spinbox = ttk.Spinbox(
        control_frame,
        from_=1,
        to=99,
        textvariable=quantity_var,
        width=5
    )
    quantity_spinbox.pack(side='left', padx=5)

    # Add to cart button
    def add_selected_to_cart():
        selected_item = product_tree.selection()
        if not selected_item:
            messagebox.showwarning("Select Product", "Please select a product first!")
            return
        
        item = product_tree.item(selected_item[0])
        product_id = item['values'][0]
        quantity = int(quantity_var.get())
        
        if product_id in self.products:
            product = self.products[product_id]
            if product.quantity >= quantity:
                self.current_user.add_to_cart(product, quantity)
                # Update the treeview
                product_tree.set(selected_item[0], 'Stock', product.quantity)
                messagebox.showinfo("Success", f"Added {quantity} {product.name} to cart!")
            else:
                self.out_of_stock(product.name, product.quantity)

    ttk.Button(control_frame, text="Add to Cart", command=add_selected_to_cart).pack(side='left', padx=5)
    ttk.Button(control_frame, text="View Cart", command=self.show_cart).pack(side='left', padx=5)
    ttk.Button(control_frame, text="Back", command=lambda: self.user_menu(self.current_user)).pack(side='right', padx=5)

# Modify the user_menu method to include a button that calls show_product_selection
def user_menu(self, user):
    # Clear previous content
    for widget in self.root.winfo_children():
        widget.destroy()

    # Create welcome label
    welcome_label = ttk.Label(self.root, text=f"Welcome, {user.first_name}!")
    welcome_label.pack(pady=20)

    # Create buttons frame
    buttons_frame = ttk.Frame(self.root)
    buttons_frame.pack(pady=20)

    # Add buttons
    ttk.Button(buttons_frame, text="Browse Products", command=self.show_product_selection).pack(pady=5)
    ttk.Button(buttons_frame, text="View Cart", command=self.show_cart).pack(pady=5)
    ttk.Button(buttons_frame, text="View Order History", command=self.show_history).pack(pady=5)
    ttk.Button(buttons_frame, text="Logout", command=lambda: self.logout(user)).pack(pady=5)