CPU Process Scheduling simulator developed by Suprabhat Gurrala (February 2018)

Files:
engine.py   simulation engine code
cpu.py      application program for CPU process scheduling simulation
input.csv   input file to specify the processes to simulate

input.csv describes the processes to simulate.
It should have each process on a new line with name, number of cycles, and arrival time as values.

Cycles is the number of cycles the process needs to execute.
Arrival time is the number of nanoseconds after the start of the simulation that the process arrived.

Ex.

|Name       |Cycles     |Arrival Time|
--------------------------------------
|powershell |   500    |    0
|cmd        |   250    |    25
|system     |   1000   |    250


To run the program:

python cpu.py

This will run the simulation using all of the scheduling algorithms.

Use the following flags to run specific scheduling algorithms:
-f for First Come First Serve (FCFS)
-s for Shortest Job First (SJF)
-r for Round Robin (RR)

Example output:

python cpu.py -f

    Executing using First Come First Serve (FCFS) scheduling.
    Scheduled process powershell to run at t= 0
    Execeuted process powershell in 300.00 nanoseconds using 4500.00 nanowatts.
    Scheduled process cmd to run at t= 300.0
    Execeuted process cmd in 200.00 nanoseconds using 7500.00 nanowatts.
    Scheduled process system to run at t= 500.0
    Execeuted process system in 100.00 nanoseconds using 9000.00 nanowatts.
    Scheduled process chrome to run at t= 3000
    Execeuted process chrome in 100.00 nanoseconds using 10500.00 nanowatts.
    All processes executed in 3100.00 nanoseconds and consumed 10500.00 nanowatts.

    CPU was idle for: 2400.0 nanoseconds
    Total wait time: 200.0 nanoseconds