"""
First Come First Served (FCFS) - Algoritmo de planificación
"""
from ..scheduler import Scheduler
from ..process import Process

class FCFS(Scheduler):
    """Implementación del algoritmo First Come First Served"""
    
    def __init__(self):
        super().__init__("First Come First Served (FCFS)")
    
    def run(self):
        """Ejecuta el algoritmo FCFS"""
        # Ordenar procesos por tiempo de llegada
        self.sort_by_arrival_time()
        
        self.current_time = 0
        self.completed_processes = []
        self.gantt_chart = []
        
        print(f"\n{'='*60}")
        print(f"Ejecutando {self.name}")
        print(f"{'='*60}")
        
        # Procesar cada proceso en orden de llegada
        for process in self.processes:
            # Si el proceso aún no ha llegado, esperar
            if self.current_time < process.arrival_time:
                self.current_time = process.arrival_time
            
            # Registrar inicio en diagrama de Gantt
            start_time = self.current_time
            
            # Ejecutar proceso completo (FCFS no es apropiativo)
            process.execute(process.burst_time, self.current_time)
            
            # Actualizar tiempo del sistema
            self.current_time += process.burst_time
            
            # Registrar fin en diagrama de Gantt
            self.update_gantt(process.pid, start_time, self.current_time)
            
            # Marcar proceso como completado
            process.completion_time = self.current_time
            process.calculate_waiting_time()
            self.completed_processes.append(process)
            
            print(f"  {process.pid}: Llegada={process.arrival_time}, "
                  f"Ejecución={process.burst_time}, "
                  f"Terminado en t={self.current_time}")
        
        print(f"{'='*60}")
        return self.completed_processes