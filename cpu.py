import csv
import sys

import engine

INPUT_FILE = "input.csv"
CLOCK_SPEED = 1  # gigahertz
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

    return input_list


class CPU:
    def __init__(self, clock_speed):
        self.clock_speed = clock_speed
        self.free = True
        self.idle_time = 0
        self.available_time = 0
        self.execution_time = 0
        self.power_consumption = 0
        self.num_processes = 0
        self.total_wait_time = 0

    def to_string(self):
        return str(self.clock_speed) + " GHz CPU object"

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()


def fcfs_handler(params):
    """
    Handles arrivals of processes and schedules them to be executed on the CPU using the FCFS algorithm.
    :param params: the parameters passed into the handler
    """
    fel = params[0]
    cpu = params[1]
    process = params[2]
    name, cycles_rem, arrival_time = process

    event_data = cpu, process
    timestamp = max(cpu.available_time, arrival_time)
    if arrival_time > cpu.available_time:
        cpu.idle_time += arrival_time - cpu.available_time
    elif arrival_time < cpu.available_time:
        cpu.total_wait_time += cpu.available_time - arrival_time
    print("Scheduled process", name, "to run at t=", timestamp)
    fel.schedule(engine.Event(event_data, process_handler), timestamp)
    cpu.available_time += cycles_rem / cpu.clock_speed

def sjf_handler(params):
    """
    Handles arrivals of processes and schedules them to be executed on the CPU using the SJF algorithm.
    :param params: the parameters passed into the handler
    """
    fel = params[0]
    cpu = params[1]
    process = params[2]
    name, cycles_rem, arrival_time = process

    event_data = cpu, process
    timestamp = max(cpu.available_time, arrival_time)
    if arrival_time > cpu.available_time:
        cpu.idle_time += arrival_time - cpu.available_time
    elif arrival_time < cpu.available_time:
        cpu.total_wait_time += cpu.available_time - arrival_time
    print("Scheduled process", name, "to run at t=", timestamp)
    fel.schedule(engine.Event(event_data, process_handler), timestamp)
    cpu.available_time += cycles_rem / cpu.clock_speed


def rr_handler(params):
    """
    Handles arrivals of processes and schedules them to be executed on the CPU using the RR algorithm.
    :param params: the parameters passed into the handler
    """
    fel = params[0]
    cpu = params[1]
    process = params[2]
    name, cycles_rem, arrival_time = process

    event_data = cpu, process
    timestamp = max(cpu.available_time, arrival_time)
    if arrival_time > cpu.available_time:
        cpu.idle_time += arrival_time - cpu.available_time
    elif arrival_time < cpu.available_time:
        cpu.total_wait_time += cpu.available_time - arrival_time
    # print("Scheduled process", name, "to run at t=", timestamp)
    fel.schedule(engine.Event(event_data, process_handler), timestamp)
    cpu.available_time += cycles_rem / cpu.clock_speed


def process_handler(params):
    cpu = params[0]
    name, cycles_rem, arrival_time = params[1]

    cpu.free = False
    execute_time = cycles_rem / cpu.clock_speed
    cpu.execution_time += execute_time
    cpu.power_consumption += execute_time * POWER_CONSUMPTION
    cpu.num_processes -= 1

    print("Execeuted process", name, "in", "{0:.2f}".format(execute_time), "nanoseconds using", "{0:.2f}".format(cpu.power_consumption), "nanowatts.")


def fcfs_loop(processes):
    fel = engine.FEL()
    cpu = CPU(CLOCK_SPEED)

    for process in processes:
        name, cycles, arrival_time = process
        event_data = fel, cpu, process
        event_handler = fcfs_handler
        fel.schedule(engine.Event(event_data, event_handler), arrival_time)

    engine.run_sim(fel)
    print("All processes executed in", "{0:.2f}".format(cpu.execution_time + cpu.idle_time), "nanoseconds and consumed",
          "{0:.2f}".format(cpu.power_consumption),
          "nanowatts.\n")
    print("CPU was idle for:", cpu.idle_time, "nanoseconds")
    print("Total wait time:", cpu.total_wait_time, "nanoseconds")


def sjf_loop(processes):
    fel = engine.FEL()
    cpu = CPU(CLOCK_SPEED)

    for process in processes:
        name, cycles, arrival_time = process
        event_data = fel, cpu, process
        event_handler = sjf_handler
        fel.schedule(engine.Event(event_data, event_handler), cycles)

    engine.run_sim(fel)
    print("All processes executed in", "{0:.2f}".format(cpu.execution_time + cpu.idle_time), "nanoseconds and consumed",
          "{0:.2f}".format(cpu.power_consumption),
          "nanowatts.\n")
    print("CPU was idle for:", cpu.idle_time, "nanoseconds")
    print("Total wait time:", cpu.total_wait_time, "nanoseconds")


def rr_loop(processes):
    fel = engine.FEL()
    cpu = CPU(CLOCK_SPEED)

    for process in processes:
        name, cycles, arrival_time = process
        event_data = fel, cpu, process
        event_handler = rr_handler
        fel.schedule(engine.Event(event_data, event_handler), arrival_time)

    engine.run_sim(fel)
    print("All processes executed in", "{0:.2f}".format(cpu.execution_time + cpu.idle_time),
          "nanoseconds and consumed",
          "{0:.2f}".format(cpu.power_consumption),
          "nanowatts.\n")
    print("CPU was idle for:", cpu.idle_time, "nanoseconds")
    print("Total wait time:", cpu.total_wait_time, "nanoseconds")


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
        fcfs_loop(processes)
    if sjf:
        print("Executing using Shortest Job First (SJF) scheduling.")
        sjf_loop(processes)
    if rr:
        print("Executing using Round Robin (RR) scheduling.")
        rr_loop(processes)


main()
