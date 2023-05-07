import threading
import time
from queue import Queue

# Initialize dictionaries and variables
neighbours_dict = {}
weights_dict = {}
queue_dict = {}
routing_table_dict = {}
node_map_dict = {}
value_map_dict = {}
updated_dict = {}
improved_dict = {}
all_nodes_list = []
num = 0 
inf = 10000
done = 0

# Read input from the topology file
def read_input():
    file_object = open(r"topology.txt", "r")
    idx = 0
    for line in file_object:
        line = line.split()
        if line[0] == "EOF":
            break
        if idx == 0:
            global num
            num = int(line[0])
        elif idx == 1:
            cnt = 0
            # Initialize dictionaries and lists for each router
            for node in line:
                all_nodes_list.append(node)
                neighbours_dict[node] = []
                routing_table_dict[node] = [inf] * num
                weights_dict[node] = [inf] * num
                updated_dict[node] = [0] * num
                improved_dict[node] = [0] * num
                queue_dict[node] = Queue()
                node_map_dict[node] = cnt
                value_map_dict[cnt] = node
                routing_table_dict[node][cnt] = 0
                cnt += 1
        else:
            u, v, w = line[0], line[1], int(line[2])
            # Add neighbours and weights to dictionaries
            neighbours_dict[u].append((v, w))
            neighbours_dict[v].append((u, w))
            weights_dict[u][node_map_dict[v]] = w
            weights_dict[v][node_map_dict[u]] = w
            # Initialize routing table with initial weights
            routing_table_dict[u][node_map_dict[v]] = w
            routing_table_dict[v][node_map_dict[u]] = w
            # Add routers to the queue for communication
            queue_dict[u].put((v, routing_table_dict[v]))
            queue_dict[v].put((u, routing_table_dict[u]))
        idx += 1

# Print the routing table for a specific router
def print_routing_table(router):
    to_print = f"{router}:"
    for i in range(num):
        to_print += f"\t{value_map_dict[i]}, {'*' if improved_dict[router][i] == 1 else ''}{routing_table_dict[router][i]}"
    print(to_print)

# Update the routing table for a specific router
def update_router(router):
    updated_dict[router] = [0] * num
    updated_dict[router][node_map_dict[router]] = 1
    while True:
        print_routing_table(router)

        global done
        done += 1
        if done == num:
            done = 0
            print('\n')

        time.sleep(2)

        improved_dict[router] = [0] * num

        cnt = 0
        mn, mn_node = inf, 0
        for val in all_nodes_list:
            if val == router:
                continue
            if routing_table_dict[router][cnt] <= mn and updated_dict[router][cnt] == 0:
                mn = routing_table_dict[router][cnt]
                mn_node = cnt
            cnt += 1
        if mn_node != -1:
            updated_dict[router][mn_node] = 1
            for neighbours in neighbours_dict[value_map_dict[mn_node]]:
                old = routing_table_dict[router][node_map_dict[neighbours[0]]]
                new = mn + neighbours[1]
                routing_table_dict[router][node_map_dict[neighbours[0]]] = min(old, new)
                if new < old:
                    improved_dict[router][node_map_dict[neighbours[0]]] = 1
                queue_dict[neighbours[0]].put((router, routing_table_dict[router]))

# Main function
def main():
    # Read input and initialize data structures
    read_input()

    # Create threads for each router and start them
    threads = []
    for node in all_nodes_list:
        threads.append(threading.Thread(target=update_router, args=(node,)))
        threads[-1].start()  

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()

