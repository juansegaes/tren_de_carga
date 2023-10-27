import random
import copy
import csv
import os


# Estructura días
class Dia:
    def init(
        self,
        dia,
        lista_comite_manana,
        lista_comite_tarde,
        lista_repricing_manana,
        lista_repricing_tarde,
        lista_inmobiliaria_manana,
        lista_inmobiliaria_tarde,
    ):
        self.dia = dia
        self.lista_comite_manana = lista_comite_manana
        self.lista_comite_tarde = lista_comite_tarde
        self.lista_repricing_manana = lista_repricing_manana
        self.lista_repricing_tarde = lista_repricing_tarde
        self.lista_inmobiliaria_manana = lista_inmobiliaria_manana
        self.lista_inmobiliaria_tarde = lista_inmobiliaria_tarde


# funcion acomodar


class Tarea:
    def __init__(self, nombre, cant_equipo, hora):
        self.nombre = nombre
        self.cant_equipo = cant_equipo
        self.team = [[], [], [], [], []]
        self.hora = hora

    def __print__(self):
        return self.nombre

    def __eq__(self, other):
        return (
            self.nombre == other.nombre
            and self.hora == other.hora
            and self.cant_equipo == other.cant_equipo
        )


class Empleado:
    def __init__(self, nombre, horas):
        self.nombre = nombre
        self.horas = horas

    def __str__(self):
        return self.nombre

    def __print__(self):
        return self.nombre


class Regla:
    def __init__(self, empleado1, condicion1, tarea1, empleado2, condicion2, tarea2):
        self.empleado1 = empleado1
        self.condicion1 = condicion1
        self.tarea1 = tarea1
        self.empleado2 = empleado2
        self.condicion2 = condicion2
        self.tarea2 = tarea2


class Day:
    def __init__(self, nombre):
        self.nombre = nombre
        self.tareas_manana = []
        self.tareas_tarde = []
        self.reglas = []
        self.indice = 0
        if self.nombre == "Lunes":
            self.indice = 0
        elif self.nombre == "Martes":
            self.indice = 1
        elif self.nombre == "Miercoles":
            self.indice = 2
        elif self.nombre == "Jueves":
            self.indice = 3
        elif self.nombre == "Viernes":
            self.indice = 4


    def __print__(self):
        print(self.nombre)
        for t in self.tareas_manana:
            print("**" + t.nombre)
            for e in t.team[self.indice]:
                print(e.nombre)
        for t in self.tareas_tarde:
            print("**" + t.nombre)
            for e in t.team[self.indice]:
                print(e.nombre)
        print("-------------------------")

    def resultado(self):
        # a string with the list of tasks and employees
        resultado = []
        for t in self.tareas_manana:
            resultado.append("**" + t.nombre)
            for e in t.team[self.indice]:
                resultado.append(e.nombre)
        for t in self.tareas_tarde:
            resultado.append("**" + t.nombre)
            for e in t.team[self.indice]:
                resultado.append(e.nombre)
        # return "test"
        return resultado


