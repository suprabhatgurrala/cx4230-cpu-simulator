import csv
import sys

import engine

INPUT_FILE = "input.csv"
CLOCK_SPEED = 3  # gigahertz
POWER_CONSUMPTION = 15  # watts


def read_input_file():
    """
    Reads the input file and populates the processes.
    :return: A list of the processes
    """
    input_list = []

    with open(INPUT_FILE) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) != 3:
                print("Row is missing values.")
                continue
            name = row[0]
            try:
                cycles = int(row[1])
                arrival_time = int(row[2])
            except ValueError:
                print("Unable to parse row.")
                continue
            input_list.append((name, cycles, arrival_time))

    # input_list.sort(key=lambda process: process[2])
    return input_list


class CPU:
    def __init__(self, clock_speed):
        self.clock_speed = clock_speed
        self.free = True
        self.current_time = 0
        self.execution_time = 0
        self.power_consumption = 0

    def to_string(self):
        return str(self.clock_speed) + " GHz CPU object"

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()


def get_fcfs_priority(fel, process):
    return 1


def get_sjf_priority(fel, process):
    return process[1]


def get_rr_priority(fel, process):
    return 1


def fcfs_handler(params):
    """
    Handles arrivals of processes and schedules them to be executed on the CPU using the FCFS algorithm.
    :param params: the parameters passed into the handler
    """
    fel = params[0]
    cpu = params[1]
    name, cycles_rem, arrival_time = params[2]

    if cpu.free:
        cpu.free = False

        execute_time = cycles_rem / cpu.clock_speed
        cpu.execution_time += execute_time
        cpu.power_consumption += execute_time * POWER_CONSUMPTION

        cpu.current_time += execute_time




def process_handler(params):
    cpu = params[0]
    name, cycles_rem = params[1]

    cpu.free = False
    execute_time = cycles_rem / cpu.clock_speed
    cpu.execution_time += execute_time
    cpu.power_consumption += execute_time * POWER_CONSUMPTION

    print("Execeuted process", name, "in", "{0:.2f}".format(execute_time), "nanoseconds using", "{0:.2f}".format(cpu.power_consumption), "nanowatts.")


def main_loop(processes, priority_generator):
    fel = engine.FEL()
    cpu = CPU(CLOCK_SPEED)


    for process in processes:
        priority = priority_generator(fel, process)
        event_data = cpu, process
        event_handler = process_handler
        fel.schedule(engine.Event(event_data, event_handler), priority)

    engine.run_sim(fel)
    print("All processes executed in", "{0:.2f}".format(cpu.execution_time), "nanoseconds and consumed", "{0:.2f}".format(cpu.power_consumption),
          "nanowatts.\n")


def main():
    processes = read_input_file()

    fcfs = False
    sjf = False
    rr = False

    if len(sys.argv) == 1:
        fcfs = True
        sjf = True
        rr = True
    elif len(sys.argv) == 2:
        if sys.argv[1] == "-f":
            fcfs = True
        elif sys.argv[1] == "-s":
            sjf = True
        elif sys.argv[1] == "-r":
            rr = True
        else:
            "Invalid argument. Args must be -f, -s, or -r"
    else:
        "Too many arguments. Args must be -f, -s, or -r if provided."

    if fcfs:
        print("Executing using First Come First Serve (FCFS) scheduling.")
        main_loop(processes, get_fcfs_priority)
    # if sjf:
    #     print("Executing using Shortest Job First (SJF) scheduling.")
    #     main_loop(processes, get_sjf_priority)
    # if rr:
    #     print("Executing using Round Robin (RR) scheduling.")
    #     main_loop(processes, get_rr_priority)


main()
