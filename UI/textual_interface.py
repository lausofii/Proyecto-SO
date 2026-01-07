"""
Interfaz principal del simulador usando Textual
Implementa todas las funcionalidades del proyecto con interfaz gráfica de terminal
"""
import sys
import os
from copy import deepcopy
from datetime import datetime

# Configurar rutas para importaciones
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Button, Header, Footer, Static, DataTable, Input, Select, 
    Label, TextArea, Tabs, Tab, Log, Rule
)
from textual.binding import Binding
from textual.screen import Screen, ModalScreen
from textual import events

# Importaciones del proyecto
try:
    from Core.process import Process
    from Core.algorithms.fcfs import FCFS
    from Core.algorithms.sjf import SJF
    from Core.algorithms.round_robin import RoundRobin
    from Core.algorithms.priority import PriorityScheduler
    from Utils.file_handler import FileHandler
    from Utils.process_generator import ProcessGenerator
    from UI.results_display import ResultsDisplay
except ImportError as e:
    print(f"Error de importación: {e}")
    sys.exit(1)


class CPUSchedulerApp(App):
    """Aplicación principal del simulador de planificación de CPU"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #main-container {
        width: 100%;
        height: 100%;
        padding: 1;
    }
    
    #header-text {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin: 1;
    }
    
    #menu-container {
        width: 100%;
        height: auto;
        padding: 1;
        align: center middle;
    }
    
    Button {
        width: 50;
        margin: 1;
    }
    
    .menu-button {
        width: 70;
        margin: 1;
    }
    
    DataTable {
        width: 100%;
        height: auto;
    }
    
    #process-table {
        height: 15;
    }
    
    #results-container {
        height: auto;
        padding: 1;
    }
    
    .metric-label {
        text-style: bold;
        color: $primary;
        margin: 1;
    }
    
    #gantt-display {
        height: auto;
        padding: 1;
        border: solid $primary;
        background: $panel;
    }
    
    #dialog {
        width: 50;
        height: auto;
        padding: 2;
        border: solid $primary;
        background: $panel;
        align: center middle;
    }
    
    #no-files {
        margin: 1;
        color: $warning;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Salir", priority=True),
        Binding("escape", "back", "Atrás", priority=True),
    ]
    
    def __init__(self):
        super().__init__()
        self.processes = []
        self.file_handler = FileHandler()
        self.process_generator = ProcessGenerator()
        self.results_display = ResultsDisplay()
        self.schedulers = {
            "1": ("FCFS (First Come First Served)", FCFS()),
            "2": ("SJF (Shortest Job First - No apropiativo)", SJF()),
            "3": ("Round Robin (Quantum configurable)", RoundRobin()),
            "4": ("Prioridades (sin desalojo)", PriorityScheduler(preemptive=False)),
            "5": ("Prioridades (con desalojo)", PriorityScheduler(preemptive=True))
        }
        self.default_quantum = 4
    
    def compose(self) -> ComposeResult:
        """Construye la interfaz principal"""
        yield Header(show_clock=True)
        yield Footer()
        
        with Container(id="main-container"):
            yield Static(
                "SIMULADOR DE ALGORITMOS DE PLANIFICACIÓN DE CPU\n"
                "Universidad Católica Andrés Bello - Sistemas Operativos\n"
                "Equipo 7: Maria, Laura, Andrea",
                id="header-text"
            )
            
            with Container(id="menu-container"):
                yield Button("1. Cargar procesos desde archivo", id="load-file", classes="menu-button")
                yield Button("2. Crear procesos manualmente", id="create-manual", classes="menu-button")
                yield Button("3. Usar casos de prueba predefinidos", id="test-cases", classes="menu-button")
                yield Button("4. Ejecutar simulación", id="run-simulation", classes="menu-button")
                yield Button("5. Comparar todos los algoritmos", id="compare", classes="menu-button")
                yield Button("6. Ver historial de resultados", id="history", classes="menu-button")
                yield Button("7. Configurar parámetros", id="configure", classes="menu-button")
            
            with Container(id="process-info"):
                yield Static(f"Procesos cargados: {len(self.processes)}", id="process-count")
                yield DataTable(id="process-table")
    
    def on_mount(self) -> None:
        """Se ejecuta cuando la app se monta"""
        self.update_process_table()
    
    def update_process_table(self):
        """Actualiza la tabla de procesos"""
        count_label = self.query_one("#process-count", Static)
        count_label.update(f"Procesos cargados: {len(self.processes)}")
        
        try:
            table = self.query_one("#process-table", DataTable)
            table.clear()
            table.add_columns("PID", "Llegada", "Ráfaga", "Prioridad")
            
            if self.processes:
                for p in self.processes[:10]:  # Mostrar máximo 10
                    table.add_row(p.pid, str(p.arrival_time), str(p.burst_time), str(p.priority))
        except:
            pass  # La tabla se creará en on_mount
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja los clicks en los botones"""
        button_id = event.button.id
        
        if button_id == "load-file":
            self.push_screen(LoadFileScreen(self))
        elif button_id == "create-manual":
            self.push_screen(CreateManualScreen(self))
        elif button_id == "test-cases":
            self.push_screen(TestCasesScreen(self))
        elif button_id == "run-simulation":
            if not self.processes:
                self.notify("⚠️ No hay procesos cargados. Cargue procesos primero.", severity="warning")
            else:
                self.push_screen(RunSimulationScreen(self))
        elif button_id == "compare":
            if not self.processes:
                self.notify("⚠️ No hay procesos cargados. Cargue procesos primero.", severity="warning")
            else:
                self.push_screen(CompareScreen(self))
        elif button_id == "history":
            self.push_screen(HistoryScreen(self))
        elif button_id == "configure":
            self.push_screen(ConfigureScreen(self))
    
    def action_quit(self) -> None:
        """Acción para salir"""
        self.exit()
    
    def action_back(self) -> None:
        """Acción para volver atrás"""
        if len(self.screen_stack) > 1:
            self.pop_screen()


