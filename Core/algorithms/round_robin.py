"""
Round Robin - Algoritmo de planificación con quantum configurable
"""
from collections import deque
from ..scheduler import Scheduler
from ..process import Process

class RoundRobin(Scheduler):
    """Implementación del algoritmo Round Robin con quantum configurable"""
    
    def __init__(self, quantum=4):
        super().__init__(f"Round Robin (Quantum={quantum})")
        self.quantum = quantum
    
    def set_quantum(self, quantum):
        """Configura el quantum del algoritmo"""
        self.quantum = quantum
        self.name = f"Round Robin (Quantum={quantum})"
    
    def run(self):
        """Ejecuta el algoritmo Round Robin"""
        # Ordenar por tiempo de llegada
        self.sort_by_arrival_time()
        
        self.current_time = 0
        self.completed_processes = []
        self.gantt_chart = []
        
        # Cola de procesos listos
        ready_queue = deque()
        
        # Diccionario para tiempos restantes
        remaining_time = {p.pid: p.burst_time for p in self.processes}
        
        # Índice para recorrer procesos por llegada
        process_index = 0
        n = len(self.processes)
        
        print(f"\n{'='*60}")
        print(f"Ejecutando {self.name}")
        print(f"{'='*60}")
        
        while len(self.completed_processes) < n:
            # Agregar procesos que han llegado a la cola
            while (process_index < n and 
                   self.processes[process_index].arrival_time <= self.current_time):
                p = self.processes[process_index]
                if remaining_time[p.pid] > 0:
                    ready_queue.append(p)
                process_index += 1
            
            if ready_queue:
                current_process = ready_queue.popleft()
                pid = current_process.pid
                
                # Registrar tiempo de respuesta (primera ejecución)
                if current_process.start_time is None:
                    current_process.start_time = self.current_time
                    current_process.response_time = self.current_time - current_process.arrival_time
                
                # Ejecutar por quantum o hasta terminar
                execution_time = min(self.quantum, remaining_time[pid])
                start_time = self.current_time
                
                # Actualizar proceso
                current_process.execute(execution_time, self.current_time)
                
                self.current_time += execution_time
                remaining_time[pid] -= execution_time
                
                # Actualizar diagrama de Gantt
                self.update_gantt(pid, start_time, self.current_time)
                
                print(f"  {pid}: Ejecutó {execution_time}u (Restante: {remaining_time[pid]}u)")
                
                # Agregar procesos que llegaron durante la ejecución
                while (process_index < n and 
                       self.processes[process_index].arrival_time <= self.current_time):
                    p = self.processes[process_index]
                    if remaining_time[p.pid] > 0:
                        ready_queue.append(p)
                    process_index += 1
                
                # Si el proceso no terminó, volver a la cola
                if remaining_time[pid] > 0:
                    ready_queue.append(current_process)
                else:
                    # Proceso terminado
                    current_process.completion_time = self.current_time
                    current_process.calculate_waiting_time()
                    self.completed_processes.append(current_process)
            else:
                # No hay procesos en cola, avanzar tiempo
                self.current_time += 1
        
        print(f"{'='*60}")
        return self.completed_processes