from Node import Node, StaticNode
from random import randint, choice
from Sockets import create_msg
from Functions import func_per_second
from concurrent.futures import ThreadPoolExecutor


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
        print("New frame")
        self.move_vehicles()

    def start(self):
        try:
            func_per_second(self.frame)
        except KeyboardInterrupt:
            print("\n😄 Thank you for using our VanetBlockChain simulation 😄")

    def move_vehicles(self):
        for node in self.nodes:
            node.move()

    def simulate_accident(self):
        self.accidents.append((100, 100))


if __name__ == "__main__":
    simulation = Simulation(1000, 1000, 3, 3)
    simulation.display_coordinates()
    # simulation.simulate_send_msg()
    simulation.start()