class LoadFileScreen(Screen):
    """Pantalla para cargar procesos desde archivo"""
    
    CSS = """
    #file-list {
        height: 15;
        border: solid $primary;
        margin: 1;
    }
    
    #file-input {
        width: 50;
        margin: 1;
    }
    """
    
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        
        with Container():
            yield Static("CARGAR PROCESOS DESDE ARCHIVO", id="header-text")
            
            # Listar archivos disponibles
            data_dir = "data"
            files = []
            if os.path.exists(data_dir):
                files = [f for f in os.listdir(data_dir) 
                        if f.endswith(('.json', '.txt', '.csv')) and f != "simulation_history.json"]
            
            if files:
                yield Static("Archivos disponibles:", classes="metric-label")
                yield DataTable(id="file-list")
            else:
                yield Static("No hay archivos en la carpeta 'data/'.", id="no-files")
            
            yield Static("O ingrese el nombre del archivo:", classes="metric-label")
            with Horizontal():
                yield Input(placeholder="ej: conjunto1.json", id="file-input")
                yield Button("Cargar", id="load-btn")
            
            yield Button("Volver", id="back-btn")
    
    def on_mount(self) -> None:
        """Carga la lista de archivos"""
        table = self.query_one("#file-list", DataTable, can_raise=False)
        if table:
            table.add_columns("#", "Nombre del archivo")
            data_dir = "data"
            if os.path.exists(data_dir):
                files = [f for f in os.listdir(data_dir) 
                        if f.endswith(('.json', '.txt', '.csv')) and f != "simulation_history.json"]
                for i, file in enumerate(files, 1):
                    table.add_row(str(i), file)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja clicks en botones"""
        if event.button.id == "load-btn":
            self.load_file()
        elif event.button.id == "back-btn":
            self.dismiss()
    
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Cuando se selecciona un archivo de la tabla"""
        row_key = event.data_table.get_row(event.cursor_row)
        filename = row_key[1]  # El nombre del archivo está en la segunda columna
        input_widget = self.query_one("#file-input", Input)
        input_widget.value = filename
    
    def load_file(self):
        """Carga el archivo seleccionado"""
        input_widget = self.query_one("#file-input", Input)
        filename = input_widget.value.strip()
        
        if not filename:
            self.notify("⚠️ Ingrese un nombre de archivo", severity="warning")
            return
        
        # Si no tiene extensión, agregar .json por defecto
        if '.' not in filename:
            filename += '.json'
        
        try:
            self.parent_app.processes = self.parent_app.file_handler.load_processes(filename)
            self.parent_app.update_process_table()
            self.notify(f"✅ Cargados {len(self.parent_app.processes)} procesos exitosamente", severity="success")
            self.dismiss()
        except FileNotFoundError:
            self.notify(f"❌ Archivo no encontrado: {filename}", severity="error")
        except Exception as e:
            self.notify(f"❌ Error al cargar archivo: {e}", severity="error")


