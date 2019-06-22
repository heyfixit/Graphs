class Player:
    def __init__(self, name, startingRoom):
        self.name = name
        self.currentRoom = startingRoom

        # start off with one visit on the starting room
        self.currentRoom.visits = 1
    def travel(self, direction, showRooms = False):
        nextRoom = self.currentRoom.getRoomInDirection(direction)
        if nextRoom is not None:
            self.currentRoom = nextRoom

            # increment the room's visits
            self.currentRoom.visits += 1
            if (showRooms):
                nextRoom.printRoomDescription(self)
        else:
            print("You cannot move in that direction.")
