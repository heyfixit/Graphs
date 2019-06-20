from room import Room
from player import Player
from world import World

import sys
sys.path.insert(0, '../graph')
from util import Stack, Queue  # These may come in handy

import random

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# roomGraph={0: [(3, 5), {'n': 1}], 1: [(3, 6), {'s': 0, 'n': 2}], 2: [(3, 7), {'s': 1}]}
# roomGraph={0: [(3, 5), {'n': 1, 's': 5, 'e': 3, 'w': 7}], 1: [(3, 6), {'s': 0, 'n': 2}], 2: [(3, 7), {'s': 1}], 3: [(4, 5), {'w': 0, 'e': 4}], 4: [(5, 5), {'w': 3}], 5: [(3, 4), {'n': 0, 's': 6}], 6: [(3, 3), {'n': 5}], 7: [(2, 5), {'w': 8, 'e': 0}], 8: [(1, 5), {'e': 7}]}
roomGraph={0: [(3, 5), {'n': 1, 's': 5, 'e': 3, 'w': 7}], 1: [(3, 6), {'s': 0, 'n': 2, 'e': 12, 'w': 15}], 2: [(3, 7), {'s': 1}], 3: [(4, 5), {'w': 0, 'e': 4}], 4: [(5, 5), {'w': 3}], 5: [(3, 4), {'n': 0, 's': 6}], 6: [(3, 3), {'n': 5, 'w': 11}], 7: [(2, 5), {'w': 8, 'e': 0}], 8: [(1, 5), {'e': 7}], 9: [(1, 4), {'n': 8, 's': 10}], 10: [(1, 3), {'n': 9, 'e': 11}], 11: [(2, 3), {'w': 10, 'e': 6}], 12: [(4, 6), {'w': 1, 'e': 13}], 13: [(5, 6), {'w': 12, 'n': 14}], 14: [(5, 7), {'s': 13}], 15: [(2, 6), {'e': 1, 'w': 16}], 16: [(1, 6), {'n': 17, 'e': 15}], 17: [(1, 7), {'s': 16}]}

world.loadGraph(roomGraph)

# UNCOMMENT TO VIEW MAP
world.printRooms()

player = Player("Name", world.startingRoom)

# Fill this out
traversalPath = []

# build the graph in a dictionary
graph = {}

# keep a dictionary mapping opposite directions
direction_opposites = {
    'n': 's',
    'e': 'w',
    's': 'n',
    'w': 'e'
}

# pick a random direction to start
exits = player.currentRoom.getExits()
direction = exits[random.randint(0,len(exits) - 1)]

# initialize the graph with question marks for available directions
initial_exits = {}
for e in exits:
    initial_exits[e] = '?'
print(initial_exits)

graph[player.currentRoom.id] = initial_exits

# in the end, our player will have visted all rooms in the roomGraph
# so maybe we should iterate until the player's graph is as long as the
# roomGraph
while len(graph) < len(roomGraph):
    # assume we left the last iteration inside a room and pointed in a direction
    # to an unknown room
    print("############## NEW ITERATION #########################")
    world.printRooms()
    print("Direction we're headed: ", direction)

    # remember the last room we were in
    last_room = player.currentRoom

    # move in that direction
    player.travel(direction)
    traversalPath.append(direction)
    print(f"--------CURRENT ROOM: {player.currentRoom.id}-----------")
    print("Graph length: ", len(graph) )
    print("Room Graph Length: ", len(roomGraph))


    # update the room using the last room we were in
    # initialize the available exits to all be question marks first
    room_exits = {}

    # if we've been to this room before, bring in those exits
    if player.currentRoom.id in graph:
        room_exits = graph[player.currentRoom.id]
    else:
        # otherwise, initialize them all to '?'
        for e in player.currentRoom.getExits():
            room_exits[e] = '?'


    # print(room_exits)

    # update the direction pointing to the room we came from
    room_exits[direction_opposites[direction]] = last_room.id

    graph[player.currentRoom.id] = room_exits
    # also update the last room's direction that points to this room
    graph[last_room.id][direction] = player.currentRoom.id

    # if we're at a dead end, move to the closest room with an open
    # path we haven't explored
    # dead end can be indicated by only having one exit (the way we came from)
    if len(room_exits) == 1:
        print("******** DEAD END *********")
        # walk the shortest path to closest room with an unexplored direction
        # breadth first search to find that path
        visited = set()

        # create a Queue to hold paths we must explore
        q = Queue()
        # enqueue the first step
        # it seems like we need to know the direction of each step
        # and the room id so I'm using a list of tuples (direction, room_id)
        q.enqueue([(direction_opposites[direction], last_room.id)])

        # while our q length is > 0, seek the first graph element with
        # a ? direction
        while q.size() > 0:
            # dequeue the first path
            path = q.dequeue()

            # the tuple to inspect will be the last element
            t = path[-1]
            room_id = t[1]
            room_direction = t[0]

            # if we haven't checked this room for ?'s yet

            # NOTE: we might want to keep an iteration count here
            # to see if we check all of the rooms and none of them
            # have ?'s
            if len(graph) == len(roomGraph):
                break

            if room_id not in visited:

                # mark it as visited now
                visited.add(room_id)

                # if this room has a question mark, we've found the
                # next room to move to
                # this is the case where the BFS is over
                unexplored = None
                for k,v in graph[room_id].items():
                    if v == '?':
                        unexplored = k
                        # we found a ?
                        print(f"Next closest unexplored: Room: {room_id}, direction: {room_direction}")
                        break
                    else:
                        # queue up these rooms
                        path_copy = list(path)
                        path_copy.append((k,v))
                        q.enqueue(path_copy)


                if unexplored is not None:
                    # we have the path to this room
                    # and we know a direction that hasn't been explored
                    # move the player here, set the direction
                    print(f"Moving there from Room: {player.currentRoom.id}")
                    for t in path:
                        # t is a tuple of (direction, room_id)
                        # so move the player along each direction
                        player.travel(t[0])
                        print(f"Moved {t[0]}")

                        # add the movements to the traversalPath
                        traversalPath.append(t[0])
                    # set the direction and end the search
                    direction = unexplored
                    break
    else:
        # we do not need to backtrack
        # find the next unexplored direction
        print("More than one exit available: ", room_exits)
        for k,v in room_exits.items():
            if v == '?':
                direction = k
                print("Next unexplored direction: ", k)
                # we found a ?
                break
    input("Next? ")


print(traversalPath)













# TRAVERSAL TEST
visited_rooms = set()
player.currentRoom = world.startingRoom
visited_rooms.add(player.currentRoom)

for move in traversalPath:
    player.travel(move)
    visited_rooms.add(player.currentRoom)

if len(visited_rooms) == len(roomGraph):
    print(f"TESTS PASSED: {len(traversalPath)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(roomGraph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.currentRoom.printRoomDescription(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     else:
#         print("I did not understand that command.")