class CreateManualScreen(Screen):
    """Pantalla para crear procesos manualmente"""
    
    CSS = """
    #form-container {
        padding: 1;
    }
    
    .form-row {
        height: 3;
        margin: 1;
    }
    """
    
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        self.editing_index = None
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        
        with Container():
            yield Static("CREAR PROCESOS MANUALMENTE", id="header-text")
            
            with Container(id="form-container"):
                yield Static("PID:", classes="metric-label")
                yield Input(placeholder="ej: P1", id="pid-input")
                
                yield Static("Tiempo de llegada:", classes="metric-label")
                yield Input(placeholder="0", id="arrival-input")
                
                yield Static("Tiempo de ráfaga:", classes="metric-label")
                yield Input(placeholder="5", id="burst-input")
                
                yield Static("Prioridad:", classes="metric-label")
                yield Input(placeholder="1", id="priority-input")
            
            with Horizontal():
                yield Button("Agregar", id="add-btn")
                yield Button("Limpiar", id="clear-btn")
            
            yield DataTable(id="process-table")
            
            with Horizontal():
                yield Button("Guardar y volver", id="save-btn")
                yield Button("Volver sin guardar", id="back-btn")
    
    def on_mount(self) -> None:
        """Inicializa la tabla"""
        table = self.query_one("#process-table", DataTable)
        table.add_columns("PID", "Llegada", "Ráfaga", "Prioridad", "Acción")
        self.update_table()
    
    def update_table(self):
        """Actualiza la tabla de procesos"""
        table = self.query_one("#process-table", DataTable)
        table.clear()
        table.add_columns("PID", "Llegada", "Ráfaga", "Prioridad", "Acción")
        
        for i, p in enumerate(self.parent_app.processes):
            table.add_row(p.pid, str(p.arrival_time), str(p.burst_time), 
                         str(p.priority), "Eliminar", key=str(i))
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja clicks en botones"""
        if event.button.id == "add-btn":
            self.add_process()
        elif event.button.id == "clear-btn":
            self.clear_form()
        elif event.button.id == "save-btn":
            self.dismiss()
        elif event.button.id == "back-btn":
            self.dismiss()
    
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Cuando se selecciona una fila para eliminar"""
        row_key = event.data_table.get_row_key(event.cursor_row)
        if row_key:
            index = int(row_key)
            if 0 <= index < len(self.parent_app.processes):
                self.parent_app.processes.pop(index)
                self.update_table()
                self.parent_app.update_process_table()
                self.notify("✅ Proceso eliminado", severity="success")
    
    def add_process(self):
        """Agrega un proceso"""
        try:
            pid = self.query_one("#pid-input", Input).value.strip()
            arrival = int(self.query_one("#arrival-input", Input).value or "0")
            burst = int(self.query_one("#burst-input", Input).value or "1")
            priority = int(self.query_one("#priority-input", Input).value or "1")
            
            if not pid:
                self.notify("⚠️ El PID no puede estar vacío", severity="warning")
                return
            
            process = Process(pid, arrival, burst, priority)
            self.parent_app.processes.append(process)
            self.update_table()
            self.parent_app.update_process_table()
            self.clear_form()
            self.notify(f"✅ Proceso {pid} agregado", severity="success")
        except ValueError:
            self.notify("❌ Error: Ingrese valores numéricos válidos", severity="error")
    
    def clear_form(self):
        """Limpia el formulario"""
        self.query_one("#pid-input", Input).value = ""
        self.query_one("#arrival-input", Input).value = ""
        self.query_one("#burst-input", Input).value = ""
        self.query_one("#priority-input", Input).value = ""


