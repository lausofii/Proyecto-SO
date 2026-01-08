"""
Muestra resultados de las simulaciones
"""
import json
import os
from datetime import datetime

class ResultsDisplay:
    """Clase para mostrar y gestionar resultados de simulaciones"""
    
    def __init__(self):
        self.history_file = "data/simulation_history.json"
        self.ensure_history_file()
    
    def ensure_history_file(self):
        """Asegura que el archivo de historial exista"""
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump([], f)
    
    def show_results(self, scheduler, metrics):
        """Muestra resultados de una simulación"""
        print("\n" + "="*80)
        print("RESULTADOS DE LA SIMULACIÓN")
        print("="*80)
        
        print(f"\nAlgoritmo: {scheduler.name}")
        print(f"Tiempo total de simulación: {scheduler.current_time}")
        print(f"Procesos completados: {len(scheduler.completed_processes)}")
        
        # Mostrar diagrama de Gantt
        print("\n--- DIAGRAMA DE GANTT ---")
        self.print_gantt_chart(scheduler.get_gantt_chart())
        
        # Mostrar métricas
        from Core.metrics import MetricsCalculator
        MetricsCalculator.print_metrics(metrics)
        
        # Mostrar recomendación
        self.show_recommendation(metrics)
    
    def print_gantt_chart(self, gantt_chart):
        """Imprime el diagrama de Gantt en formato texto"""
        if not gantt_chart:
            print("No hay datos para el diagrama de Gantt")
            return
        
        # Línea superior
        print("┌" + "─"*len(gantt_chart)*8 + "┐")
        
        # Línea de procesos
        print("│", end="")
        for item in gantt_chart:
            spaces = 8 - len(item['process_id']) - 2
            left_spaces = spaces // 2
            right_spaces = spaces - left_spaces
            print(" "*left_spaces + item['process_id'] + " "*right_spaces, end="")
        print("│")
        
        # Línea de tiempos
        print("└" + "─"*len(gantt_chart)*8 + "┘")
        
        # Marcas de tiempo
        print("0", end="")
        current_time = 0
        for item in gantt_chart:
            current_time += item['duration']
            spaces = 8 * (gantt_chart.index(item) + 1) - len(str(current_time))
            print(" "*(spaces-1) + str(current_time), end="")
        print()
    
    def show_comparison(self, results):
        """Muestra comparativa entre algoritmos"""
        print("\n" + "="*100)
        print("COMPARATIVA DE ALGORITMOS")
        print("="*100)
        
        # Encabezado de la tabla
        print(f"\n{'Algoritmo':<25} {'T.Retorno Prom.':<18} {'T.Espera Prom.':<18} "
              f"{'T.Respuesta Prom.':<18} {'CPU Util.':<12} {'Throughput':<12}")
        print("-"*100)
        
        # Encontrar mejores valores
        best_turnaround = min(r['metrics']['system']['avg_turnaround'] for r in results)
        best_waiting = min(r['metrics']['system']['avg_waiting'] for r in results)
        best_response = min(r['metrics']['system']['avg_response'] for r in results)
        best_cpu = max(r['metrics']['system']['cpu_utilization'] for r in results)
        best_throughput = max(r['metrics']['system']['throughput'] for r in results)
        
        # Mostrar cada algoritmo
        for result in results:
            metrics = result['metrics']['system']
            
            # Determinar si es el mejor en cada categoría
            turn_arrow = "" if metrics['avg_turnaround'] == best_turnaround else ""
            wait_arrow = "" if metrics['avg_waiting'] == best_waiting else ""
            resp_arrow = "" if metrics['avg_response'] == best_response else ""
            cpu_arrow = "" if metrics['cpu_utilization'] == best_cpu else ""
            thr_arrow = "" if metrics['throughput'] == best_throughput else ""
            
            print(f"{result['algorithm']:<25} "
                  f"{metrics['avg_turnaround']:<16.2f}{turn_arrow:<2} "
                  f"{metrics['avg_waiting']:<16.2f}{wait_arrow:<2} "
                  f"{metrics['avg_response']:<16.2f}{resp_arrow:<2} "
                  f"{metrics['cpu_utilization']:<10.1f}%{cpu_arrow:<2} "
                  f"{metrics['throughput']:<10.3f}{thr_arrow:<2}")
        
        print("-"*100)
        
        # Mostrar recomendación general
        self.show_overall_recommendation(results)
    
    def show_recommendation(self, metrics):
        """Muestra recomendación basada en métricas"""
        print("\n--- RECOMENDACIÓN ---")
        
        system = metrics['system']
        
        if system['avg_waiting'] < 10:
            print("Este algoritmo muestra buen rendimiento con baja espera.")
        elif system['avg_waiting'] < 20:
            print("Rendimiento aceptable, pero podría optimizarse.")
        else:
            print("Alto tiempo de espera, considere otro algoritmo.")
        
        if system['cpu_utilization'] > 80:
            print("Excelente utilización de CPU (>80%).")
        elif system['cpu_utilization'] > 60:
            print("Utilización de CPU moderada.")
        else:
            print("Baja utilización de CPU, considere optimizar.")
    
    def show_overall_recommendation(self, results):
        """Muestra recomendación general basada en comparativa"""
        print("\n--- RECOMENDACIÓN GENERAL ---")
        
        # Encontrar el algoritmo con mejor promedio de ranking
        rankings = []
        
        for result in results:
            metrics = result['metrics']['system']
            ranking_score = 0
            
            # Para tiempos, menor es mejor
            for r in results:
                if metrics['avg_turnaround'] <= r['metrics']['system']['avg_turnaround']:
                    ranking_score += 1
            
            for r in results:
                if metrics['avg_waiting'] <= r['metrics']['system']['avg_waiting']:
                    ranking_score += 1
            
            for r in results:
                if metrics['avg_response'] <= r['metrics']['system']['avg_response']:
                    ranking_score += 1
            
            # Para CPU y throughput, mayor es mejor
            for r in results:
                if metrics['cpu_utilization'] >= r['metrics']['system']['cpu_utilization']:
                    ranking_score += 1
            
            for r in results:
                if metrics['throughput'] >= r['metrics']['system']['throughput']:
                    ranking_score += 1
            
            rankings.append((result['algorithm'], ranking_score))
        
        # Ordenar por mejor ranking
        rankings.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\nMEJOR ALGORITMO PARA ESTE CASO: {rankings[0][0]}")
        print("Ranking de algoritmos:")
        
        for algo, score in rankings:
            print(f"  {algo:<30} Puntuación: {score}/{(len(results)*5)}")
    
    def save_to_history(self, scheduler, metrics):
        """Guarda resultados en el historial"""
        try:
            with open(self.history_file, 'r') as f:
                history = json.load(f)
        except:
            history = []
        
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "algorithm": scheduler.name,
            "process_count": len(scheduler.completed_processes),
            "total_time": scheduler.current_time,
            "metrics": metrics,
            "gantt_chart": scheduler.get_gantt_chart()
        }
        
        history.append(history_entry)
        
        # Mantener solo las últimas 50 simulaciones
        if len(history) > 50:
            history = history[-50:]
        
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def show_history(self):
        """Muestra historial de simulaciones"""
        try:
            with open(self.history_file, 'r') as f:
                history = json.load(f)
        except:
            print("No hay historial de simulaciones.")
            return
        
        if not history:
            print("No hay simulaciones en el historial.")
            return
        
        print("\n" + "="*100)
        print("HISTORIAL DE SIMULACIONES")
        print("="*100)
        
        for i, entry in enumerate(reversed(history[-10:]), 1):  # Mostrar últimas 10
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M")
            
            print(f"\n{i}. {timestamp} - {entry['algorithm']}")
            print(f"   Procesos: {entry['process_count']} | "
                  f"Tiempo total: {entry['total_time']} | "
                  f"T.Retorno Prom: {entry['metrics']['system']['avg_turnaround']} | "
                  f"CPU Util: {entry['metrics']['system']['cpu_utilization']}%")
        
        print("\n" + "="*100)