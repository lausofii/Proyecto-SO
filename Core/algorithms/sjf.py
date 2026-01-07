"""
Shortest Job First (SJF) - Algoritmo de planificación NO apropiativo
"""
from ..scheduler import Scheduler
from ..process import Process

class SJF(Scheduler):
    """Implementación del algoritmo Shortest Job First (no apropiativo)"""
    
    def __init__(self):
        super().__init__("Shortest Job First (SJF) - No apropiativo")
    
    def run(self):
        """Ejecuta el algoritmo SJF (no apropiativo)"""
        # Ordenar procesos por tiempo de llegada inicialmente
        self.sort_by_arrival_time()
        
        self.current_time = 0
        self.completed_processes = []
        self.gantt_chart = []
        n = len(self.processes)
        completed = 0
        
        # Estados de los procesos
        for p in self.processes:
            p.remaining_time = p.burst_time
        
        print(f"\n{'='*60}")
        print(f"Ejecutando {self.name}")
        print(f"{'='*60}")
        
        while completed < n:
            # Encontrar procesos que han llegado y no han terminado
            ready_processes = [
                p for p in self.processes 
                if not p.is_completed() and p.arrival_time <= self.current_time
            ]
            
            if ready_processes:
                # Seleccionar proceso con menor ráfaga (burst time)
                ready_processes.sort(key=lambda p: p.burst_time)
                current_process = ready_processes[0]
                
                start_time = self.current_time
                
                # Ejecutar proceso completo (no apropiativo)
                current_process.execute(current_process.burst_time, self.current_time)
                
                self.current_time += current_process.burst_time
                self.update_gantt(current_process.pid, start_time, self.current_time)
                
                current_process.completion_time = self.current_time
                current_process.calculate_waiting_time()
                self.completed_processes.append(current_process)
                completed += 1
                
                print(f"  {current_process.pid}: Ráfaga={current_process.burst_time}, "
                      f"Terminado en t={self.current_time}")
            else:
                # No hay procesos listos, avanzar tiempo
                self.current_time += 1
        
        print(f"{'='*60}")
        return self.completed_processes