class TestCasesScreen(Screen):
    """Pantalla para seleccionar casos de prueba predefinidos"""
    
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        
        with Container():
            yield Static("CASOS DE PRUEBA PREDEFINIDOS", id="header-text")
            
            yield Button("1. Conjunto 1: Procesos Básicos (4 procesos)\n"
                        "   P1(0,8,3), P2(1,4,1), P3(2,9,4), P4(3,5,2)", 
                        id="case1", classes="menu-button")
            
            yield Button("2. Conjunto 2: Procesos Variados (5 procesos)\n"
                        "   P1(0,10,2), P2(2,3,1), P3(4,6,3), P4(6,1,1), P5(8,4,2)", 
                        id="case2", classes="menu-button")
            
            yield Button("3. Conjunto 3: Caso Personal (6 procesos)\n"
                        "   P1(0,7,1), P2(2,4,3), P3(3,9,2), P4(5,5,1), P5(6,3,4), P6(8,6,2)", 
                        id="case3", classes="menu-button")
            
            yield Button("4. Generar procesos aleatorios", id="random", classes="menu-button")
            
            yield Button("Volver", id="back-btn")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja clicks en botones"""
        if event.button.id == "case1":
            self.parent_app.processes = [
                Process("P1", 0, 8, 3),
                Process("P2", 1, 4, 1),
                Process("P3", 2, 9, 4),
                Process("P4", 3, 5, 2)
            ]
            self.parent_app.update_process_table()
            self.notify("✅ Conjunto 1 cargado (4 procesos)", severity="success")
            self.dismiss()
        
        elif event.button.id == "case2":
            self.parent_app.processes = [
                Process("P1", 0, 10, 2),
                Process("P2", 2, 3, 1),
                Process("P3", 4, 6, 3),
                Process("P4", 6, 1, 1),
                Process("P5", 8, 4, 2)
            ]
            self.parent_app.update_process_table()
            self.notify("✅ Conjunto 2 cargado (5 procesos)", severity="success")
            self.dismiss()
        
        elif event.button.id == "case3":
            self.parent_app.processes = [
                Process("P1", 0, 7, 1),
                Process("P2", 2, 4, 3),
                Process("P3", 3, 9, 2),
                Process("P4", 5, 5, 1),
                Process("P5", 6, 3, 4),
                Process("P6", 8, 6, 2)
            ]
            self.parent_app.update_process_table()
            self.notify("✅ Conjunto 3 cargado (6 procesos)", severity="success")
            self.dismiss()
        
        elif event.button.id == "random":
            self.app.push_screen(RandomProcessScreen(self.parent_app))
        
        elif event.button.id == "back-btn":
            self.dismiss()


class RandomProcessScreen(ModalScreen):
    """Pantalla modal para generar procesos aleatorios"""
    
    CSS = """
    Screen {
        align: center middle;
    }
    
    #dialog {
        width: 50;
        height: auto;
        padding: 2;
        border: solid $primary;
        background: $panel;
    }
    """
    
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
    
    def compose(self) -> ComposeResult:
        yield Container(
            Static("Generar procesos aleatorios", id="header-text"),
            Static("Número de procesos (4-10):", classes="metric-label"),
            Input(placeholder="6", id="count-input"),
            Horizontal(
                Button("Generar", id="generate-btn"),
                Button("Cancelar", id="cancel-btn")
            ),
            id="dialog"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja clicks en botones"""
        if event.button.id == "generate-btn":
            try:
                count = int(self.query_one("#count-input", Input).value or "6")
                if 4 <= count <= 10:
                    self.parent_app.processes = self.parent_app.process_generator.generate_random_processes(count)
                    self.parent_app.update_process_table()
                    self.notify(f"✅ {count} procesos aleatorios generados", severity="success")
                    self.dismiss()
                else:
                    self.notify("⚠️ El número debe estar entre 4 y 10", severity="warning")
            except ValueError:
                self.notify("❌ Valor inválido", severity="error")
        elif event.button.id == "cancel-btn":
            self.dismiss()


