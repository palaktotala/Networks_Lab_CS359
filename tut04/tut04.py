import threading
import time
from queue import Queue

neighbour_dict = {}
weight_dict = {}
queue_dict = {}
routing_table_dict = {}
node_map_dict = {}
value_map_dict = {}
updated_dict = {}
all_nodes_list = []
num = 0
inf = 10000
done = 0

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
            for node in line:
                all_nodes_list.append(node)
                neighbour_dict[node] = []
                routing_table_dict[node] = [inf] * num
                weight_dict[node] = [inf] * num
                updated_dict[node] = [0] * num
                queue_dict[node] = Queue()
                node_map_dict[node] = cnt
                value_map_dict[cnt] = node
                routing_table_dict[node][cnt] = 0
                cnt += 1
        else:
            u = line[0]
            v = line[1]
            w = int(line[2])
            neighbour_dict[u].append((v, w))
            neighbour_dict[v].append((u, w))
            weight_dict[u][node_map_dict[v]] = w
            weight_dict[v][node_map_dict[u]] = w
            queue_dict[u].put((v, routing_table_dict[v]))
            queue_dict[v].put((u, routing_table_dict[u]))
        idx += 1

def print_routing_table(router):
    to_print = f"{router}:"
    for i in range(num):
        to_print += f"\t{value_map_dict[i]}, {'*' if updated_dict[router][i] == 1 else ''}{routing_table_dict[router][i]}"
    print(to_print)

done = 0

def update_router(router):
    while True:
        print_routing_table(router)

        global done
        done += 1
        if done == num:
            done = 0
            print('\n')

        time.sleep(2)

        updated_dict[router] = [0] * num

        while not queue_dict[router].empty():
            elem = queue_dict[router].get()
            cnt = 0
            for val in elem[1]:
                if val + weight_dict[elem[0]][node_map_dict[router]] < routing_table_dict[router][cnt]:
                    updated_dict[router][cnt] = 1
                    routing_table_dict[router][cnt] = val + weight_dict[elem[0]][node_map_dict[router]]
                cnt += 1
            for neighbours in neighbour_dict[router]:
                queue_dict[neighbours[0]].put((router, routing_table_dict[router]))

def main():
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
            for node in line:
                all_nodes_list.append(node)
                neighbour_dict[node] = []
                routing_table_dict[node] = [inf] * num
                weight_dict[node] = [inf] * num
                updated_dict[node] = [0] * num
                queue_dict[node] = Queue()
                node_map_dict[node] = cnt
                value_map_dict[cnt] = node
                routing_table_dict[node][cnt] = 0
                cnt += 1
        else:
            u = line[0]
            v = line[1]
            w = int(line[2])
            neighbour_dict[u].append((v, w))
            neighbour_dict[v].append((u, w))
            weight_dict[u][node_map_dict[v]] = w
            weight_dict[v][node_map_dict[u]] = w
            queue_dict[u].put((v, routing_table_dict[v]))
            queue_dict[v].put((u, routing_table_dict[u]))
        idx += 1

    threads = []
    for node in all_nodes_list:
        threads.append(threading.Thread(target=update_router, args=(node,)))
        threads[-1].start()
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()

