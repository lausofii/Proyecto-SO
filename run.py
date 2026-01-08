"""
Archivo alternativo para ejecutar el simulador
"""
import sys
import os

# Obtener ruta actual
current_dir = os.path.abspath(os.path.dirname(__file__))

# Agregar directorio actual al path
sys.path.insert(0, current_dir)

# Crear directorios necesarios
for folder in ["Core", "Core/algorithms", "UI", "Utils", "data"]:
    folder_path = os.path.join(current_dir, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        print(f"Creado directorio: {folder_path}")

# Crear archivos __init__.py si no existen
for folder in ["Core", "Core/algorithms", "UI", "Utils"]:
    init_file = os.path.join(current_dir, folder, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('"""Paquete Python"""\n')
        print(f"Creado: {init_file}")

print(f"Directorio de ejecución: {current_dir}")

# Intentar importar
try:
    print("\nCargando módulos...")
    from Core.scheduler import Scheduler
    from Core.process import Process
    from Core.metrics import MetricsCalculator
    from Core.algorithms.fcfs import FCFS
    from Core.algorithms.sjf import SJF
    from Core.algorithms.round_robin import RoundRobin
    from Core.algorithms.priority import PriorityScheduler
    from UI.interface import CPUSchedulerInterface
    
    print("TODOS LOS MÓDULOS CARGADOS!")
    
except ImportError as e:
    print(f"\nError de importación: {e}")
    input("\nPresiona Enter para salir...")
    sys.exit(1)

# Si todo va bien, ejecutar
print("\nINICIANDO SIMULADOR DE PLANIFICACIÓN DE CPU")
print("="*70)

try:
    app = CPUSchedulerInterface()
    app.main_menu()
    
except Exception as e:
    print(f"\n❌ Error durante la ejecución: {e}")
    import traceback
    traceback.print_exc()
    input("\nPresiona Enter para salir...")