class RunSimulationScreen(Screen):
    """Pantalla para ejecutar simulación con un algoritmo"""
    
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        
        with Container():
            yield Static("EJECUTAR SIMULACIÓN", id="header-text")
            yield Static(f"Procesos cargados: {len(self.parent_app.processes)}", classes="metric-label")
            
            yield Static("Seleccione algoritmo:", classes="metric-label")
            
            for key, (name, _) in self.parent_app.schedulers.items():
                yield Button(f"{key}. {name}", id=f"algo-{key}", classes="menu-button")
            
            yield Button("Volver", id="back-btn")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja clicks en botones"""
        if event.button.id == "back-btn":
            self.dismiss()
        elif event.button.id.startswith("algo-"):
            algo_key = event.button.id.split("-")[1]
            self.run_simulation(algo_key)
    
    def run_simulation(self, algo_key: str):
        """Ejecuta la simulación con el algoritmo seleccionado"""
        if algo_key not in self.parent_app.schedulers:
            self.notify("❌ Algoritmo inválido", severity="error")
            return
        
        scheduler_name, scheduler = self.parent_app.schedulers[algo_key]
        
        # Configurar quantum para Round Robin
        if algo_key == "3":
            self.app.push_screen(QuantumConfigScreen(scheduler, self.parent_app, algo_key))
        else:
            self.execute_simulation(scheduler, scheduler_name)
    
    def execute_simulation(self, scheduler, scheduler_name):
        """Ejecuta la simulación"""
        import io
        from contextlib import redirect_stdout
        
        # Clonar procesos
        processes_copy = deepcopy(self.parent_app.processes)
        scheduler.processes = processes_copy
        
        # Ejecutar simulación (suprimiendo prints)
        with redirect_stdout(io.StringIO()):
            scheduler.run()
        
        # Calcular métricas
        metrics = scheduler.calculate_metrics()
        
        # Guardar en historial
        self.parent_app.results_display.save_to_history(scheduler, metrics)
        
        # Mostrar resultados
        self.app.push_screen(ResultsScreen(scheduler, metrics, scheduler_name))


class QuantumConfigScreen(ModalScreen):
    """Pantalla modal para configurar quantum de Round Robin"""
    
    CSS = """
    Screen {
        align: center middle;
    }
    
    #dialog {
        width: 50;
        height: auto;
        padding: 2;
        border: solid $primary;
        background: $panel;
    }
    """
    
    def __init__(self, scheduler, parent_app, algo_key):
        super().__init__()
        self.scheduler = scheduler
        self.parent_app = parent_app
        self.algo_key = algo_key
    
    def compose(self) -> ComposeResult:
        yield Container(
            Static("Configurar Round Robin", id="header-text"),
            Static(f"Quantum actual: {self.scheduler.quantum}", classes="metric-label"),
            Static("Nuevo quantum:", classes="metric-label"),
            Input(placeholder=str(self.scheduler.quantum), id="quantum-input"),
            Horizontal(
                Button("Aceptar", id="accept-btn"),
                Button("Cancelar", id="cancel-btn")
            ),
            id="dialog"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja clicks en botones"""
        if event.button.id == "accept-btn":
            try:
                quantum_str = self.query_one("#quantum-input", Input).value.strip()
                if quantum_str:
                    quantum = int(quantum_str)
                    if quantum > 0:
                        self.scheduler.set_quantum(quantum)
                        self.notify(f"✅ Quantum configurado a {quantum}", severity="success")
                    else:
                        self.notify("❌ Quantum debe ser > 0", severity="error")
                        return
            except ValueError:
                self.notify("❌ Valor inválido", severity="error")
                return
            
            self.dismiss()
            # Ejecutar simulación
            import io
            from contextlib import redirect_stdout
            
            processes_copy = deepcopy(self.parent_app.processes)
            self.scheduler.processes = processes_copy
            
            # Suprimir prints durante la ejecución
            with redirect_stdout(io.StringIO()):
                self.scheduler.run()
            
            metrics = self.scheduler.calculate_metrics()
            self.parent_app.results_display.save_to_history(self.scheduler, metrics)
            self.app.push_screen(ResultsScreen(self.scheduler, metrics, self.parent_app.schedulers[self.algo_key][0]))
        
        elif event.button.id == "cancel-btn":
            self.dismiss()


