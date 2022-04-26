from load_csv import ad
import copy


def ucs(start, end):

    # Begin your code (Part 3)
    """
    1. load ad from load_csv.py

    2. run the ucs
        (1) everytime select the min distance one from the pool and see if it is Goal:
            if yes: add it to the vis and finish ucs
            if no:  keep doing following (2)
        (2) relax others and add this point into vis after this process
            relax:
                if the point now can go to is "not" in the "pool" now, add it to the pool,
                else check the value in the pool:
                    if the value now is better:
                        renew the value in the pool to the value this time
                        == **give dead end to the original record**

    * watch out:
        [1] need to add start to the pool at first, and set to 0, 
            to let usc can start expand(run) from it
        [2] store the path for each node during the process,
            cuz every node need to succeed the last one
            -> "one node one list" is enough cuz will only need the "optimal" record
        [3] remember to add the goal point into vis at final 
            -> after we finished it, it is viewed as visited
        [4] ** need to delete the record in pool, **
            or the min function can't get next element in the dict
        [5] need to deepcopy the path, or the original one will be used in
            unexpected place and all the record is linked with each other,
            everybody is changing the same record, which is wrong
    """

    pool = dict()
    vis = set()
    pool[start] = 0 
    path_node = dict()
    path_node[start] = [start]  # store the list of node(path) to go to each node
    final_dist = 0
    final_path = []

    while True:
        # return the key who store the minimum value in pool
        now_id = min( pool.keys(), key=(lambda k: pool[k]) )
        if now_id == end:
            vis.add(now_id)
            final_dist = pool[now_id]
            final_path = path_node[now_id]
            break

        if now_id in ad:
            for next_node in ad[now_id]:
                next_id = next_node[0]
                dis = next_node[1]
                if next_id not in vis:
                    if next_id not in pool:
                        pool[next_id] = pool[now_id] + dis
                        path_node[next_id] = copy.deepcopy(path_node[now_id])
                        path_node[next_id].append(next_id)
                    else: # next_id already in the pool -> see if need to renew value
                        if pool[now_id] + dis < pool[next_id]:
                            pool[next_id] = pool[now_id] + dis
                            path_node[next_id] = copy.deepcopy(path_node[now_id])
                            path_node[next_id].append(next_id)

        vis.add( now_id ) # add to vis after use it to relax others
        del pool[now_id] # need to delete the record in pool, or the min function can't get next element

    return final_path, final_dist, len(vis)
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(1718165260, 8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
