"""
Interfaz principal del simulador
Implementa la interfaz de usuario según especificaciones
"""
import sys
import os

# Configurar rutas para importaciones
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Agregar al path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Importaciones
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
    print("Verifique que tenga los archivos __init__.py en cada carpeta")
    input("Presiona Enter para salir...")
    sys.exit(1)

class CPUSchedulerInterface:
    """Interfaz principal del simulador de planificación de CPU"""
    
    def __init__(self):
        self.schedulers = {
            "1": ("FCFS (First Come First Served)", FCFS()),
            "2": ("SJF (Shortest Job First - No apropiativo)", SJF()),
            "3": ("Round Robin (Quantum configurable)", RoundRobin()),
            "4": ("Prioridades (sin desalojo)", PriorityScheduler(preemptive=False)),
            "5": ("Prioridades (con desalojo)", PriorityScheduler(preemptive=True))
        }
        self.processes = []
        self.file_handler = FileHandler()
        self.process_generator = ProcessGenerator()
        self.results_display = ResultsDisplay()
    
    def clear_screen(self):
        """Limpia la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_header(self):
        """Muestra el encabezado de la aplicación"""
        print("\n" + "="*70)
        print("SIMULADOR DE ALGORITMOS DE PLANIFICACIÓN DE CPU")
        print("Universidad Católica Andrés Bello - Sistemas Operativos")
        print("Equipo 7: Maria, Laura, Andrea")
        print("="*70)
    
    def main_menu(self):
        """Muestra el menú principal"""
        while True:
            self.clear_screen()
            self.show_header()
            
            print("\n" + "="*70)
            print("MENÚ PRINCIPAL")
            print("="*70)
            
            print("\n1. Cargar procesos desde archivo")
            print("2. Crear procesos manualmente")
            print("3. Usar casos de prueba predefinidos")
            print("4. Ejecutar simulación")
            print("5. Comparar todos los algoritmos")
            print("6. Ver historial de resultados")
            print("7. Configurar parámetros")
            print("8. Salir")
            
            print("\n" + "="*70)
            
            choice = input("\n👉 Seleccione una opción (1-8): ").strip()
            
            if choice == "1":
                self.load_from_file()
            elif choice == "2":
                self.create_manual_processes()
            elif choice == "3":
                self.use_test_cases()
            elif choice == "4":
                self.run_simulation()
            elif choice == "5":
                self.compare_algorithms()
            elif choice == "6":
                self.view_results_history()
            elif choice == "7":
                self.configure_parameters()
            elif choice == "8":
                print("\n¡Gracias por usar el simulador!")
                sys.exit(0)
            else:
                print("\nOpción inválida. Debe ser un número del 1 al 8.")
                input("Presione Enter para continuar...")
    
    def load_from_file(self):
        """Carga procesos desde archivo"""
        self.clear_screen()
        self.show_header()
        
        print("\n" + "="*70)
        print("CARGAR PROCESOS DESDE ARCHIVO")
        print("="*70)
        
        # Mostrar archivos disponibles en data/
        data_dir = "data"
        files = []
        if os.path.exists(data_dir):
            files = [f for f in os.listdir(data_dir) 
                    if f.endswith(('.json', '.txt', '.csv')) and f != "simulation_history.json"]
        
        if not files:
            print("\nNo hay archivos en la carpeta 'data'.")
            print("   Use la opción 3 (Casos de prueba) o")
            print("   ejecute 'crear_datos.py' para generar archivos.")
            input("\nPresione Enter para continuar...")
            return
        
        print("\nArchivos disponibles en 'data/':")
        for i, file in enumerate(files, 1):
            print(f"   {i}. {file}")
        
        print("\nPuede ingresar:")
        print("   - Número del archivo (ej: 1)")
        print("   - Nombre completo (ej: conjunto1.json)")
        
        choice = input("\n👉 Ingrese su selección: ").strip()
        
        # Si el usuario ingresó un número
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(files):
                filename = files[num - 1]
            else:
                print(f"\nNúmero fuera de rango (1-{len(files)})")
                input("Presione Enter para continuar...")
                return
        else:
            filename = choice
        
        # Si no tiene extensión, agregar .json por defecto
        if '.' not in filename:
            filename += '.json'
        
        try:
            self.processes = self.file_handler.load_processes(filename)
            print(f"\nCargados {len(self.processes)} procesos exitosamente.")
            
            # Mostrar procesos cargados
            print("\nProcesos cargados:")
            print("-"*60)
            print(f"{'PID':<5} {'Llegada':<8} {'Ráfaga':<8} {'Prioridad':<10}")
            print("-"*60)
            for p in self.processes:
                print(f"{p.pid:<5} {p.arrival_time:<8} {p.burst_time:<8} {p.priority:<10}")
            
            # Preguntar si ejecutar simulación inmediatamente
            run_now = input("\n¿Ejecutar simulación ahora? (s/n): ").strip().lower()
            if run_now == 's':
                self.run_simulation()
        
        except FileNotFoundError:
            print(f"\nArchivo no encontrado: {filename}")
            print("   Asegúrese de que el archivo esté en la carpeta 'data/'")
        except Exception as e:
            print(f"\nError al cargar archivo: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def use_test_cases(self):
        """Usa casos de prueba predefinidos"""
        self.clear_screen()
        self.show_header()
        
        print("\n" + "="*70)
        print("CASOS DE PRUEBA PREDEFINIDOS")
        print("="*70)
        
        print("\n1. Conjunto 1: Procesos Básicos (4 procesos)")
        print("   P1(0,8,3), P2(1,4,1), P3(2,9,4), P4(3,5,2)")
        
        print("\n2. Conjunto 2: Procesos Variados (5 procesos)")
        print("   P1(0,10,2), P2(2,3,1), P3(4,6,3), P4(6,1,1), P5(8,4,2)")
        
        print("\n3. Conjunto 3: Caso Personal (6 procesos)")
        print("   P1(0,7,1), P2(2,4,3), P3(3,9,2), P4(5,5,1), P5(6,3,4), P6(8,6,2)")
        
        print("\n4. Generar procesos aleatorios")
        
        choice = input("\n👉 Seleccione opción (1-4): ").strip()
        
        if choice == "1":
            self.processes = [
                Process("P1", 0, 8, 3),
                Process("P2", 1, 4, 1),
                Process("P3", 2, 9, 4),
                Process("P4", 3, 5, 2)
            ]
            print("\nConjunto 1 cargado (4 procesos)")
            
        elif choice == "2":
            self.processes = [
                Process("P1", 0, 10, 2),
                Process("P2", 2, 3, 1),
                Process("P3", 4, 6, 3),
                Process("P4", 6, 1, 1),
                Process("P5", 8, 4, 2)
            ]
            print("\nConjunto 2 cargado (5 procesos)")
            
        elif choice == "3":
            self.processes = [
                Process("P1", 0, 7, 1),
                Process("P2", 2, 4, 3),
                Process("P3", 3, 9, 2),
                Process("P4", 5, 5, 1),
                Process("P5", 6, 3, 4),
                Process("P6", 8, 6, 2)
            ]
            print("\nConjunto 3 cargado (6 procesos)")
            
        elif choice == "4":
            try:
                num_processes = int(input("Número de procesos a generar (4-10): "))
                if 4 <= num_processes <= 10:
                    self.processes = self.process_generator.generate_random_processes(num_processes)
                    print(f"\n{num_processes} procesos aleatorios generados")
                else:
                    print("Número debe estar entre 4 y 10. Generando 6 procesos.")
                    self.processes = self.process_generator.generate_random_processes(6)
            except ValueError:
                print("Valor inválido. Generando 6 procesos.")
                self.processes = self.process_generator.generate_random_processes(6)
        else:
            print("Opción inválida, usando Conjunto 1 por defecto")
            self.processes = [
                Process("P1", 0, 8, 3),
                Process("P2", 1, 4, 1),
                Process("P3", 2, 9, 4),
                Process("P4", 3, 5, 2)
            ]
        
        # Mostrar procesos cargados
        print("\nProcesos cargados:")
        self.show_processes()
        
        # Preguntar si ejecutar simulación inmediatamente
        run_now = input("\n¿Ejecutar simulación ahora? (s/n): ").strip().lower()
        if run_now == 's':
            self.run_simulation()
        else:
            input("\nPresione Enter para continuar...")
    
    def run_simulation(self):
        """Ejecuta simulación con algoritmo seleccionado"""
        if not self.processes:
            print("\n⚠️  No hay procesos cargados.")
            print("   Use opción 1, 2 o 3 para cargar procesos primero.")
            input("Presione Enter para continuar...")
            return
        
        self.clear_screen()
        self.show_header()
        
        print("\n" + "="*70)
        print("EJECUTAR SIMULACIÓN")
        print("="*70)
        
        print(f"\n📊 Procesos cargados: {len(self.processes)}")
        print("📋 Resumen:")
        for p in self.processes[:5]:
            print(f"   {p.pid}: Llegada={p.arrival_time}, Ráfaga={p.burst_time}, Prioridad={p.priority}")
        if len(self.processes) > 5:
            print(f"   ... y {len(self.processes)-5} más")
        
        print("\n" + "-"*70)
        print("📈 SELECCIONE ALGORITMO DE PLANIFICACIÓN:")
        print("-"*70)
        
        for key, (name, _) in self.schedulers.items():
            print(f"   {key}. {name}")
        
        print("\n" + "="*70)
        
        algo_choice = input("\n👉 Seleccione algoritmo (1-5): ").strip()
        
        if algo_choice not in self.schedulers:
            print("❌ Algoritmo inválido. Debe ser 1-5.")
            input("\nPresione Enter para continuar...")
            return
        
        scheduler_name, scheduler = self.schedulers[algo_choice]
        
        # Configurar parámetros específicos
        if algo_choice == "3":  # Round Robin
            print(f"\n⚙️  Configurar Round Robin")
            print(f"   Quantum actual: {scheduler.quantum}")
            try:
                new_quantum = input("   Nuevo quantum (Enter para mantener): ").strip()
                if new_quantum:
                    quantum = int(new_quantum)
                    if quantum > 0:
                        scheduler.set_quantum(quantum)
                        print(f"   ✅ Quantum configurado a {quantum}")
                    else:
                        print("   ❌ Quantum debe ser > 0. Manteniendo valor actual.")
            except ValueError:
                print("   ❌ Valor inválido. Manteniendo quantum actual.")
        
        print(f"\n🚀 Ejecutando {scheduler_name}...")
        print("="*70)
        
        # Clonar procesos
        from copy import deepcopy
        processes_copy = deepcopy(self.processes)
        scheduler.processes = processes_copy
        
        # Ejecutar simulación
        scheduler.run()
        
        # Calcular métricas
        metrics = scheduler.calculate_metrics()
        
        # Mostrar resultados
        self.results_display.show_results(scheduler, metrics)
        
        # Guardar en historial
        self.results_display.save_to_history(scheduler, metrics)
        
        input("\nPresione Enter para continuar...")
    
    def compare_algorithms(self):
        """Compara todos los algoritmos"""
        if not self.processes:
            print("\n⚠️  No hay procesos cargados.")
            input("Presione Enter para continuar...")
            return
        
        self.clear_screen()
        self.show_header()
        
        print("\n" + "="*70)
        print("COMPARAR TODOS LOS ALGORITMOS")
        print("="*70)
        
        print(f"\n📊 Procesos cargados: {len(self.processes)}")
        
        # Configurar Round Robin
        try:
            quantum = int(input("\nQuantum para Round Robin (predeterminado: 4): "))
            if quantum <= 0:
                quantum = 4
        except ValueError:
            quantum = 4
        
        self.schedulers["3"] = ("Round Robin", RoundRobin(quantum))
        
        results = []
        
        print("\n⚡ Ejecutando comparativa...")
        
        for key, (name, scheduler) in self.schedulers.items():
            print(f"\n  🔄 Ejecutando {name}...")
            
            # Clonar procesos
            from copy import deepcopy
            processes_copy = deepcopy(self.processes)
            scheduler.processes = processes_copy
            
            # Ejecutar
            scheduler.run()
            metrics = scheduler.calculate_metrics()
            
            results.append({
                "algorithm": name,
                "scheduler": scheduler,
                "metrics": metrics
            })
        
        # Mostrar comparativa
        self.results_display.show_comparison(results)
        
        input("\nPresione Enter para continuar...")
    
    def view_results_history(self):
        """Muestra historial de resultados"""
        self.results_display.show_history()
        input("\nPresione Enter para continuar...")
    
    def configure_parameters(self):
        """Configura parámetros del sistema"""
        self.clear_screen()
        self.show_header()
        
        print("\n" + "="*70)
        print("CONFIGURAR PARÁMETROS")
        print("="*70)
        
        print("\n1. Configurar quantum por defecto para Round Robin")
        print("2. Configurar modo de prioridad por defecto")
        print("3. Volver al menú principal")
        
        choice = input("\n👉 Seleccione opción (1-3): ").strip()
        
        if choice == "1":
            try:
                quantum = int(input("Nuevo quantum por defecto: "))
                if quantum > 0:
                    self.schedulers["3"] = ("Round Robin", RoundRobin(quantum))
                    print(f"✅ Quantum configurado a {quantum}")
                else:
                    print("❌ Quantum debe ser > 0")
            except ValueError:
                print("❌ Valor inválido")
        
        elif choice == "2":
            print("\nModo de prioridad:")
            print("1. Sin desalojo (default)")
            print("2. Con desalojo")
            mode = input("Seleccione modo (1-2): ").strip()
            
            if mode == "1":
                self.schedulers["4"] = ("Prioridades (sin desalojo)", PriorityScheduler(preemptive=False))
                print("✅ Prioridad sin desalojo configurada")
            elif mode == "2":
                self.schedulers["5"] = ("Prioridades (con desalojo)", PriorityScheduler(preemptive=True))
                print("✅ Prioridad con desalojo configurada")
            else:
                print("❌ Opción inválida")
        
        input("\nPresione Enter para continuar...")
    
    def show_processes(self):
        """Muestra todos los procesos cargados"""
        if not self.processes:
            print("No hay procesos cargados.")
            return
        
        print("\n" + "-"*60)
        print(f"{'PID':<5} {'Llegada':<8} {'Ráfaga':<8} {'Prioridad':<10} {'Estado':<12}")
        print("-"*60)
        
        for p in self.processes:
            print(f"{p.pid:<5} {p.arrival_time:<8} {p.burst_time:<8} {p.priority:<10} {p.state:<12}")
        
        print("-"*60)
    
    def create_manual_processes(self):
        """Crea procesos manualmente"""
        self.clear_screen()
        self.show_header()
        
        print("\n" + "="*70)
        print("CREAR PROCESOS MANUALMENTE")
        print("="*70)
        
        self.processes = []
        
        while True:
            print(f"\n📊 Procesos actuales: {len(self.processes)}")
            print("\n1. Agregar nuevo proceso")
            print("2. Editar proceso existente")
            print("3. Eliminar proceso")
            print("4. Ver todos los procesos")
            print("5. Finalizar creación")
            
            choice = input("\n👉 Seleccione opción (1-5): ").strip()
            
            if choice == "1":
                self.add_manual_process()
            elif choice == "2":
                self.edit_process()
            elif choice == "3":
                self.delete_process()
            elif choice == "4":
                self.show_processes()
            elif choice == "5":
                if len(self.processes) > 0:
                    save = input("\n¿Desea guardar estos procesos en un archivo? (s/n): ").lower()
                    if save == 's':
                        filename = input("Nombre del archivo: ").strip()
                        self.file_handler.save_processes(self.processes, filename)
                        print(f"✅ Procesos guardados en data/{filename}")
                break
            else:
                print("❌ Opción inválida")
    
    def add_manual_process(self):
        """Agrega un proceso manualmente"""
        print("\n--- AGREGAR NUEVO PROCESO ---")
        
        try:
            pid = input("ID del proceso (ej: P1): ").strip()
            arrival = int(input("Tiempo de llegada: "))
            burst = int(input("Tiempo de ráfaga (burst time): "))
            priority = int(input("Prioridad (número entero): "))
            
            process = Process(pid, arrival, burst, priority)
            self.processes.append(process)
            print(f"✅ Proceso {pid} agregado exitosamente.")
        
        except ValueError:
            print("❌ Error: Ingrese valores numéricos válidos.")
    
    def edit_process(self):
        """Edita un proceso existente"""
        self.show_processes()
        
        pid = input("\nID del proceso a editar: ").strip()
        
        process = next((p for p in self.processes if p.pid == pid), None)
        
        if not process:
            print(f"❌ Proceso {pid} no encontrado")
            return
        
        print(f"\nEditando proceso {pid}:")
        print(f"  Llegada actual: {process.arrival_time}")
        print(f"  Ráfaga actual: {process.burst_time}")
        print(f"  Prioridad actual: {process.priority}")
        
        try:
            new_arrival = input("Nuevo tiempo de llegada (Enter para mantener): ").strip()
            if new_arrival:
                process.arrival_time = int(new_arrival)
            
            new_burst = input("Nueva ráfaga (Enter para mantener): ").strip()
            if new_burst:
                process.burst_time = int(new_burst)
            
            new_priority = input("Nueva prioridad (Enter para mantener): ").strip()
            if new_priority:
                process.priority = int(new_priority)
            
            print(f"✅ Proceso {pid} actualizado")
        
        except ValueError:
            print("❌ Error: Ingrese valores numéricos válidos.")
    
    def delete_process(self):
        """Elimina un proceso"""
        self.show_processes()
        
        pid = input("\nID del proceso a eliminar: ").strip()
        
        process = next((p for p in self.processes if p.pid == pid), None)
        
        if not process:
            print(f"❌ Proceso {pid} no encontrado")
            return
        
        confirm = input(f"¿Está seguro de eliminar el proceso {pid}? (s/n): ").strip().lower()
        
        if confirm == 's':
            self.processes = [p for p in self.processes if p.pid != pid]
            print(f"✅ Proceso {pid} eliminado")