class Semana:
    def __init__(self):
        self.dias = []
        self.dias.append(Day("Lunes"))
        self.dias.append(Day("Martes"))
        self.dias.append(Day("Miercoles"))
        self.dias.append(Day("Jueves"))
        self.dias.append(Day("Viernes"))

        self.empleados = []
        self.Cargar_Empleados()

        self.tareas = []
        self.Cargar_Tareas()

        self.reglas = []
        self.Cargar_Reglas()

    def Cargar_Empleados(self):
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
                for row in reader:
                    name = row[name_idx]
                    availability = int(row[avail_idx])
                    if availability == 1:
                        self.empleados.append(Empleado(name, 0))
        except FileNotFoundError:
            print(f"File {filename} not found")

    def Cargar_Tareas(self):
        # raise NotImplementedError("Subclass must implement abstract method"        filename = "tasks.csv"

        filename = "tasks.csv"
        filename = os.path.join(os.path.dirname(__file__),"tasks.csv")
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
                for row in reader:
                    name = row[name_idx]
                    time = 0 if row[time_idx] == "Manana" else 1
                    # day = "Lunes a Viernes" if row[day_idx] == "0" else row[day_idx]
                    people_needed = int(row[people_needed_idx])
                    self.tareas.append(Tarea(name, people_needed, time))

                    if row[day_idx] == "Lunes":
                        if time == 0:
                            self.dias[0].tareas_manana.append(self.tareas[-1])
                        else:
                            self.dias[0].tareas_tarde.append(self.tareas[-1])
                    elif row[day_idx] == "Martes":
                        if time == 0:
                            self.dias[1].tareas_manana.append(self.tareas[-1])
                        else:
                            self.dias[1].tareas_tarde.append(self.tareas[-1])
                    elif row[day_idx] == "Miercoles":
                        if time == 0:
                            self.dias[2].tareas_manana.append(self.tareas[-1])
                        else:
                            self.dias[2].tareas_tarde.append(self.tareas[-1])
                    elif row[day_idx] == "Jueves":
                        if time == 0:
                            self.dias[3].tareas_manana.append(self.tareas[-1])
                        else:
                            self.dias[3].tareas_tarde.append(self.tareas[-1])
                    elif row[day_idx] == "Viernes":
                        if time == 0:
                            self.dias[4].tareas_manana.append(self.tareas[-1])
                        else:
                            self.dias[4].tareas_tarde.append(self.tareas[-1])
                    elif row[day_idx] == "Lunes a Viernes":
                        if time == 0:
                            self.dias[0].tareas_manana.append(self.tareas[-1])
                            self.dias[1].tareas_manana.append(self.tareas[-1])
                            self.dias[2].tareas_manana.append(self.tareas[-1])
                            self.dias[3].tareas_manana.append(self.tareas[-1])
                            self.dias[4].tareas_manana.append(self.tareas[-1])
                        else:
                            self.dias[0].tareas_tarde.append(self.tareas[-1])
                            self.dias[1].tareas_tarde.append(self.tareas[-1])
                            self.dias[2].tareas_tarde.append(self.tareas[-1])
                            self.dias[3].tareas_tarde.append(self.tareas[-1])
                            self.dias[4].tareas_tarde.append(self.tareas[-1])

        except FileNotFoundError:
            print("No se encontró el archivo de tareas")

    def Cargar_Reglas(self):
        filename = "rules.csv"
        filename = os.path.join(os.path.dirname(__file__),"rules.csv")
        try:
            with open(filename, "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                for row in reader:
                    if len(row) == 6:  # Ensure there are 6 parts in each rule
                        tmp_emp1 = self.search_empleado_index(row[0])
                        if row[1] == "esta":
                            tmp_cond1 = 1
                        else:
                            tmp_cond1 = 0
                        tmp_tarea1 = self.search_tarea_index(row[2])
                        tmp_emp2 = self.search_empleado_index(row[3])
                        if row[4] == "debe estar":
                            tmp_cond2 = 1
                        else:
                            tmp_cond2 = 0
                        tmp_tarea2 = self.search_tarea_index(row[5])
                        self.reglas.append(
                            Regla(
                                tmp_emp1,
                                tmp_cond1,
                                tmp_tarea1,
                                tmp_emp2,
                                tmp_cond2,
                                tmp_tarea2,
                            )
                        )

        except FileNotFoundError:
            print("No se encontró el archivo de reglas")

    def search_tarea_index(self, nombre):
        for i in range(len(self.tareas)):
            if self.tareas[i].nombre == nombre:
                return i
        raise Exception("Tarea no encontrada")

    def search_empleado_index(self, nombre):
        for i in range(len(self.empleados)):
            if self.empleados[i].nombre == nombre:
                return i
        raise Exception("Empleado no encontrado")

    def dif_horarios(
        self,
    ):
        maximo = 0
        minimo = 100
        for e in self.empleados:
            if e.horas > maximo:
                maximo = e.horas
            if e.horas < minimo:
                minimo = e.horas
        return maximo - minimo

    def intentar_horario(self):
        self.limpiar()
        for dia in self.dias:
            ocupados = []
            for tarea in dia.tareas_manana:
                while len(tarea.team[dia.indice]) < tarea.cant_equipo:
                    rnd = random.randint(0, len(self.empleados) - 1)
                    if self.empleados[rnd] not in ocupados:
                        tarea.team[dia.indice].append(self.empleados[rnd])
                        ocupados.append(self.empleados[rnd])
                        self.empleados[rnd].horas += 1

            ocupados = []
            for tarea in dia.tareas_tarde:
                while len(tarea.team[dia.indice]) < tarea.cant_equipo:
                    rnd = random.randint(0, len(self.empleados) - 1)
                    if self.empleados[rnd] not in ocupados:
                        tarea.team[dia.indice].append(self.empleados[rnd])
                        ocupados.append(self.empleados[rnd])
                        self.empleados[rnd].horas += 1

    def limpiar(self):
        for e in self.empleados:
            e.horas = 0
        for t in self.tareas:
            t.team = [[], [], [], [], []]

    def revisar_horario(self):
        if self.dif_horarios() > 2:
            return False

        for reg in self.reglas:
            if reg.condicion1 == 1:
                if reg.condicion2 == 1:
                    for day in self.dias:
                        if (
                            self.empleados[reg.empleado1]
                            in self.tareas[reg.tarea1].team[day.indice]
                            and self.empleados[reg.empleado2]
                            not in self.tareas[reg.tarea2].team[day.indice]
                        ):
                            return False
            if reg.condicion1 == 1:
                if reg.condicion2 == 0:
                    for day in self.dias:
                        if (
                            self.empleados[reg.empleado1]
                            in self.tareas[reg.tarea1].team[day.indice]
                            and self.empleados[reg.empleado2]
                            in self.tareas[reg.tarea2].team[day.indice]
                        ):
                            return False
            if reg.condicion1 == 0:
                if reg.condicion2 == 1:
                    for day in self.dias:
                        if (
                            self.empleados[reg.empleado1]
                            not in self.tareas[reg.tarea1].team[day.indice]
                            and self.empleados[reg.empleado2]
                            not in self.tareas[reg.tarea2].team[day.indice]
                        ):
                            return False
            if reg.condicion1 == 0:
                if reg.condicion2 == 0:
                    for day in self.dias:
                        if (
                            self.empleados[reg.empleado1]
                            not in self.tareas[reg.tarea1].team[day.indice]
                            and self.empleados[reg.empleado2]
                            in self.tareas[reg.tarea2].team[day.indice]
                        ):
                            return False
        return True

    def organizar(self):
        works = False
        while not works:
            self.intentar_horario()
            works = self.revisar_horario()

    def __print__(self):
        for d in self.dias:
            d.__print__()


# semana = Semana()
#
# semana.organizar()
# semana.__print__()

# def Acomodar(dias, empleados):
#    for dia in dias:
#        empleados2 = copy.copy(empleados)
#        # primer emple de la mañana
#        aleatorio = random.randint(0, len(empleados2) - 1)
#        dia.lista_comite_manana.append(empleados2[aleatorio])
#        for emp in empleados:
#            if emp.nombre == empleados2[aleatorio].nombre:
#                emp.horas = emp.horas + 1
#        empleados2.pop(aleatorio)
#        # segundo emple de la mañana
#        aleatorio = random.randint(0, len(empleados2) - 1)
#        dia.lista_comite_manana.append(empleados2[aleatorio])
#        for emp in empleados:
#            if emp.nombre == empleados2[aleatorio].nombre:
#                emp.horas = emp.horas + 1
#        empleados2.pop(aleatorio)
#        # tercer emple de la mañana
#        aleatorio = random.randint(0, len(empleados2) - 1)
#        dia.lista_comite_manana.append(empleados2[aleatorio])
#        for emp in empleados:
#            if emp.nombre == empleados2[aleatorio].nombre:
#                emp.horas = emp.horas + 1
#        empleados2.pop(aleatorio)
#        # repricing manana
#        aleatorio = random.randint(0, len(empleados2) - 1)
#        dia.lista_repricing_manana.append(empleados2[aleatorio])
#        for emp in empleados:
#            if emp.nombre == empleados2[aleatorio].nombre:
#                emp.horas = emp.horas + 1
#        # primer emple de la tarde
#        aleatorio = random.randint(0, len(empleados2) - 1)
#        dia.lista_comite_tarde.append(empleados2[aleatorio])
#        for emp in empleados:
#            if emp.nombre == empleados2[aleatorio].nombre:
#                emp.horas = emp.horas + 1
#        empleados2.pop(aleatorio)
#        # segundo emple de la tarde
#        aleatorio = random.randint(0, len(empleados2) - 1)
#        dia.lista_comite_tarde.append(empleados2[aleatorio])
#        for emp in empleados:
#            if emp.nombre == empleados2[aleatorio].nombre:
#                emp.horas = emp.horas + 1
#        empleados2.pop(aleatorio)
#        # tercer emple de la tarde
#        aleatorio = random.randint(0, len(empleados2) - 1)
#        dia.lista_comite_tarde.append(empleados2[aleatorio])
#        for emp in empleados:
#            if emp.nombre == empleados2[aleatorio].nombre:
#                emp.horas = emp.horas + 1
#        empleados2.pop(aleatorio)
#        # repricing tarde
#        tmp = copy.copy(dia.lista_comite_tarde)
#        tmp.extend(dia.lista_repricing_manana)
#        candidantos_rep_tarde = list(set(empleados) - set(tmp))
#        aleatorio = random.randint(0, len(candidantos_rep_tarde) - 1)
#        dia.lista_repricing_tarde.append(candidantos_rep_tarde[aleatorio])
#        for emp in empleados:
#            if emp.nombre == candidantos_rep_tarde[aleatorio].nombre:
#                emp.horas = emp.horas + 1
#
#
## funcion funciona
#
#
# def Funciona(dias, empleados):
#    cumple = True
#    for dia in dias:
#        if (
#            manuelalopez in dia.lista_comite_manana
#            and santiagosimbaqueba in dia.lista_comite_manana
#        ):
#            cumple = False
#        if (
#            manuelalopez in dia.lista_comite_tarde
#            and santiagosimbaqueba in dia.lista_comite_tarde
#        ):
#            cumple = False
#        # if danielamaya in dia.lista_comite_manana and danielacadena in dia.lista_comite_manana:
#        # cumple = False
#        # if danielamaya in dia.lista_comite_tarde and danielacadena in dia.lista_comite_tarde:
#        # cumple = False
