"""
Cálculo de métricas de rendimiento
"""
class MetricsCalculator:
    """Calcula todas las métricas de rendimiento requeridas"""
    
    @staticmethod
    def calculate_all(processes):
        """Calcula todas las métricas obligatorias"""
        
        if not processes:
            return {}
        
        # Métricas por proceso
        per_process_metrics = []
        total_turnaround = 0
        total_waiting = 0
        total_response = 0
        
        for process in processes:
            turnaround = process.completion_time - process.arrival_time
            waiting = process.waiting_time
            response = process.response_time if process.response_time is not None else 0
            
            per_process_metrics.append({
                "pid": process.pid,
                "arrival_time": process.arrival_time,
                "burst_time": process.burst_time,
                "priority": process.priority,
                "completion_time": process.completion_time,
                "turnaround_time": turnaround,
                "waiting_time": waiting,
                "response_time": response
            })
            
            total_turnaround += turnaround
            total_waiting += waiting
            total_response += response
        
        n = len(processes)
        
        # Métricas del sistema
        avg_turnaround = total_turnaround / n if n > 0 else 0
        avg_waiting = total_waiting / n if n > 0 else 0
        avg_response = total_response / n if n > 0 else 0
        
        # Utilización de CPU
        total_burst_time = sum(p.burst_time for p in processes)
        max_completion_time = max(p.completion_time for p in processes) if processes else 0
        cpu_utilization = (total_burst_time / max_completion_time * 100) if max_completion_time > 0 else 0
        
        return {
            "per_process": per_process_metrics,
            "system": {
                "avg_turnaround": round(avg_turnaround, 2),
                "avg_waiting": round(avg_waiting, 2),
                "avg_response": round(avg_response, 2),
                "cpu_utilization": round(cpu_utilization, 2),
                "throughput": round(n / max_completion_time, 3) if max_completion_time > 0 else 0
            }
        }
    
    @staticmethod
    def print_metrics(metrics):
        """Imprime las métricas en formato legible"""
        if not metrics:
            print("No hay métricas para mostrar")
            return
        
        print("\n" + "="*80)
        print("METRICAS DE RENDIMIENTO")
        print("="*80)
        
        print("\n--- Métricas por Proceso ---")
        print(f"{'PID':<5} {'Llegada':<8} {'Ráfaga':<8} {'Prioridad':<10} "
              f"{'Fin':<8} {'Retorno':<10} {'Espera':<8} {'Respuesta':<10}")
        print("-"*80)
        
        for proc in metrics["per_process"]:
            print(f"{proc['pid']:<5} {proc['arrival_time']:<8} {proc['burst_time']:<8} "
                  f"{proc['priority']:<10} {proc['completion_time']:<8} "
                  f"{proc['turnaround_time']:<10.2f} {proc['waiting_time']:<8.2f} "
                  f"{proc['response_time']:<10.2f}")
        
        print("\n--- Métricas del Sistema ---")
        system = metrics["system"]
        print(f"Tiempo Promedio de Retorno: {system['avg_turnaround']}")
        print(f"Tiempo Promedio de Espera:   {system['avg_waiting']}")
        print(f"Tiempo Promedio de Respuesta: {system['avg_response']}")
        print(f"Utilización de CPU:          {system['cpu_utilization']}%")
        print(f"Throughput:                  {system['throughput']} procesos/ut")
        print("="*80)