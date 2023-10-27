import tkinter as tk
from tkinter import ttk
import csv
import os

class TeamManagement:
    def __init__(self, root):
        self.root = root
        self.employees = []
        self.create_gui()  # Create the GUI

    def load_employees(self):
        filename = "employees.csv"
        filename = os.path.join(os.path.dirname(__file__),"employees.csv")
        try:
            with open(filename, "r") as file:
                reader = csv.reader(file)
                header = next(reader)  # Skip the header row
                # Find the column indices for Name and Availability
                name_idx = header.index("Nombre")
                avail_idx = header.index("Disponibilidad")
                # Clear the existing employees and listbox entries
                self.employees.clear()
                self.employee_listbox.delete(0, "end")
                for row in reader:
                    name = row[name_idx]
                    availability = int(row[avail_idx])
                    self.employees.append([name, availability])
                    availability_str = (
                        "Disponible" if availability == 1 else "No disponible"
                    )
                    self.employee_listbox.insert("end", f"{name}, {availability_str}")
        except FileNotFoundError:
            print("No se encontró el archivo de empleados")

    def save_employees(self):
        filename = "employees.csv"
        filename = os.path.join(os.path.dirname(__file__),"employees.csv")
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Nombre", "Disponibilidad"])
            for employee in self.employees:
                writer.writerow(employee)

    def add_employee(self):
        name = self.employee_name_entry.get()
        availability = self.employee_avail_combobox.get()
        availability = 1 if availability == "Disponible" else 0

        self.employees.append([name, availability])
        availability_str = "Disponible" if availability == 1 else "No disponible"
        self.employee_listbox.insert("end", f"{name}, {availability_str}")

        self.employee_name_entry.delete(0, "end")

    def remove_employee(self):
        selected_employee_index = self.employee_listbox.curselection()
        if selected_employee_index:
            index = selected_employee_index[0]
            self.employee_listbox.delete(index)
            self.employees.pop(index)

    def toggle_availability(self):
        selected_employee_index = self.employee_listbox.curselection()
        if selected_employee_index:
            index = selected_employee_index[0]
            name, availability = self.employees[index]
            new_availability = 1 - availability  # Toggle the availability
            self.employees[index] = [name, new_availability]
            availability_str = (
                "Disponible" if new_availability == 1 else "No disponible"
            )
            self.employee_listbox.delete(index)
            self.employee_listbox.insert(index, f"{name}, {availability_str}")

    def create_gui(self):
        self.employee_name_label = tk.Label(self.root, text="Nombre:")
        self.employee_name_label.pack()

        self.employee_name_entry = tk.Entry(self.root)
        self.employee_name_entry.pack()

        self.employee_avail_label = tk.Label(self.root, text="Disponibilidad:")
        self.employee_avail_label.pack()

        self.employee_avail_combobox = ttk.Combobox(
            self.root, values=["Disponible", "No disponible"]
        )
        self.employee_avail_combobox.set("Disponible")
        self.employee_avail_combobox.pack()

        self.add_employee_button = tk.Button(
            self.root, text="Agregar Empleado", command=self.add_employee
        )
        self.add_employee_button.pack()

        self.remove_employee_button = tk.Button(
            self.root, text="Eliminar Empleado", command=self.remove_employee
        )
        self.remove_employee_button.pack()

        self.toggle_availability_button = tk.Button(
            self.root, text="Cambiar Disponibilidad", command=self.toggle_availability
        )
        self.toggle_availability_button.pack()

        self.save_employee_button = tk.Button(
            self.root, text="Guardar Empleados", command=self.save_employees
        )
        self.save_employee_button.pack()

        self.load_employee_button = tk.Button(
            self.root, text="Cargar Empleados", command=self.load_employees
        )
        self.load_employee_button.pack()

        self.employee_listbox = tk.Listbox(self.root, width=50, height=10)
        self.employee_listbox.pack()

        # Initialize employees
        self.load_employees()  # Load employees at the beginning


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestor de Equipos")

    team_management = TeamManagement(root)

    root.mainloop()
