import sys
from load_csv import ad

"""
[ dfs2 ]
    global: (var easy to access for dfs2 recursion)
        vis_total: a set to record the visited node, we can' go to the place twice,
                   the run time will exceed and we will always do the repeating searching
        final_path, final_dist: for "dfs" can get the result ans
    
    * watch out:
        [1] add the current id to the vis_total everytime enter the dfs2, 
            and no need to pop it out at any situation
            even it is impossible for this point to reach the end point, 
            store it into vis can help us don't try the wrong path again,
            also, we can't choose back road in searching, we can only move forward,
            we will go back naturally by the return of function(but all the vis record still will be there)

        [2] if successful get to the end point, create a "return True chain" 
            keep returning back to the first call
            Otherwise, return False to let the last layer to find next possible choice
        [3] element in ad[a]: (node_id_b, distance between a & b)
        [4] recover the things if it was a fail try return.
            with the recover be implemented, we can pass the array by reference directly,
            no need to use deep copy
"""
start, end = 0, 0
vis_total = set()
final_path = []
final_dist = 0

def dfs2( now_id, path, dist ):
    global start, end, vis_total
    vis_total.add( now_id )

    if now_id == end:
        global final_path, final_dist
        final_path = path
        final_dist = dist
        return True
    
    # not yet reach the end point
    if now_id in ad:
        for next_node in ad[ now_id ]:
            next_id = next_node[0]
            dis = next_node[1]
            if next_id not in vis_total:
                path.append( next_id )
                dist += dis
                if dfs2( next_id, path, dist ) == True:
                    return True
                path.remove( next_id )
                dist -= dis

    return False # not yet find the road to the end


def dfs(start_passin, end_passin):
    # Begin your code (Part 2)
    """
    1. load the ad from load_csv.py, and set the global value for dfs2
       * when using global value, need to import it into the code block first,
         or it won't use it as the global one 
    
    2. implement another dfs2 for the recursion
       dfs2( current node, path so far, dist accumulated )
       * set the recursion limit for the recursive, 
         or it won't completely run to the result
    """
    global start, end, vis_total
    start = start_passin
    end = end_passin
    
    sys.setrecursionlimit(6000)

    dfs2( start, [start], 0 )

    return final_path, final_dist, len(vis_total)
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(1718165260, 8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')