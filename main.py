"""
Punto de entrada principal del simulador de planificación de CPU
Usa Textual para la interfaz gráfica de terminal
"""
import sys
import os

# Configurar rutas para importaciones
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Agregar rutas necesarias
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "Core"))
sys.path.insert(0, os.path.join(BASE_DIR, "UI"))
sys.path.insert(0, os.path.join(BASE_DIR, "Utils"))

# Verificar que existan los directorios necesarios
required_dirs = ["Core", "UI", "Utils", "data"]
for dir_name in required_dirs:
    dir_path = os.path.join(BASE_DIR, dir_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

# Verificar archivos __init__.py
for dir_name in ["Core", "UI", "Utils", "Core/algorithms"]:
    init_file = os.path.join(BASE_DIR, dir_name, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('"""Paquete Python"""\n')

# Intentar importar
try:
    from UI.textual_interface import CPUSchedulerApp
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("\n📦 Asegúrese de instalar las dependencias:")
    print("   pip install -r requirements.txt")
    print("\n📁 Verificando estructura de archivos...")
    
    # Listar archivos .py
    for root, dirs, files in os.walk(BASE_DIR):
        level = root.replace(BASE_DIR, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if file.endswith('.py'):
                print(f'{subindent}{file}')
    
    input("\nPresiona Enter para salir...")
    sys.exit(1)

def main():
    """Función principal"""
    try:
        # Crear directorios necesarios
        os.makedirs("data", exist_ok=True)
        
        # Guardar referencias originales de stdout/stderr antes de que Textual los capture
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        # Iniciar aplicación Textual
        app = CPUSchedulerApp()
        # Restaurar stdout/stderr originales para logging
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        app.run()
        
    except KeyboardInterrupt:
        print("\n\nSimulador terminado por el usuario.", file=sys.__stdout__)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.__stderr__)
        import traceback
        traceback.print_exc(file=sys.__stderr__)
        input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()