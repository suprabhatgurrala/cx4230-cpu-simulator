import time


class Event:
    """
    Object to handle events.
    """
    def __init__(self, event_data, event_handler):
        """
        Initializes event object
        :param event_data: data specific to the event instance
        :param event_handler: a method to handle the event, takes event_data as a paramter
        """
        self.timestamp = time.time()
        self.event_data = event_data
        self.event_handler = event_handler

    def handle(self):
        """
        calls the provided event handler with event_data as a parameter
        """
        self.event_handler(self.event_data)

class FEL:
    def schedule(self, event, priority):
        """
        Schedules an event into the priority queue.
        :param event: the event to schedule
        :param priority: the priority of the event to schedule
        """
        print("Scheduling event", event, "with priority", priority)
        self.priority_queue.append((event, priority))
        self.priority_queue.sort(key=lambda pair: pair[1])
        print(self.priority_queue)

    def remove(self):
        """
        Removes the last item in the priority queue
        :return: the last object in the priority queue
        """
        return self.priority_queue.pop()

    def is_empty(self):
        """
        :return: True if the FEL is empty, False otherwise
        """
        return len(self.priority_queue) == 0

    def __init__(self):
        self.priority_queue = []


def run_sim(fel):
    """
    Executes the simulation
    :param fel: the FEL to execute
    """
    while not fel.is_empty():
        event = fel.remove()
        event.handle()