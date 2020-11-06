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
        self.nodes[0].send_msg(self.nodes[1].server.server_address,
                               create_msg(self.nodes[0].server.server_address, "Hi"))
        self.nodes[1].send_msg(self.rsus[0].server.server_address,
                               create_msg(self.nodes[1].server.server_address, "Hi"))
        self.rsus[0].send_msg(self.rsus[1].server.server_address,
                              create_msg(self.rsus[0].server.server_address, "Hi"))

    def display_coordinates(self):
        for i, node in enumerate(self.nodes):
            print("Node", i+1, node.get_pos())
        for i, rsu in enumerate(self.rsus):
            print("RSU", i+1, rsu.get_pos())

    def frame(self):
        if exit_event.is_set():
            exit(0)
        # print("New frame")
        vehicle_thread = Thread(target=self.move_vehicles)
        accident_thread = Thread(target=self.check_accidents_nearby)
        vehicle_thread.start()
        accident_thread.start()

    def start(self):
        func_per_second(self.frame)

    def move_vehicles(self):
        for node in self.nodes:
            node.move()

    def simulate_accident(self):
        self.accidents.append(Accident(500, 500))
        # self.accidents.append(Accident(250, 500))
        # self.accidents.append(Accident(500, 250))
        # self.accidents.append(Accident(750, 500))
        # self.accidents.append(Accident(500, 750))

    def action_on_accident(self, node, accident):
        
        if exit_event.is_set():
            exit(0)
        node.reverse_direction()
        nearby_node = self.get_nearby_node(node, self.nodes + self.rsus)
        if not nearby_node:
            return False
        node.send_msg(
            nearby_node.server.server_address,
            create_msg(
                node.server.server_address,
                f"Accident at ({accident.get_pos()['x']}, {accident.get_pos()['y']})"
            )
        )
        self.action_on_accident(nearby_node, accident)

    def check_accidents_nearby(self):
        for node in self.nodes:
            for accident in self.accidents:
                if check_dict_within_range(node.get_pos(), node.range, accident.get_pos()):
                    notify_accident_thread = Thread(
                        target=self.action_on_accident,
                        args=(node, accident)
                    )
                    notify_accident_thread.start()

    def get_nearby_node(self, node, nodes_list):
        nearby_nodes = []

        for n_node in nodes_list:
            if node is not n_node and check_dict_within_range(node.get_pos(), node.range, n_node.get_pos()):
                nearby_nodes.append(n_node)

        if len(nearby_nodes) == 0:
            return None

        min_dist = float('inf')
        min_dist_node = None
        for n_node in nearby_nodes:
            cur_dist = get_dict_distance(node.get_pos(), n_node.get_pos())
            if cur_dist < min_dist:
                min_dist = cur_dist
                min_dist_node = n_node
        return min_dist_node


def signal_handler(signum, frame):
    print("\n😄 Thank you for using our VanetBlockChain simulation 😄")
    exit_event.set()


if __name__ == "__main__":
    # Exit handler on Keyboard Interrupt
    exit_event = Event()
    signal.signal(signal.SIGINT, signal_handler)

    simulation = Simulation(1000, 1000, 7, 3)
    simulation.display_coordinates()
    simulation_thread = Thread(target=simulation.start)
    simulation_thread.start()
    simulation.simulate_accident()
    # simulation.simulate_send_msg()
