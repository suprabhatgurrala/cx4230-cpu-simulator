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

    def to_string(self):
        return "Event object with data" + str(self.event_data) + " at " + time.strftime("%H:%M:%S",
                                                                                        time.localtime(self.timestamp))

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

class FEL:
    def schedule(self, event, priority):
        """
        Schedules an event into the priority queue.
        :param event: the event to schedule
        :param priority: the priority of the event to schedule
        """
        self.priority_queue.append((event, priority))
        self.priority_queue.sort(key=lambda pair: pair[1])

    def remove(self):
        """
        Removes and returns the item at the front of the priority queue
        :return: the item at the front of the priority queue
        """
        return self.priority_queue.pop(0)

    def delete(self, event):
        """
        Removes and returns a specified Event object from the priority queue
        :param event: the Event object to remove
        :return: the removed Event object
        """
        return self.priority_queue.remove(event)

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
        event, priority = fel.remove()
        event.handle()