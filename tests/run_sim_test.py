from Core.algorithms.fcfs import FCFS
from Core.process import Process
from copy import deepcopy
import json

p=[Process('P1',0,5,1),Process('P2',1,3,1)]
s=FCFS()
s.processes=p
s.run()
print('completed:', [proc.pid for proc in s.completed_processes])
print('gantt:', s.get_gantt_chart())
metrics = s.calculate_metrics()
print('metrics keys:', list(metrics.keys()))
print(json.dumps(metrics, indent=2))
