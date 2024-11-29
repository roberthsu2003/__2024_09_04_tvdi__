from tkinter import ttk, messagebox

class TreeViewWidget(ttk.Frame):
    """
    A reusable widget containing a Treeview to manage a list of items.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        

        # Define the Treeview
        self.tree = ttk.Treeview(self, columns=("Title",), show="headings")
        self.tree.heading("Title", text="片名")
        self.tree.column("Title", width=200, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configure the Treeview to use scrollbar
        self.tree.configure(yscrollcommand=self.scrollbar.set)

    def get_children(self):
        """
        Returns the list of all children items in the Treeview.
        """
        return self.tree.get_children()

    def add_item(self, item_name):
        """
        Adds an item to the TreeView if it doesn't already exist.
        """
        # Prevent duplicate items
        for child in self.tree.get_children():
            if self.tree.item(child, 'values')[0] == item_name:
                messagebox.showinfo("提示", f"'{item_name}' 已經存在於列表中!")
                return
        # Add the new item
        self.tree.insert("", "end", values=(item_name,))

    def remove_selected_item(self):
        """
        Removes the currently selected item from the Treeview.
        """
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "請先選擇要刪除的項目!")
            return
        
        for item in selected_items:
            self.tree.delete(item)

    def get_selected_item(self):
        """
        Returns the currently selected item's value.
        Returns None if no item is selected.
        """
        selected_items = self.tree.selection()
        if not selected_items:
            return None
        return self.tree.item(selected_items[0], 'values')[0]

    def clear_all(self):
        """
        Removes all items from the Treeview.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

    def get_all_items(self):
        """
        Returns a list of all items' values in the Treeview.
        """
        return [self.tree.item(child, 'values')[0] 
                for child in self.tree.get_children()]