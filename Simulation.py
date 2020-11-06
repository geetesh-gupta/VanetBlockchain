from Node import Node, StaticNode, Accident
from random import randint, choice
from Sockets import create_msg
from Functions import func_per_second, check_dict_within_range, get_dict_distance
from threading import Thread, Event
import json
import signal


class Simulation:

    def __init__(self, x_range, y_range, num_nodes, num_rsus):
        self.nodes = [
            Node(
                randint(0, x_range), randint(0, y_range),
                randint(0, 10), randint(0, 10)
            ) for _ in range(num_nodes)]
        self.rsus = [
            StaticNode(
                choice([0, x_range, x_range // 2]),
                choice([0, y_range, y_range // 2])
            ) for _ in range(num_rsus)]
        self.x_range = x_range
        self.y_range = y_range
        self.accidents = []

    def simulate_send_msg(self):
        """
        Simulation function to test messaging socket functionality
        """
        self.nodes[0].send_msg(self.nodes[1].server.server_address,
                               create_msg(self.nodes[0].server.server_address, "Hi"))
        self.nodes[1].send_msg(self.rsus[0].server.server_address,
                               create_msg(self.nodes[1].server.server_address, "Hi"))
        self.rsus[0].send_msg(self.rsus[1].server.server_address,
                              create_msg(self.rsus[0].server.server_address, "Hi"))

    def display_coordinates(self):
        """
        Displays the coordinates of the nodes and RSUs
        """
        for i, node in enumerate(self.nodes):
            print("Node", i+1, node.get_pos())
        for i, rsu in enumerate(self.rsus):
            print("RSU", i+1, rsu.get_pos())

    def frame(self):
        """
        Contains the functions that will be executed on every frame change
        which is currently set to change every second
        """

        # Exit the thread if Exit Event is called
        if exit_event.is_set():
            exit(0)

        # print("New frame")
        vehicle_thread = Thread(target=self.move_vehicles)
        accident_thread = Thread(target=self.check_accidents_nearby)
        vehicle_thread.start()
        accident_thread.start()

    def start(self):
        """
        Entry function to start the simulation.
        Changes frame every second.
        """

        func_per_second(self.frame)

    def move_vehicles(self):
        """
        Updates all the moving vehicle's position
        """
        for node in self.nodes:
            node.move()

    def simulate_accident(self):
        """
        Creates accident objects to simulate accident scenarios
        """
        self.accidents.append(Accident(500, 500))
        # self.accidents.append(Accident(250, 500))
        # self.accidents.append(Accident(500, 250))
        # self.accidents.append(Accident(750, 500))
        # self.accidents.append(Accident(500, 750))

    def action_on_accident(self, node, accident):
        """
        Contains the functions to call 
        when a node detects accident within its range
        TODO: Prevent calling this function every second for optimisation (To think)
        """

        # Exit the thread if Exit Event is called
        if exit_event.is_set():
            exit(0)

        # Reverse the node's direction to take different route
        node.reverse_direction()

        nearby_node = self.get_nearby_node(node, self.nodes + self.rsus)
        if not nearby_node:
            return

        # Send message to the nearby node
        node.send_msg(
            nearby_node.server.server_address,
            create_msg(
                node.server.server_address,
                f"Accident at ({accident.get_pos()['x']}, {accident.get_pos()['y']})"
            )
        )

        # Recurse on nearby node
        # TODO: Devise a way to prevent calling previous node
        self.action_on_accident(nearby_node, accident)

    def check_accidents_nearby(self):
        """
        Checks if any accident has occured in the range of the any node
        If so, starts a thread to call action_on_accident function
        """
        for node in self.nodes:
            for accident in self.accidents:
                if check_dict_within_range(node.get_pos(), node.range, accident.get_pos()):
                    notify_accident_thread = Thread(
                        target=self.action_on_accident,
                        args=(node, accident)
                    )
                    notify_accident_thread.start()

    def get_nearby_node(self, node, nodes_list):
        """
        Returns the nearby node
        TODO: To rethink if one nearby_node or all are needed
        """

        # Stores all the nearby nodes in the range of current node
        nearby_nodes = []
        for n_node in nodes_list:
            if node is not n_node and check_dict_within_range(node.get_pos(), node.range, n_node.get_pos()):
                nearby_nodes.append(n_node)

        if len(nearby_nodes) == 0:
            return None

        # Returns the minimum distance node amont the nearby nodes
        min_dist = float('inf')
        min_dist_node = None
        for n_node in nearby_nodes:
            cur_dist = get_dict_distance(node.get_pos(), n_node.get_pos())
            if cur_dist < min_dist:
                min_dist = cur_dist
                min_dist_node = n_node
        return min_dist_node


def signal_handler(signum, frame):
    """
    Handles Exit Event
    """
    print("\n😄 Thank you for using our VanetBlockChain simulation 😄")
    exit_event.set()


if __name__ == "__main__":
    # Exit handler on Keyboard Interrupt
    exit_event = Event()
    signal.signal(signal.SIGINT, signal_handler)

    # Simulation
    simulation = Simulation(1000, 1000, 7, 3)

    # Display Coordinates of nodes
    simulation.display_coordinates()

    # Starting simulation in a thread to call further function
    simulation_thread = Thread(target=simulation.start)
    simulation_thread.start()

    # Simulate Accidents
    simulation.simulate_accident()

    # Simulate Sending Messages Functionality
    # simulation.simulate_send_msg()
