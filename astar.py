from load_csv import ad
from load_csv import eudis # need to use the [0] one
import copy

def astar(start, end):
    # Begin your code (Part 4)

    """
    1. load ad, eudis from load_csv.py

    2. run the astar
        (1) the vis in astar need to record the a star score
        (2) elements in pool: ( path_len + heu_score = ascore, true path_len, path list )
        (3) everytime extract "min ascore" in the pool
            , pool's value can be tuple:
                # extract min from pool base on the "first" element in value tuple
                now_key = min( pool.keys(), key=(lambda k: pool[k][0]) )
        (4) if we have visited the node, check if the record in vis is the best:
                if yes: del now node in pool -> set it to be deadend, cuz the record is better
                if no: renew the record and run the following relax process
            else not yet vis:
                add to vis and record the value
        (5) if now == end -> extract value and break, no need to add into vis again
        (6) else keep run following astar:
            [1] find all next possible reach point
            [2] calculate 
                    <1> their "astar score" f(n) as: 
                        f(n) = g(n) + h(n)
                        g(n) = "real path len" to next_id
                        h(n) = "predict dis" to end point
                        the unit is "meter"
                        *the (true path_len so far) we store in pool can help us count faster*
                    <2> remember to deepcopy the path
            [3] if next_id is already "vis" (not in pool)
                    check if the value now is better:
                        yes: "add it into the pool again" to count for better record 
                            the step change renew the value will run when we selected it,
                            or actually implement here
                        no: ignore it
                if not in vis:
                    directly add to vis
        (7) **remember to delete the node we processed to help us move to next choice in pool!**
   
    * watch out:
        [1] everytime we run a key in dict, we need to first check if it is in the dict
            [invalid key error]
        [2] *** the visit need to renew earler, or the answer will be incorrect!! ***
    """

    pool = dict()
    vis = dict()
    pool[start] = (eudis[start][end]+0, 0, [start])
    final_path_len = 0
    final_path = []

    while True:
        now_key = min( pool.keys(), key=(lambda k: pool[k][0]) )
        
        if now_key in vis:
            if vis[now_key] < pool[now_key][0]: # if now astar score is bigger than the record in vis
                del pool[now_key] # dead_end -> remove it from the pool and run continue to help us select next min
                continue
            else:
                vis[now_key] = pool[now_key][0] # renew the record and keep running on new one to expand others
        else:
            vis[now_key] = pool[now_key][0] # not in vis -> add this time's record into vis

        if now_key == end:
            final_path_len = pool[now_key][1]
            final_path = pool[now_key][2]
            break


        now_id = now_key
        now_heu = pool[now_key][0]
        now_path_len = pool[now_key][1]
        now_path = pool[now_key][2]

        if now_id in ad:
            for next_node in ad[now_id]:
                next_id = next_node[0]
                dis = next_node[1]
                if next_id not in vis:
                    # directly add to the pool
                    next_path = copy.deepcopy( now_path )
                    next_path.append( next_id )
                    pool[next_id] = ( now_path_len + dis + eudis[next_id][end], now_path_len + dis, next_path )
                    vis[next_id] = now_path_len + dis + eudis[next_id][end]  # ***
                else:
                    if (now_path_len + dis + eudis[next_id][end])  < vis[next_id]:
                        next_path = copy.deepcopy( now_path )
                        next_path.append( next_id )
                        pool[next_id] = ( now_path_len + dis + eudis[next_id][end], now_path_len + dis, next_path )
                        vis[next_id] = now_path_len + dis + eudis[next_id][end]  # ***
        
        del pool[now_key] # remember to delete it

    return final_path, final_path_len, len(vis)
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(1718165260, 8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
