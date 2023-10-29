import tkinter as tk
from tkinter import ttk
import csv
import os


class TaskManagement:
    def __init__(self, root):
        self.root = root
        self.tasks = []
        self.create_gui()  # Create the GUI

    def load_tasks(self):
        filename = "tasks.csv"
        filename = os.path.join(os.path.dirname(__file__), "tasks.csv")
        try:
            with open(filename, "r") as file:
                reader = csv.reader(file)
                header = next(reader)  # Skip the header row
                # Find the column indices for Name, Time, Day of the Week, and People Needed
                name_idx = header.index("Nombre")
                time_idx = header.index("Turno")
                day_idx = header.index("Dia de la Semana")
                people_needed_idx = header.index("Personas Necesarias")
                # Clear the existing tasks and listbox entries
                self.tasks.clear()
                self.task_listbox.delete(0, "end")
                for row in reader:
                    name = row[name_idx]
                    time = "Manana" if row[time_idx] == "Manana" else "Tarde"
                    day = "Lunes a Viernes" if row[day_idx] == "0" else row[day_idx]
                    people_needed = row[people_needed_idx]
                    self.tasks.append([name, time, day, people_needed])
                    self.task_listbox.insert(
                        "end",
                        f"{name}, Turno: {time}, Día de la Semana: {day}, Personas Necesarias: {people_needed}",
                    )
        except FileNotFoundError:
            print("No se encontró el archivo de tareas")

    def save_tasks(self):
        filename = "tasks.csv"
        filename = os.path.join(os.path.dirname(__file__), "tasks.csv")
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Nombre", "Turno", "Dia de la Semana", "Personas Necesarias"]
            )
            for task in self.tasks:
                writer.writerow(task)

    def add_task(self):
        name = self.name_entry.get()
        time = self.time_combobox.get()
        day_of_week = self.day_combobox.get()
        people_needed = self.people_entry.get()

        self.tasks.append([name, time, day_of_week, people_needed])
        self.task_listbox.insert(
            "end",
            f"{name}, Turno: {time}, Día de la Semana: {day_of_week}, Personas Necesarias: {people_needed}",
        )

        self.name_entry.delete(0, "end")
        self.people_entry.delete(0, "end")

    def remove_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            self.task_listbox.delete(index)
            self.tasks.pop(index)

    def create_gui(self):
        self.name_label = tk.Label(self.root, text="Nombre:")
        self.name_label.pack()

        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        self.time_label = tk.Label(self.root, text="Turno (Mañana/Tarde):")
        self.time_label.pack()

        self.time_combobox = ttk.Combobox(self.root, values=["Manana", "Tarde"])
        self.time_combobox.set("Manana")
        self.time_combobox.pack()

        self.day_label = tk.Label(self.root, text="Día de la Semana:")
        self.day_label.pack()

        self.day_combobox = ttk.Combobox(
            self.root,
            values=[
                "Lunes a Viernes",
                "Lunes",
                "Martes",
                "Miércoles",
                "Jueves",
                "Viernes",
                "Sábado",
                "Domingo",
            ],
        )
        self.day_combobox.set("Lunes a Viernes")
        self.day_combobox.pack()

        self.people_label = tk.Label(self.root, text="Personas Necesarias:")
        self.people_label.pack()

        self.people_entry = tk.Entry(self.root)
        self.people_entry.pack()

        self.add_button = tk.Button(
            self.root, text="Agregar Tarea", command=self.add_task
        )
        self.add_button.pack()

        self.remove_button = tk.Button(
            self.root, text="Eliminar Tarea", command=self.remove_task
        )
        self.remove_button.pack()

        self.save_button = tk.Button(
            self.root, text="Guardar Tareas", command=self.save_tasks
        )
        self.save_button.pack()

        self.load_button = tk.Button(
            self.root, text="Cargar Tareas", command=self.load_tasks
        )
        self.load_button.pack()

        self.task_listbox = tk.Listbox(self.root, width=100, height=10)
        self.task_listbox.pack()

        # Initialize tasks
        self.tasks = []
        self.load_tasks()  # Load tasks at the beginning


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Planificador de Tareas")

    task_management = TaskManagement(root)

    root.mainloop()
