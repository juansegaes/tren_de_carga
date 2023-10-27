import tkinter as tk
from tkinter import ttk
import csv
import os


class RuleManagement:
    def __init__(self, root):
        self.root = root
        self.employees = []
        self.tasks = []
        self.rules = []

        self.load_employees()
        self.load_tasks()

        self.create_gui()
        self.load_rules()

    def load_employees(self):
        filename = "employees.csv"
        filename = os.path.join(os.path.dirname(__file__),"employees.csv")
        try:
            with open(filename, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    self.employees.append(
                        row[0]
                    )  # Assuming the name is in the first column
        except FileNotFoundError:
            print("No se encontró el archivo de empleados")

    def load_tasks(self):
        filename = "tasks.csv"
        filename = os.path.join(os.path.dirname(__file__),"tasks.csv")
        try:
            with open(filename, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    self.tasks.append(
                        row[0]
                    )  # Assuming the task name is in the first column
        except FileNotFoundError:
            print("No se encontró el archivo de tareas")

    def add_rule(self):
        employee1 = self.employee_rule_combobox.get()
        condition1 = self.condition_combobox.get()
        task1 = self.task_rule_combobox.get()
        employee2 = self.employee_rule_combobox2.get()
        condition2 = self.condition_combobox2.get()
        task2 = self.task_rule_combobox2.get()

        rule = f"{employee1},{condition1},{task1},{employee2},{condition2},{task2}"
        self.rules.append(rule)
        self.rules_listbox.insert("end", rule)

    def remove_rule(self):
        selected_rule_index = self.rules_listbox.curselection()
        if selected_rule_index:
            index = selected_rule_index[0]
            self.rules_listbox.delete(index)
            self.rules.pop(index)

    def save_rules(self):
        filename = "rules.csv"
        filename = os.path.join(os.path.dirname(__file__),"rules.csv")
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Team Member 1",
                    "Condition 1",
                    "Task 1",
                    "Team Member 2",
                    "Condition 2",
                    "Task 2",
                ]
            )
            for rule in self.rules:
                rule_parts = rule.split(",")
                if len(rule_parts) == 6:
                    writer.writerow(rule_parts)

    def load_rules(self):
        filename = "rules.csv"
        filename = os.path.join(os.path.dirname(__file__), "rules.csv")
        try:
            with open(filename, "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                for row in reader:
                    rule_parts = row[0].split(",")
                    if len(row) == 6:  # Ensure there are 6 parts in each rule
                        if ",".join(row) not in self.rules:
                            self.rules.append(",".join(row))
                            self.rules_listbox.insert("end", ",".join(row))
        except FileNotFoundError:
            print("No se encontró el archivo de reglas")

    def create_gui(self):
        self.rules_label = tk.Label(self.root, text="Reglas:")
        self.rules_label.pack()

        self.label_si = tk.Label(self.root, text="Si")
        self.label_si.pack()

        self.employee_rule_combobox = ttk.Combobox(self.root, values=self.employees)
        self.employee_rule_combobox.pack()

        self.condition_combobox = ttk.Combobox(self.root, values=["esta", "no esta"])
        self.condition_combobox.set("esta")  # Default value
        self.condition_combobox.pack()

        self.task_rule_combobox = ttk.Combobox(self.root, values=self.tasks)
        self.task_rule_combobox.pack()

        self.label_entonces = tk.Label(self.root, text="entonces")
        self.label_entonces.pack()

        self.employee_rule_combobox2 = ttk.Combobox(self.root, values=self.employees)
        self.employee_rule_combobox2.pack()

        self.condition_combobox2 = ttk.Combobox(
            self.root, values=["debe estar", "no debe estar"]
        )
        self.condition_combobox2.set("debe estar")  # Default value
        self.condition_combobox2.pack()

        self.task_rule_combobox2 = ttk.Combobox(self.root, values=self.tasks)
        self.task_rule_combobox2.pack()

        self.add_rule_button = tk.Button(
            self.root, text="Agregar Regla", command=self.add_rule
        )
        self.add_rule_button.pack()

        self.remove_rule_button = tk.Button(
            self.root, text="Eliminar Regla", command=self.remove_rule
        )
        self.remove_rule_button.pack()

        self.save_rule_button = tk.Button(
            self.root, text="Guardar Reglas", command=self.save_rules
        )
        self.save_rule_button.pack()

        self.load_rule_button = tk.Button(
            self.root, text="Cargar Reglas", command=self.load_rules
        )
        self.load_rule_button.pack()

        self.rules_listbox = tk.Listbox(self.root, width=75, height=10)
        self.rules_listbox.pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestor de Reglas")

    rule_management = RuleManagement(root)

    root.mainloop()
