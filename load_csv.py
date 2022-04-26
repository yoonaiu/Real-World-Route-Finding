import csv
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'

"""
ad: load the graph as an adlist
    (1) use csv related function to get the info
    (2) store into an "dict":
                key:   the place id
                value: list of tuple, (places_id, dis, speed_limit)
                        * speed limit need to change from km/hr to m/s (/3.6)

eudis: just load, 
       eudis[now_id][destination_id] can get the Euclidean distance

speed_limit_avg:  [XXXX no need XXXX] -> the result of test3 will exceed 1000 s
        directly count for the average, cuz the record in ad must mean 
        that you can walk there, don't mind who can walk to you
        ex: 
            a->b won't record in b, b will only record b->c, d, e,
            which is right the "path b can choose", no related to a(who can walk to b)

* things in the row are string type, need to change to int / float type *
"""

avg_speed = 0
cnt = 0
ad = dict()
with open(edgeFile, 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader) # skip the header
    for row in csvreader:
        a, b, dis, speed_limit = int(row[0]), int(row[1]), float(row[2]), float(row[3])/3.6  # speed_limit: km/hr -> m/s
        time = dis / speed_limit
        avg_speed += speed_limit
        cnt += 1
        if a not in ad:
            ad[a] = [(b, dis, speed_limit, time)]  # speed limit is used by speed_limit_avg, not in astar time
        else:
            ad[a].append( (b, dis, speed_limit, time) )    # the key of the dict can be an int
    avg_speed /= cnt

eudis = dict()
with open(heuristicFile, 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        # d1: 1079387396,  d2: 1737223506,  d3: 8513026827 -> can get from header
        tmp = dict()
        tmp[1079387396], tmp[1737223506], tmp[8513026827] = float(row[1]), float(row[2]), float(row[3])
        node_id = int(row[0])
        # node_id, d1, d2, d3 = int(row[0]), float(row[1]), float(row[2]), float(row[3])
        eudis[ node_id ] = tmp


# if one point have 3 roads to choose, this value will be the,
# avg speed limit value of the 3 road
# 只需要管可以去的地方就好，因為 a->b 的這條不會紀錄在 b 裏面，b只會紀錄 b-> c, d, e 
speed_limit_avg = dict()
for key in ad:
    """
    total = 0
    for item in ad[key]:
        total += item[2]
    speed_limit_avg[key] = total / float(len(ad[key]))
    """
    for item in ad[key]:
        if key in speed_limit_avg:
            speed_limit_avg[key] = max( speed_limit_avg[key], item[2])
        else:
            speed_limit_avg[key] = item[2]
    
