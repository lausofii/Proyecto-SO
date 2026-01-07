"""
Priority Scheduling - Algoritmo de planificación por prioridades
"""
from ..scheduler import Scheduler
from ..process import Process

class PriorityScheduler(Scheduler):
    """Implementación de planificación por prioridades (con y sin desalojo)"""
    
    def __init__(self, preemptive=False):
        mode = "con desalojo" if preemptive else "sin desalojo"
        super().__init__(f"Priority Scheduling ({mode})")
        self.preemptive = preemptive
    
    def run(self):
        """Ejecuta el algoritmo de prioridades"""
        if self.preemptive:
            return self._run_preemptive()
        else:
            return self._run_non_preemptive()
    
    def _run_non_preemptive(self):
        """Versión sin desalojo"""
        self.sort_by_arrival_time()
        
        self.current_time = 0
        self.completed_processes = []
        self.gantt_chart = []
        n = len(self.processes)
        completed = 0
        
        print(f"\n{'='*60}")
        print(f"Ejecutando {self.name}")
        print(f"{'='*60}")
        
        while completed < n:
            # Procesos que han llegado y no han terminado
            ready_processes = [
                p for p in self.processes 
                if not p.is_completed() and p.arrival_time <= self.current_time
            ]
            
            if ready_processes:
                # Seleccionar proceso con mayor prioridad (número menor = mayor prioridad)
                ready_processes.sort(key=lambda p: (p.priority, p.arrival_time))
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
                
                print(f"  {current_process.pid}: Prioridad={current_process.priority}, "
                      f"Terminado en t={self.current_time}")
            else:
                self.current_time += 1
        
        print(f"{'='*60}")
        return self.completed_processes
    
    def _run_preemptive(self):
        """Versión con desalojo"""
        from collections import deque
        
        self.sort_by_arrival_time()
        
        self.current_time = 0
        self.completed_processes = []
        self.gantt_chart = []
        
        ready_queue = []
        remaining_time = {p.pid: p.burst_time for p in self.processes}
        process_index = 0
        n = len(self.processes)
        
        print(f"\n{'='*60}")
        print(f"Ejecutando {self.name}")
        print(f"{'='*60}")
        
        current_process = None
        current_start_time = 0
        
        while len(self.completed_processes) < n:
            # Agregar nuevos procesos que han llegado
            while (process_index < n and 
                   self.processes[process_index].arrival_time <= self.current_time):
                p = self.processes[process_index]
                if remaining_time[p.pid] > 0:
                    ready_queue.append(p)
                    # Ordenar por prioridad (menor número = mayor prioridad)
                    ready_queue.sort(key=lambda x: (x.priority, x.arrival_time))
                process_index += 1
            
            # Si hay un proceso ejecutando, verificar si debe ser desalojado
            if current_process and ready_queue:
                next_process = ready_queue[0]
                if (next_process.priority < current_process.priority and 
                    remaining_time[current_process.pid] > 0):
                    # Desalojar proceso actual
                    execution_time = self.current_time - current_start_time
                    if execution_time > 0:
                        current_process.execute(execution_time, current_start_time)
                        self.update_gantt(current_process.pid, current_start_time, self.current_time)
                        print(f"  {current_process.pid}: Desalojado después de {execution_time}u")
                    
                    # Volver a poner en cola el proceso desalojado
                    if remaining_time[current_process.pid] > 0:
                        ready_queue.append(current_process)
                        ready_queue.sort(key=lambda x: (x.priority, x.arrival_time))
                    
                    # Tomar nuevo proceso
                    current_process = ready_queue.pop(0)
                    current_start_time = self.current_time
                    
                    if current_process.start_time is None:
                        current_process.start_time = self.current_time
                        current_process.response_time = self.current_time - current_process.arrival_time
            
            # Si no hay proceso ejecutando, tomar uno de la cola
            if not current_process and ready_queue:
                current_process = ready_queue.pop(0)
                current_start_time = self.current_time
                
                if current_process.start_time is None:
                    current_process.start_time = self.current_time
                    current_process.response_time = self.current_time - current_process.arrival_time
            
            # Ejecutar proceso actual por 1 unidad de tiempo
            if current_process:
                self.current_time += 1
                remaining_time[current_process.pid] -= 1
                
                if remaining_time[current_process.pid] == 0:
                    # Proceso terminado
                    execution_time = self.current_time - current_start_time
                    if execution_time > 0:
                        current_process.execute(execution_time, current_start_time)
                        self.update_gantt(current_process.pid, current_start_time, self.current_time)
                    
                    current_process.completion_time = self.current_time
                    current_process.calculate_waiting_time()
                    self.completed_processes.append(current_process)
                    
                    print(f"  {current_process.pid}: Terminado en t={self.current_time}")
                    
                    current_process = None
                    current_start_time = self.current_time
            else:
                # No hay procesos listos, avanzar tiempo
                self.current_time += 1
        
        print(f"{'='*60}")
        return self.completed_processes