class ResultsScreen(Screen):
    """Pantalla para mostrar resultados de simulación"""
    
    CSS = """
    #results-container {
        padding: 1;
    }
    
    .metric-row {
        height: 1;
        margin: 1;
    }
    """
    
    def __init__(self, scheduler, metrics, scheduler_name):
        super().__init__()
        self.scheduler = scheduler
        self.metrics = metrics
        self.scheduler_name = scheduler_name
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        
        with ScrollableContainer(id="results-container"):
            yield Static(f"RESULTADOS DE LA SIMULACIÓN", id="header-text")
            yield Static(f"Algoritmo: {self.scheduler_name}", classes="metric-label")
            yield Static(f"Tiempo total: {self.scheduler.current_time}", classes="metric-label")
            yield Static(f"Procesos completados: {len(self.scheduler.completed_processes)}", classes="metric-label")
            
            yield Rule()
            yield Static("DIAGRAMA DE GANTT", classes="metric-label")
            yield Static(self.format_gantt(), id="gantt-display")
            
            yield Rule()
            yield Static("MÉTRICAS POR PROCESO", classes="metric-label")
            yield DataTable(id="per-process-table")
            
            yield Rule()
            yield Static("MÉTRICAS DEL SISTEMA", classes="metric-label")
            yield Static(self.format_system_metrics(), id="system-metrics")
            
            yield Button("Volver", id="back-btn")
    
    def on_mount(self) -> None:
        """Inicializa las tablas"""
        table = self.query_one("#per-process-table", DataTable)
        table.add_columns("PID", "Llegada", "Ráfaga", "Prioridad", "Fin", 
                         "Retorno", "Espera", "Respuesta")
        
        for proc in self.metrics["per_process"]:
            table.add_row(
                proc['pid'],
                str(proc['arrival_time']),
                str(proc['burst_time']),
                str(proc['priority']),
                str(proc['completion_time']),
                f"{proc['turnaround_time']:.2f}",
                f"{proc['waiting_time']:.2f}",
                f"{proc['response_time']:.2f}"
            )
    
    def format_gantt(self) -> str:
        """Formatea el diagrama de Gantt"""
        gantt = self.scheduler.get_gantt_chart()
        if not gantt:
            return "No hay datos para el diagrama de Gantt"
        
        # Línea superior
        line = "┌" + "─" * len(gantt) * 8 + "┐\n"
        
        # Línea de procesos
        line += "│"
        for item in gantt:
            spaces = 8 - len(item['process_id']) - 2
            left_spaces = spaces // 2
            right_spaces = spaces - left_spaces
            line += " " * left_spaces + item['process_id'] + " " * right_spaces
        line += "│\n"
        
        # Línea inferior
        line += "└" + "─" * len(gantt) * 8 + "┘\n"
        
        # Marcas de tiempo
        line += "0"
        current_time = 0
        for item in gantt:
            current_time += item['duration']
            spaces = 8 * (gantt.index(item) + 1) - len(str(current_time))
            line += " " * (spaces - 1) + str(current_time)
        
        return line
    
    def format_system_metrics(self) -> str:
        """Formatea las métricas del sistema"""
        system = self.metrics["system"]
        return (
            f"Tiempo Promedio de Retorno: {system['avg_turnaround']}\n"
            f"Tiempo Promedio de Espera:   {system['avg_waiting']}\n"
            f"Tiempo Promedio de Respuesta: {system['avg_response']}\n"
            f"Utilización de CPU:          {system['cpu_utilization']}%\n"
            f"Throughput:                  {system['throughput']} procesos/ut"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja clicks en botones"""
        if event.button.id == "back-btn":
            self.dismiss()


class CompareScreen(Screen):
    """Pantalla para comparar todos los algoritmos"""
    
    CSS = """
    #compare-container {
        padding: 2;
    }
    
    #quantum-input {
        width: 20;
        margin: 1;
    }
    
    #compare-btn {
        width: 30;
        margin: 1;
    }
    """
    
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        
        with Container(id="compare-container"):
            yield Static("COMPARAR TODOS LOS ALGORITMOS", id="header-text")
            yield Static(f"Procesos cargados: {len(self.parent_app.processes)}", classes="metric-label")
            
            yield Static("Configurar quantum para Round Robin (opcional, por defecto: 4):", classes="metric-label")
            with Horizontal():
                yield Input(placeholder="4", id="quantum-input")
                yield Button("Ejecutar comparativa", id="compare-btn", variant="primary")
            
            yield Static("", id="spacer")  # Espaciador
            
            yield Button("Volver", id="back-btn")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja clicks en botones"""
        if event.button.id == "compare-btn":
            self.run_comparison()
        elif event.button.id == "back-btn":
            self.dismiss()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Maneja cuando se presiona Enter en el campo de entrada"""
        if event.input.id == "quantum-input":
            self.run_comparison()
    
    def run_comparison(self):
        """Ejecuta la comparativa"""
        import io
        from contextlib import redirect_stdout
        
        # Configurar quantum
        try:
            quantum_str = self.query_one("#quantum-input", Input).value.strip()
            quantum = int(quantum_str) if quantum_str else 4
            if quantum <= 0:
                quantum = 4
        except ValueError:
            quantum = 4
        
        self.parent_app.schedulers["3"] = ("Round Robin", RoundRobin(quantum))
        
        results = []
        
        for key, (name, scheduler) in self.parent_app.schedulers.items():
            # Clonar procesos
            processes_copy = deepcopy(self.parent_app.processes)
            scheduler.processes = processes_copy
            
            # Ejecutar (suprimiendo prints)
            with redirect_stdout(io.StringIO()):
                scheduler.run()
            
            metrics = scheduler.calculate_metrics()
            
            results.append({
                "algorithm": name,
                "scheduler": scheduler,
                "metrics": metrics
            })
        
        # Mostrar comparativa
        self.app.push_screen(ComparisonResultsScreen(results))


class ComparisonResultsScreen(Screen):
    """Pantalla para mostrar resultados de comparativa"""
    
    def __init__(self, results):
        super().__init__()
        self.results = results
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        
        with ScrollableContainer():
            yield Static("COMPARATIVA DE ALGORITMOS", id="header-text")
            
            yield DataTable(id="comparison-table")
            
            yield Static(self.format_recommendation(), id="recommendation")
            
            yield Button("Volver", id="back-btn")
    
    def on_mount(self) -> None:
        """Inicializa la tabla de comparativa"""
        table = self.query_one("#comparison-table", DataTable)
        table.add_columns("Algoritmo", "T.Retorno Prom.", "T.Espera Prom.", 
                         "T.Respuesta Prom.", "CPU Util.", "Throughput")
        
        # Encontrar mejores valores
        best_turnaround = min(r['metrics']['system']['avg_turnaround'] for r in self.results)
        best_waiting = min(r['metrics']['system']['avg_waiting'] for r in self.results)
        best_response = min(r['metrics']['system']['avg_response'] for r in self.results)
        best_cpu = max(r['metrics']['system']['cpu_utilization'] for r in self.results)
        best_throughput = max(r['metrics']['system']['throughput'] for r in self.results)
        
        for result in self.results:
            metrics = result['metrics']['system']
            
            turn_arrow = "⭐" if metrics['avg_turnaround'] == best_turnaround else ""
            wait_arrow = "⭐" if metrics['avg_waiting'] == best_waiting else ""
            resp_arrow = "⭐" if metrics['avg_response'] == best_response else ""
            cpu_arrow = "⭐" if metrics['cpu_utilization'] == best_cpu else ""
            thr_arrow = "⭐" if metrics['throughput'] == best_throughput else ""
            
            table.add_row(
                result['algorithm'],
                f"{metrics['avg_turnaround']:.2f} {turn_arrow}",
                f"{metrics['avg_waiting']:.2f} {wait_arrow}",
                f"{metrics['avg_response']:.2f} {resp_arrow}",
                f"{metrics['cpu_utilization']:.1f}% {cpu_arrow}",
                f"{metrics['throughput']:.3f} {thr_arrow}"
            )
    
    def format_recommendation(self) -> str:
        """Formatea la recomendación"""
        # Encontrar el algoritmo con mejor promedio de ranking
        rankings = []
        
        for result in self.results:
            metrics = result['metrics']['system']
            ranking_score = 0
            
            # Para tiempos, menor es mejor
            for r in self.results:
                if metrics['avg_turnaround'] <= r['metrics']['system']['avg_turnaround']:
                    ranking_score += 1
            
            for r in self.results:
                if metrics['avg_waiting'] <= r['metrics']['system']['avg_waiting']:
                    ranking_score += 1
            
            for r in self.results:
                if metrics['avg_response'] <= r['metrics']['system']['avg_response']:
                    ranking_score += 1
            
            # Para CPU y throughput, mayor es mejor
            for r in self.results:
                if metrics['cpu_utilization'] >= r['metrics']['system']['cpu_utilization']:
                    ranking_score += 1
            
            for r in self.results:
                if metrics['throughput'] >= r['metrics']['system']['throughput']:
                    ranking_score += 1
            
            rankings.append((result['algorithm'], ranking_score))
        
        # Ordenar por mejor ranking
        rankings.sort(key=lambda x: x[1], reverse=True)
        
        text = f"\nMEJOR ALGORITMO PARA ESTE CASO: {rankings[0][0]}\n"
        text += "Ranking de algoritmos:\n"
        
        for algo, score in rankings:
            text += f"  {algo:<30} Puntuación: {score}/{(len(self.results)*5)}\n"
        
        return text
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja clicks en botones"""
        if event.button.id == "back-btn":
            self.dismiss()


