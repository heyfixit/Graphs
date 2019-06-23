from room import Room
from player import Player
import random
import math
import truecolor
import time

class AdvVisualizer:
    def __init__(self):
        self.startingRoom = None
        self.rooms = {}
        self.roomGrid = []
        self.gridSize = 0
        self.tail_color = (81, 255, 7)
        self.room_color = (0, 98, 178)
        self.head_color = (255, 0, 246)
    def loadGraph(self, roomGraph):
        numRooms = len(roomGraph)
        rooms = [None] * numRooms
        gridSize = 1
        for i in range(0, numRooms):
            x = roomGraph[i][0][0]
            gridSize = max(gridSize, roomGraph[i][0][0], roomGraph[i][0][1])
            self.rooms[i] = Room(f"Room {i}", f"({roomGraph[i][0][0]},{roomGraph[i][0][1]})",i, roomGraph[i][0][0], roomGraph[i][0][1])
        self.roomGrid = []
        gridSize += 1
        self.gridSize = gridSize
        for i in range(0, gridSize):
            self.roomGrid.append([None] * gridSize)
        for roomID in roomGraph:
            room = self.rooms[roomID]
            self.roomGrid[room.x][room.y] = room
            if 'n' in roomGraph[roomID][1]:
                self.rooms[roomID].connectRooms('n', self.rooms[roomGraph[roomID][1]['n']])
            if 's' in roomGraph[roomID][1]:
                self.rooms[roomID].connectRooms('s', self.rooms[roomGraph[roomID][1]['s']])
            if 'e' in roomGraph[roomID][1]:
                self.rooms[roomID].connectRooms('e', self.rooms[roomGraph[roomID][1]['e']])
            if 'w' in roomGraph[roomID][1]:
                self.rooms[roomID].connectRooms('w', self.rooms[roomGraph[roomID][1]['w']])
        self.startingRoom = self.rooms[0]

    # take a list of moves i.e. ['n','s','e','e','w']
    # and issue those moves to a new player while printing
    # a colorized world at each move while sleeping a specified
    # time in between each print
    def walk_rooms(self, moves, sleep_time = None):

        # default sleep_time to 0.06
        if sleep_time is None:
            sleep_time = 0.06
        player = Player("Name", self.startingRoom)
        room_history = {player.currentRoom: [1,0]}
        move_count = 0
        for move in moves:

            # clear terminal character code
            print("\033c", end="")

            # print the current world
            self.printRooms(player, room_history, move_count)

            # move the player for the next iteration
            player.travel(move)

            # track the count of moves they've taken
            move_count += 1

            # track the number of visits a room has along with
            # the move_count when the player visited it (time since last visit)
            if player.currentRoom in room_history:
                room_history[player.currentRoom][0] += 1
                room_history[player.currentRoom][1] = move_count
            else:
                room_history[player.currentRoom] = [ 1, move_count ]

            # sleep a bit
            time.sleep(sleep_time)



    def printRooms(self, player = None, visited = None, moves = None):
        rotatedRoomGrid = []
        for i in range(0, len(self.roomGrid)):
            rotatedRoomGrid.append([None] * len(self.roomGrid))
        for i in range(len(self.roomGrid)):
            for j in range(len(self.roomGrid[0])):
                rotatedRoomGrid[len(self.roomGrid[0]) - j - 1][i] = self.roomGrid[i][j]
        print("#####")
        str = ""
        for row in rotatedRoomGrid:
            allNull = True
            for room in row:
                if room is not None:
                    allNull = False
                    break
            if allNull:
                continue
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if (((not visited and room is not None) or (visited and room in visited)) and room.n_to is not None):
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if (((not visited and room is not None) or (visited and room in visited)) and room.w_to is not None):
                # if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    if player and player.currentRoom == room:
                        # \033[1m is an ansi escape sequence to create bold text
                        str += truecolor.color_text("\033[1m" + f"{room.id}".zfill(3), (255,0,0), self.head_color)
                    elif visited and room not in visited:
                        if room.w_to in visited or room.e_to in visited or room.s_to in visited or room.n_to in visited:
                            str += truecolor.color_text("\033[1m" + " ? " + "\033[0m", (0,0,0), (203, 203, 0))
                        else:
                            str += "   "
                    else:
                        if visited and room in visited:
                            age = moves - visited[room][1]
                            tail_length = 10
                            if age < tail_length:
                                str += truecolor.fore_text("\033[1m" +f"{room.id}".zfill(3), self.tail_color)
                            else:
                                str += truecolor.fore_text("\033[1m" +f"{room.id}".zfill(3), self.room_color)
                            # str += truecolor.fore_text(f"{room.id}".zfill(3), (100, min(40 + (visited[room] * 50), 254),
                            #                                                    min(180 + visited[room] * 50, 254)))
                            # str += truecolor.fore_text(f"{room.id}".zfill(3), (max(255 - (moves - visited[room][1])
                            #                                                             * 10,90), 190, min(200 + (visited[room][0] * 10), 254)))
                        else:
                            str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                # if room is not None and room.e_to is not None:
                if (((not visited and room is not None) or (visited and room in visited)) and room.e_to is not None):
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if (((not visited and room is not None) or (visited and room in visited)) and room.s_to is not None):
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
        print(str)
        print("#####")


