import copy
import threading
import queue
import time
from datetime import datetime

lock = threading.Lock()
start_time = datetime.now()

class Router:
    def __init__(self, router_id, adj_list, router_queues):
        self.router_id = router_id
        self.adj_list = adj_list
        self.router_queues = router_queues
        self.routing_table = {}
        self.changes = {}
        self.routing_table["itr"] = [router_id, 0]
        for router in adj_list.keys():
            self.routing_table[router] = [-1, -1]
        self.routing_table[router_id] = [router_id, 0]
        for router in adj_list[router_id]:
            self.routing_table[router] = [router, adj_list[router_id][router]]
        for router in adj_list.keys():
            self.changes[router] = 0

    def __call__(self):
        while self.routing_table["itr"][1] < len(self.adj_list):
            lock.acquire()
            print("_________________________")
            print("|\t|\t\t|")
            s = "| "+self.router_id+"\t| iteration "+str(self.routing_table["itr"][1])+"\t|"
            print(s)
            print("|_______|_______________|", "\n|\t|\t|\t|")
            print("|", end=' ')
            print("To", "\t|",
                  "Via", "\t|", "Cost", "\t|")
            print("|_______|_______|_______|")
            print("|\t|\t|\t|")
            for router in self.adj_list:
                print("|", end=' ')
                if self.changes[router]:
                    print("*", end='')
                print(router, "\t|",
                      self.routing_table[router][0], "\t|", self.routing_table[router][1], "\t|")
            print("|_______|_______|_______|")
            self.changes = {router: 0 for router in self.adj_list}
            lock.release()

            for router in self.adj_list:
                if router != self.router_id:
                    try:
                        self.router_queues[router].put_nowait(copy.deepcopy(self.routing_table))
                    except queue.Full:
                        print(router, "router's queue was full")

            time.sleep(2)

            while not self.router_queues[self.router_id].full():
                continue

            while not self.router_queues[self.router_id].empty():
                shared_table = self.router_queues[self.router_id].get()
                for router in self.adj_list:
                    if (self.routing_table[router][1] == -1 and shared_table[router][router][1] != -1):
                        self.routing_table[router] = [shared_table["itr"][0], shared_table[router][1] + self.adj_list[self.router_id][shared_table["itr"][0]]]
                        self.changes[router] = 1
                    if (self.routing_table[router][1] != -1 and shared_table[router][router][1] != -1):
                        if (self.routing_table[router][1] > shared_table[router][router][1] + self.adj_list[self.router_id][shared_table["itr"][0]]):
                            self.routing_table[router] = [shared_table["itr"][0], shared_table[router][1] + self.adj_list[self.router_id][shared_table["itr"][0]]]
                            self.changes[router] = 1
                del shared_table

            self.routing_table["itr"][1] += 1

def main():
    list_routers = []
    adj_list = {}
    router_queues = {}

    with open("topology.txt", "r") as input_file:
        num_routers = int(input_file.readline().strip())

        router_names = input_file.readline().strip().split(' ')
        for router_name in router_names:
            list_routers.append(router_name)
            adj_list[router_name] = {}

        for line in input_file:
            line = line.strip()
            if line == "EOF":
                break
            node1, node2, cost = line.split()
            adj_list[node1][node2] = int(cost)
            adj_list[node2][node1] = int(cost)

    for router_name in list_routers:
        router_queues[router_name] = queue.Queue(num_routers + 1)

    routers = []
    for router_name in list_routers:
        routers.append(Router(router_name, adj_list, router_queues))

    threads = []
    for router in routers:
        thread = threading.Thread(target=router)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("Program execution time:", datetime.now() - start_time)

if __name__ == "__main__":
    main()