class HistoryScreen(Screen):
    """Pantalla para ver historial de simulaciones"""
    
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        
        with Container():
            yield Static("HISTORIAL DE SIMULACIONES", id="header-text")
            yield DataTable(id="history-table")
            yield Button("Volver", id="back-btn")
    
    def on_mount(self) -> None:
        """Carga el historial"""
        try:
            with open(self.parent_app.results_display.history_file, 'r') as f:
                import json
                history = json.load(f)
        except:
            history = []
        
        if not history:
            self.notify("No hay simulaciones en el historial", severity="info")
            return
        
        table = self.query_one("#history-table", DataTable)
        table.add_columns("#", "Fecha/Hora", "Algoritmo", "Procesos", 
                         "Tiempo Total", "T.Retorno Prom.", "CPU Util.")
        
        for i, entry in enumerate(reversed(history[-10:]), 1):  # Últimas 10
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M")
            
            table.add_row(
                str(i),
                timestamp,
                entry['algorithm'],
                str(entry['process_count']),
                str(entry['total_time']),
                f"{entry['metrics']['system']['avg_turnaround']:.2f}",
                f"{entry['metrics']['system']['cpu_utilization']:.1f}%"
            )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja clicks en botones"""
        if event.button.id == "back-btn":
            self.dismiss()


class ConfigureScreen(Screen):
    """Pantalla para configurar parámetros"""
    
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        
        with Container():
            yield Static("CONFIGURAR PARÁMETROS", id="header-text")
            
            yield Static("Quantum por defecto para Round Robin:", classes="metric-label")
            with Horizontal():
                yield Input(placeholder=str(self.parent_app.default_quantum), id="quantum-input")
                yield Button("Guardar", id="save-quantum-btn")
            
            yield Static("Modo de prioridad por defecto:", classes="metric-label")
            with Horizontal():
                yield Button("Sin desalojo", id="non-preemptive-btn")
                yield Button("Con desalojo", id="preemptive-btn")
            
            yield Button("Volver", id="back-btn")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja clicks en botones"""
        if event.button.id == "save-quantum-btn":
            try:
                quantum = int(self.query_one("#quantum-input", Input).value or str(self.parent_app.default_quantum))
                if quantum > 0:
                    self.parent_app.default_quantum = quantum
                    self.parent_app.schedulers["3"] = ("Round Robin", RoundRobin(quantum))
                    self.notify(f"✅ Quantum configurado a {quantum}", severity="success")
                else:
                    self.notify("❌ Quantum debe ser > 0", severity="error")
            except ValueError:
                self.notify("❌ Valor inválido", severity="error")
        
        elif event.button.id == "non-preemptive-btn":
            self.parent_app.schedulers["4"] = ("Prioridades (sin desalojo)", PriorityScheduler(preemptive=False))
            self.notify("✅ Prioridad sin desalojo configurada", severity="success")
        
        elif event.button.id == "preemptive-btn":
            self.parent_app.schedulers["5"] = ("Prioridades (con desalojo)", PriorityScheduler(preemptive=True))
            self.notify("✅ Prioridad con desalojo configurada", severity="success")
        
        elif event.button.id == "back-btn":
            self.dismiss()

