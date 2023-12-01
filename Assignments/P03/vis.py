import pandas as pd
import matplotlib.pyplot as plt


df_io = pd.read_csv('RR_timeslice=5_cpu=4_io=4_io_int.csv')
df_cpu = pd.read_csv('RR_timeslice=5_cpu=4_io=4_cpu_int.csv')
df_hi_pri = pd.read_csv('RR_timeslice=5_cpu=4_io=4_prio_high.csv')

# df_io = pd.read_csv('FCFS_timeslice=5_cpu=4_io=4_io_int.csv')
# df_cpu = pd.read_csv('FCFS_timeslice=5_cpu=4_io=4_cpu_int.csv')
# df_hi_pri = pd.read_csv('FCFS_timeslice=5_cpu=4_io=4_prio_high.csv')

# df_io = pd.read_csv('PB_timeslice=5_cpu=4_io=4_io_int.csv')
# df_cpu = pd.read_csv('PB_timeslice=5_cpu=4_io=4_cpu_int.csv')
# df_hi_pri = pd.read_csv('PB_timeslice=5_cpu=4_io=4_prio_high.csv')

arrival_io = df_io['arrival_time']
arrival_cpu = df_cpu['arrival_time']
arrival_hi_pri = df_hi_pri['arrival_time']

id_io = df_io['process_id']
id_cpu  = df_cpu['process_id']
id_hi_pri = df_hi_pri['process_id']

tat_io = df_io['turnaround_time']
tat_cpu = df_cpu['turnaround_time']
tat_hi_pri = df_hi_pri['turnaround_time']

io_wait_io = df_io['io_time'] + df_io['wait_time']
io_wait_cpu = df_cpu['io_time'] + df_cpu['wait_time']
io_wait_hi_pri = df_hi_pri['io_time'] + df_hi_pri['wait_time']

ready_io = df_io['ready_time']
ready_cpu = df_cpu['ready_time']
ready_hi_pri = df_hi_pri['ready_time']

exit_io = df_io['exit_time']
exit_cpu = df_cpu['exit_time']
exit_hi_pri = df_hi_pri['exit_time']


fig, (ax1, ax2, ax3) = plt.subplots(3,1,figsize=(10,6))

ax1.plot(id_io,tat_io, label='io_intensive',marker = 'o')
ax2.plot(id_cpu,tat_cpu, label='cpu_intensive',marker = 'x')
ax3.plot(id_hi_pri,tat_hi_pri, label='high_priority',marker = 's')

# ax1.plot(id_io,io_wait_io, label='io_intensive',marker = 'o')
# ax2.plot(id_cpu, io_wait_cpu, label='cpu_intensive',marker = 'x')
# ax3.plot(id_hi_pri,io_wait_hi_pri, label='high_priority',marker = 's')

# ax1.plot(id_io,ready_io, label='io_intensive',marker = 'o')
# ax2.plot(id_cpu,ready_cpu, label='cpu_intensive',marker = 'x')
# ax3.plot(id_hi_pri,ready_hi_pri, label='high_priority',marker = 's')

# ax1.plot(id_io,exit_io, label='io_intensive',marker = 'o')
# ax2.plot(id_cpu,exit_cpu, label='cpu_intensive',marker = 'x')
# ax3.plot(id_hi_pri,exit_hi_pri, label='high_priority',marker = 's')

fig.suptitle('Round Robin Scheduler')
# fig.suptitle('First Come First Serve Scheduler')
# fig.suptitle('Priority Based Scheduler')

fig.supxlabel('Process ID')
# fig.supxlabel('Arrival Time')

fig.supylabel('Turnaround Time')
# fig.supylabel('IO/WAIT Time')
# fig.supylabel('Ready Time')
# fig.supylabel('Exit Time')
fig.legend()

plt.show()
