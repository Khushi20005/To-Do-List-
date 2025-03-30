import tkinter as tk # Importing tkinter for GUI development
from tkinter import ttk, messagebox # Importing themed widgets and messagebox for alerts
from ttkbootstrap import Style #Importing ttkbootstrap for enhanced styling
import json # Importing json for saving and loading tasks

class TodoListApp(tk.Tk):  # Defining the main application class
    def __init__(self): # Initializing the main application
        super().__init__() # Calling the parent class constructor

        self.title("Todo List App") # Setting the window title
        self.geometry("400x400") # Setting the window size
        style = Style(theme="flatly") # Applying a theme from ttkbootstrap
        style.configure("Custon.TEntry", foreground="gray")  # Configuring custom style for entry widget


        # Create input field for adding tasks
        self.task_input = ttk.Entry(self, font=(
            "TkDefaultFont", 16), width=30, style="Custon.TEntry")
        self.task_input.pack(pady=10)

        # Set placeholder for input field
        self.task_input.insert(0, "Enter your todo here...")

        # Bind event to clear placeholder when input field is clicked
        self.task_input.bind("<FocusIn>", self.clear_placeholder)
        # Bind event to restore placeholder when input field loses focus
        self.task_input.bind("<FocusOut>", self.restore_placeholder)

        # Create button for adding tasks
        ttk.Button(self, text="Add", command=self.add_task).pack(pady=5)

        # Create listbox to display added tasks
        self.task_list = tk.Listbox(self, font=(
            "TkDefaultFont", 16), height=10, selectmode=tk.NONE)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create buttons for marking tasks as done or deleting them
        ttk.Button(self, text="Done", style="success.TButton",
                   command=self.mark_done).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self, text="Delete", style="danger.TButton",
                   command=self.delete_task).pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Create buttton for displaying task statistics
        ttk.Button(self, text="View Stats", style="info.TButton",
                   command=self.view_stats).pack(side=tk.BOTTOM, pady=10)
        
        self.load_tasks() # Load tasks from file when the app starts
    
    def view_stats(self): # Function to display task statistics
        done_count = 0
        total_count = self.task_list.size()
        for i in range(total_count):
            if self.task_list.itemcget(i, "fg") == "green": # Checking completed tasks
                done_count += 1
        messagebox.showinfo("Task Statistics", f"Total tasks: {total_count}\nCompleted tasks: {done_count}")

    def add_task(self): # Function to add a new task
        task = self.task_input.get()
        if task != "Enter your todo here...":  # Ensuring task is not empty or default placeholder
            self.task_list.insert(tk.END, task)
            self.task_list.itemconfig(tk.END, fg="orange") # Setting default color for new tasks
            self.task_input.delete(0, tk.END) # Clearing input field after adding task
            self.save_tasks() # Save updated task list

    def mark_done(self): # Function to mark a selected task as done
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.itemconfig(task_index, fg="green") # Changing task color to indicate completion
            self.save_tasks() # Save updated task list
    
    def delete_task(self): # Function to delete a selected task
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.delete(task_index) # Removing task from the list
            self.save_tasks() # Save updated task list
    
    def clear_placeholder(self, event):  # Function to clear placeholder text in the input field
        if self.task_input.get() == "Enter your todo here...":
            self.task_input.delete(0, tk.END)
            self.task_input.configure(style="TEntry")

    def restore_placeholder(self, event): # Function to restore placeholder text if input field is empty
        if self.task_input.get() == "":
            self.task_input.insert(0, "Enter your todo here...")
            self.task_input.configure(style="Custom.TEntry")

    def load_tasks(self): # Function to load tasks from a file
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
                for task in data:
                    self.task_list.insert(tk.END, task["text"])  # Adding task text
                    self.task_list.itemconfig(tk.END, fg=task["color"]) # Restoring task color
        except FileNotFoundError:
            pass # If file is not found, do nothing
    
    def save_tasks(self):  # Function to save tasks to a file
        data = []
        for i in range(self.task_list.size()):
            text = self.task_list.get(i)
            color = self.task_list.itemcget(i, "fg")
            data.append({"text": text, "color": color})
        with open("tasks.json", "w") as f:
            json.dump(data, f) # Saving tasks as JSON

if __name__ == '__main__':  # Running the application
    app = TodoListApp()
    app.mainloop()