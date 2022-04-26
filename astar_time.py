from load_csv import ad, speed_limit_avg, eudis, avg_speed
import copy


def astar_time(start, end):
    # print( avg_speed )
    # Begin your code (Part 6)
    # the astar score: euclidean distance / avg_speed in this intersection(take the come point into consideration)
    # total info to compare: (time spent so far) + (predict to still spend how much time) -> predict... = astar score
    """
    [ similar to astar ]
    1. extraly import d1, d2, d3 from constant.py for better representation for eudis's value
    2. the astar score, f(n), here:
        g(n): "real time" to get to this place
        h(n): "predict time" to get to this place = predict distance / predict speed
                * predict distance: I use the euclidean distance in the heuristic.csv
                * predict speed: set to be "avg_speed" from load_csv [****]
        
        [XXXX wrong XXXX] 
        h(n): "predict time" to get to this place = predict distance / predict speed
                * predict distance: I use the euclidean distance in the heuristic.csv
                * predict speed:  [***]
                    at every point, we will have the next few(or 0) paths to choose as next 
                    decision, I take the "average speed limit" of them as the predicted
                    future speed to the end
        [XXXX wrong XXXX]

        use "second" as the unit
        * we set the astar score to 0 for initial point is fine, cuz it is the first element
          we need to process, without comparison

    3. [***] the algo is not allowed to stop before it find the answer that is lower than 800 seconds 
    
    * watch out:
        [1] next_id may not in speed_limit_avg 
            -> you can walk there doesn't implies there can walk to other places
            * if next_id not in speed_limit_avg:
                set the predicted time(heuristic score) to infinite if it is not end
        [2] remember to delete thing after process it
    """
    pool = dict()
    vis = dict() # the vis here also need to record the a star score
    pool[start] = (0, 0, [start]) # real + astar(second), real(second), path
    # the real initialize to be 0 is fine, no need to count it extraly cuz it will definitely be process at first
    final_path_second = 800
    final_path = []

    while True:
        now_key = min( pool.keys(), key=(lambda k: pool[k][0]) )  # extract min from pool base on the first element in value tuple
        
        if now_key in vis:
            if vis[now_key] < pool[now_key][0]: # if now astar score is bigger than the record in vis
                del pool[now_key] # dead_end -> remove it from the pool and run continue to help us select next min
                continue
            else:
                vis[now_key] = pool[now_key][0] # renew the record and keep running on new one to expand others
        else:
            vis[now_key] = pool[now_key][0] # not in vis -> add this time's record into vis
        
        if now_key == end:
            if final_path_second > pool[now_key][1]:  # ***** if the second is better than 800 second, than the astar algorithm can be stop *****
                final_path_second = pool[now_key][1]
                final_path = pool[now_key][2]
                break


        now_id = now_key
        now_real_plus_astar = pool[now_key][0]
        now_real_second = pool[now_key][1]
        now_path = pool[now_key][2]

        if now_id in ad:
            for next_node in ad[now_id]:
                next_id = next_node[0]
                next_time = next_node[3]
                predict_time_to_end = 0
                if next_id not in speed_limit_avg: # next_id can't go to anywhere else
                    if next_id != end:
                        predict_time_to_end = 1e8 # set it to be infinite large cuz it can't reach end point -> maybe need to record so don't continue directly
                else:
                    predict_time_to_end = eudis[next_id][end] / avg_speed # ******
                
                if next_id not in vis:
                    # directly add to the pool
                    next_path = copy.deepcopy( now_path )
                    next_path.append( next_id )
                    pool[next_id] = ( now_real_second + next_time + predict_time_to_end, now_real_second + next_time, next_path )
                    vis[next_id] = (now_real_second + next_time + predict_time_to_end)  # ***
                else:
                    if (now_real_second + next_time + predict_time_to_end)  < vis[next_id]:
                        next_path = copy.deepcopy( now_path )
                        next_path.append( next_id )
                        pool[next_id] = ( now_real_second + next_time + predict_time_to_end, now_real_second + next_time, next_path )
                        vis[next_id] = (now_real_second + next_time + predict_time_to_end)  # ***
        
        del pool[now_key] # remember to delete it

    return final_path, final_path_second, len(vis)
    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time(1718165260, 8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
