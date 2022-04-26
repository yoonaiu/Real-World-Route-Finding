import queue
import copy
from load_csv import ad

def bfs(start, end):
    
    # Begin your code (Part 1)
    """
    0. set, dict are built in with python3, can be used without imported

    1. import ad from load_csv.py

    2. run the BFS
        (1) vis set to record the visited node
        (2) q to run the BFS
        (3) get final_path = list of (start, end, distance)

        * watch out:
            [1] find next accessble & non-visited place
            [2] before using key, need to check if it is valid first [ invalid key error ]
            [3] when the time put node into queue, need to mark it as visited, 
                early mark will be correct
            [4] for array, need to use deep copy, or the "path_so_far" store into queue 
                will be changed afterword when we are changing outside "path_so_far"
            [5] need to remove the current choice in "path_so_far" for the next choice in for loop
            [6] when get the value from q, it will pop it too
    
    3. return
        (1) path - list of integer
        (2) total dis - float
        (3) number of node visited

       extract things from final_path
       [start, n1]
       [n1,   end] -> get the first colum, and add the end point in the end
    """

    # 2. BFS
    vis = set()
    q = queue.Queue()
    q.put( (start, []) )
    final_path = []
    while not q.empty():
        tmp = q.get()
        current_id = tmp[0]
        path_so_far = tmp[1]

        if current_id == end:
            final_path = path_so_far
            break

        if current_id in ad:
            for next_node in ad[current_id]:
                next_id = next_node[0]
                dis = next_node[1]
                if next_id not in vis:
                    vis.add( next_id )
                    path_so_far.append( (current_id, next_id, dis) )
                    q.put( (next_id, copy.deepcopy(path_so_far)) )
                    path_so_far.remove( (current_id, next_id, dis) )

    # 3. set up the return value
    path = []
    dist = 0
    num_visited = len(vis)

    for node in final_path:
        path.append( node[0] )
        dist += float(node[2])
    path.append( final_path[ len(final_path)-1 ][1] )

    return path, dist, num_visited
    # End your code (Part 1)


if __name__ == '__main__':
    path, dist, num_visited = bfs(1718165260, 8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
