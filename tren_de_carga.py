import tkinter as tk
from tkinter import ttk
import equipo
import tareas
import reglas
import logica


class MainProgram:
    def __init__(self, root):
        self.root = root
        self.create_gui()

    def open_team_management(self):
        team_gui = tk.Tk()
        team_gui.title("Gestor de Equipos")
        team_management = equipo.TeamManagement(team_gui)
        team_gui.mainloop()

    def open_task_management(self):
        task_gui = tk.Tk()
        task_gui.title("Gestor de Tareas")
        task_management = tareas.TaskManagement(task_gui)
        task_gui.mainloop()

    def open_rule_management(self):
        rule_gui = tk.Tk()
        rule_gui.title("Gestor de Reglas")
        rule_management = reglas.RuleManagement(rule_gui)
        rule_gui.mainloop()

    def generate_schedule(self):
        semana = logica.Semana()
        semana.organizar()
        for j in range(5):
            self.listboxes[j].delete(0, tk.END)
            for i in range(len((semana.dias[j]).resultado())):
                self.listboxes[j].insert(tk.END, (semana.dias[j]).resultado()[i])

        # Placeholder for schedule generation logic
        # You can add your schedule generation code here
        #print("Generating schedule...")

    def create_gui(self):
        self.team_button = tk.Button(
            self.root, text="Gestionar Equipos", command=self.open_team_management
        )
        self.team_button.grid(row=0, column=0, padx=10, pady=10)

        self.task_button = tk.Button(
            self.root, text="Gestionar Tareas", command=self.open_task_management
        )
        self.task_button.grid(row=0, column=1, padx=10, pady=10)

        self.rule_button = tk.Button(
            self.root, text="Gestionar Reglas", command=self.open_rule_management
        )
        self.rule_button.grid(row=0, column=2, padx=10, pady=10)

        self.schedule_button = tk.Button(
            self.root, text="Generar Calendario", command=self.generate_schedule
        )
        self.schedule_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Create a week calendar (excluding Saturday and Sunday)
        week_days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        self.listboxes = []
        for i, day in enumerate(week_days):
            label = tk.Label(self.root, text=day)
            label.grid(row=2, column=i, padx=10, pady=10)
            listbox = tk.Listbox(self.root, width=30, height=25)
            listbox.grid(row=3, column=i, padx=10, pady=10)
            self.listboxes.append(listbox)
            # Add horizontal scroll bar
            scroll_x = ttk.Scrollbar(
                self.root, orient="horizontal", command=listbox.xview
            )
            scroll_x.grid(row=4, column=i, padx=10, pady=10, sticky="ew")
            listbox.config(xscrollcommand=scroll_x.set)

        # Add a big horizontal scrollbar
        big_scroll_x = ttk.Scrollbar(
            self.root, orient="horizontal", command=self.scroll_listboxes
        )
        big_scroll_x.grid(row=5, column=0, columnspan=5, padx=10, pady=10, sticky="ew")
        self.root.grid_columnconfigure(0, weight=1)

    def scroll_listboxes(self, *args):
        for listbox in self.listboxes:
            listbox.xview(*args)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Programa Principal")

    main_program = MainProgram(root)

    root.mainloop()
