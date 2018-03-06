import csv
import sys

import engine

INPUT_FILE = "input.csv"
CLOCK_SPEED = 1  # gigahertz
POWER_CONSUMPTION = 15  # watts

SCHEDULE_EVENT_TYPE = "schedule"
EXECUTE_EVENT_TYPE = "execute"


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
        self.execution_time = 0
        self.power_consumption = 0
        self.total_wait_time = 0
        self.available_time = 0
        self.waiting_processes = []

    def add_waiting_process(self, process, priority):
        self.waiting_processes.append((process, priority))
        self.waiting_processes.sort(key=lambda pair: pair[1])

    def remove_waiting_process(self):
        return self.waiting_processes.pop(0)

    def num_waiting_processes(self):
        return len(self.waiting_processes)

    def to_string(self):
        return str(self.clock_speed) + " GHz CPU object"

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()


def fcfs_scheduler(params):
    """
    Handles arrivals of processes and schedules them to be executed on the CPU using the FCFS algorithm.
    :param params: the parameters passed into the handler. Expects a tuple of (fel, cpu, process)
    """
    fel = params[0]
    cpu = params[1]
    process = params[2]
    p_name, cycles_rem, arrival_time = process

    if cpu.free:
        cpu.free = False
        next_event_data = params
        runtime = cycles_rem / cpu.clock_speed
        event = engine.Event(next_event_data, process_handler, EXECUTE_EVENT_TYPE, name=p_name)
        fel.schedule(event, fel.now + runtime)
        cpu.available_time = fel.now + runtime
        print("Scheduled process", p_name, "to run at t =", fel.now)
    else:
        # CPU is not free or there are pending processes. Schedule the next deserving process for execution.
        cpu.add_waiting_process(process, arrival_time)
        wait_time = cpu.available_time - arrival_time
        cpu.total_wait_time += wait_time * cpu.num_waiting_processes()


def sjf_scheduler(params):
    """
    Handles arrivals of processes and schedules them to be executed on the CPU using the SJF algorithm
    :param params: the parameters passed into the handler. Expects a tuple of (fel, cpu, process)
    """
    fel = params[0]
    cpu = params[1]
    process = params[2]
    p_name, cycles_rem, arrival_time = process

    if cpu.free:
        cpu.free = False
        next_event_data = params
        runtime = cycles_rem / cpu.clock_speed
        event = engine.Event(next_event_data, process_handler, EXECUTE_EVENT_TYPE, name=p_name)
        fel.schedule(event, fel.now + runtime)
        cpu.available_time = fel.now + runtime
        print("Scheduled process", p_name, "to run at t =", fel.now)
    else:
        # CPU is not free or there are pending processes. Schedule the next deserving process for execution.
        cpu.add_waiting_process(process, cycles_rem)
        wait_time = cpu.available_time - arrival_time
        cpu.total_wait_time += wait_time * cpu.num_waiting_processes()


def process_handler(params):
    """
    Event handler to execute a process on the CPU
    :param params: the parameters passed into the handler. Expects a tuple of (CPU object, process)
    """
    fel = params[0]
    cpu = params[1]
    process = params[2]
    p_name, cycles_rem, arrival_time = process

    execute_time = cycles_rem / cpu.clock_speed
    cpu.execution_time += execute_time
    cpu.power_consumption += execute_time * POWER_CONSUMPTION
    cpu.free = True

    print("Executed process", p_name, "in", "{0:.2f}".format(execute_time),
          "nanoseconds using", "{0:.2f}".format(execute_time * POWER_CONSUMPTION), "nanowatts.")

    if cpu.num_waiting_processes() > 0:
        next_process, priority = cpu.remove_waiting_process()
        next_p_name, next_cycles_rem, next_arrival_time = next_process
        next_runtime = next_cycles_rem / cpu.clock_speed
        next_event_data = fel, cpu, next_process
        next_event = engine.Event(next_event_data, process_handler, EXECUTE_EVENT_TYPE, name=next_p_name)
        fel.schedule(next_event, fel.now + next_runtime)
        cpu.available_time = fel.now + next_runtime
        print("Scheduled process", next_p_name, "to run at t =", fel.now)


def input_scheduler(processes, scheduler):
    fel = engine.FEL()
    cpu = CPU(CLOCK_SPEED)
    for process in processes:
        p_name, cycles, arrival_time = process
        event_data = (fel, cpu, process)
        fel.schedule(engine.Event(event_data, scheduler, SCHEDULE_EVENT_TYPE, name=p_name), arrival_time)
    engine.run_sim(fel)

    print("Total wait time:", "{0:.2f}".format(cpu.total_wait_time), "nanoseconds")
    print("Total idle time:", "{0:.2f}".format(fel.now - cpu.execution_time), "nanoseconds")
    print("Total execution time:", "{0:.2f}".format(fel.now), "nanoseconds")
    print("Total power consumption:", "{0:.2f}".format(cpu.power_consumption), "nanowatts")


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
        input_scheduler(processes, fcfs_scheduler)
        print()
    if sjf:
        print("Executing using Shortest Job First (SJF) scheduling.")
        input_scheduler(processes, sjf_scheduler)
        print()
    if rr:
        print("Executing using Round Robin (RR) scheduling.")
        pass


main()
