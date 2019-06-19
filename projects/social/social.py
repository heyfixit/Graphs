from random import shuffle
import sys
sys.path.insert(0, '../graph')
from util import Stack, Queue  # These may come in handy

"""
# 3. Questions

1. To create 100 users with an average of 10 friends each,
how many times would you need to call `addFriendship()`? Why?

You'll need to call addFrindship 500 times since each time you call it,
a friend is added to each user's list. You need 1000 ids total in users' friends lists.

2. If you create 1000 users with an average of 5 random friends
each, what percentage of other users will be in a particular user's
extended social network? What is the average degree of separation between
a user and those in his/her extended network?

From experimentation, it seems like with 5 steps in a social graph, each user will have
will have every other user in their social graph.

Average degree of separation seems to be between 5 and 6.


"""

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.lastID = 0
        self.users = {}
        self.friendships = {}

    def addFriendship(self, userID, friendID):
        """
        Creates a bi-directional friendship
        """
        if userID == friendID:
            print("WARNING: You cannot be friends with yourself")
        elif friendID in self.friendships[userID] or userID in self.friendships[friendID]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[userID].add(friendID)
            self.friendships[friendID].add(userID)

    def addUser(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.lastID += 1  # automatically increment the ID to assign the new user
        self.users[self.lastID] = User(name)
        self.friendships[self.lastID] = set()

    def populateGraph(self, numUsers, avgFriendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.lastID = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME
        # Add users
        for i in range(numUsers):
            self.addUser(f"User{i}")

        # Create friendships
        num_friendships = (numUsers * avgFriendships) // 2

        possible_friendships = []

        # generate possible friendships where id1 < id2
        for id1 in range(1, numUsers):
            for id2 in range(id1 + 1, numUsers):
                possible_friendships.append((id1, id2))

        shuffle(possible_friendships)

        for i in range(0, num_friendships):
            self.addFriendship(possible_friendships[i][0], possible_friendships[i][1])







    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        if userID not in self.friendships:
            return visited
        # !!!! IMPLEMENT ME

        # create a queue
        q = Queue()

        # add the current user to the queue
        # keeping track of paths, so this queue will contain sets
        q.enqueue([userID])

        while q.size() > 0:

            # dequeue the first path
            path = q.dequeue()

            # the userID being inspected is the last element in the list
            f = path[-1]

            # if we haven't visited this userID
            if f not in visited:

                # consider it visited
                # store the path as the shortest route
                # to this person from the given userID
                visited[f] = path

                # queue this user's friends
                for friend in self.friendships[f]:

                    # for each friend copy the path we're at
                    path_copy = list(path)
                    # add the friend's ID to the end of the new path
                    path_copy.append(friend)

                    # queue up the new friend path for inspection
                    q.enqueue(path_copy)


        return visited


if __name__ == '__main__':
    # sg = SocialGraph()
    # sg.populateGraph(10, 2)
    # print(sg.friendships)
    # connections = sg.getAllSocialPaths(1)
    # print(connections)
    sg = SocialGraph()
    sg.populateGraph(1000, 5)
    connections = sg.getAllSocialPaths(1)
    print(len(connections))
    # sum_lengths = 0
    # for sp in connections:
    #     sum_lengths += len(connections[sp])
    # print(sum_lengths / len(connections))
