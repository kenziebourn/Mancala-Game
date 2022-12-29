class Mancala:
    """Mancala class representing the game as played. The class contains information about
    each of the players and the board."""

    def __init__(self):
        """Initializes a Mancala game object."""
        self._board = Board(num_pits=6, num_seeds=4)  #board object representing Mancala board
        self._players = {1: None, 2: None} #dictionary of player objects where keys correspond to player1 and player2 and values are the assigned names
        self._current = 1 #keeps track of which players turn it is

    def create_player(self, name):
        """takes one parameter of the player’s name as a string and returns the player object"""
        # If player 1 already added, add player 2.
        if self._players[1]:
            self._players[2] = Player(name)
        # Otherwise, add player 1.
        else:
            self._players[1] = Player(name)

    def print_board(self):
        """Prints the current board information """
        self._board.print_board()

    def return_winner(self):
        """Method to return winner of the game if the game is ended.
         It prints the winner in the following format:
            "Winner is player 1 (or 2, based on the actual winner): player’s name"
            If the game is a tie, return "It's a tie";
            If the game is not ended yet, return "Game has not ended"
        """
        # if not one of the players pits are all empty then game isn't over
        if not self._board.is_game_over():
            return "Game has not ended"

        # Otherwise report the winner or a tie
        winner = self._board.return_winner()
        if winner == 0:
            return "It's a tie"
        elif winner == 1:
            return f"Winner is player 1: {self._players[1].get_name()}"
        else:
            return f"Winner is player 2: {self._players[2].get_name()}"

    def play_game(self, player_index, pit_index):
        """Method which takes two parameters: player_index, pit_index
        and plays the game according to the rules of Mancala
        """
        # Checks for invalid pit index.
        if pit_index > 6 or pit_index < 1:
            return "Invalid number for pit index"

        # Play a round of the game according to the rules
        board = self._board
        board.play_turn(player_index, pit_index)

        # If the game is over, move any remaining seeds in the pits to their respective player store
        if self._board.is_game_over():
            self._board.final_total()
            return "Game is ended"
        # Otherwise, form the return list of seed and store seed values.
        seeds = board.get_pit_seeds(1) + [board.get_store_seeds(1)]   # Player 1 pits + store
        seeds += board.get_pit_seeds(2) + [board.get_store_seeds(2)]  # Player 2 pits + store
        return seeds


    def next_player(self):
        """switches between current players turn."""
        if self._current == 1:
            self._current = 2
        else:
            self._current = 1


class Player:
    """Player class representing a player's name"""
    def __init__(self, name):
        """Initializes a player object."""
        self._name = name #string representing name of player

    def get_name(self):
        """Returns the player name."""
        return self._name


class Board:
    """Board class representing the Mancala game board.
    The board is represented by a collection of containers that represent the pits
    and stores for player 1 and 2. Given the pit_index, we can traverse the board by
    moving in a counter-clockwise direction.
    A board is initialized with number of pits. The pits are initialized with an initial
    number of seeds.
    """
    def __init__(self, num_pits=6, num_seeds=4):
        """Initializes Board object."""
        self._num_pits = num_pits #represents the number of pits that the board contains
        self._num_seeds = num_seeds #represents the initial amount of seeds in each pit
        self._board = None #object represented by a nested dictionary where the first dict is player num 1 or 2 and the second is the Container class id value
        #either an integer between 1 and num_pits, or 'store'


        # Initializes the board setup
        self.setup_board()

    # Get methods
    def get_num_pits(self):
        """Returns the number of pits to setup the board with."""
        return self._num_pits

    def get_num_seeds(self):
        """Returns the number of seeds to seed the pits with."""
        return self._num_seeds

    def get_board(self):
        """Returns the board dictionary"""
        return self._board

    def get_pits(self, player):
        """returns the pits in consecutive order where player id is either 1 or 2 """
        return [item for item in self._board[player].values() if item.get_type() == "pit"]

    def get_pit_seeds(self, player):
        """returns the number of seeds in each pit, as a list where player id is either 1 or 2"""
        return [pit.get_seeds() for pit in self.get_pits(player)]

    def get_store_seeds(self, player):
        """returns the number of seeds in player id (1 or 2)'s store."""
        return self._board[player]['store'].get_seeds()

    def get_empty_pits(self, player):
        """returns a list of booleans representing if the pits are empty where player id is either 1 or 2"""
        return list(map(lambda x: True if x == 0 else False, self.get_pit_seeds(player)))

    def setup_board(self):
        """Sets up the Mancala board with appropriate number of pits and seeds.
        The board is represented by a chain of containers representing
        either the seed 'pit' or 'store'.
        """
        # Create player 1 store and pits.
        p1_store = Container('store', 1, 'store')
        p1_pits = [Container(i, 1, 'pit') for i in range(1, self.get_num_pits()+1)]

        # Create player 2 store and pits.
        p2_store = Container('store', 2, 'store')
        p2_pits = [Container(i, 2, 'pit') for i in range(1, self.get_num_pits()+1)]

        #create full game board by connecting the containers.
        for i in range(0, self.get_num_pits() - 1):
            p1_pits[i].set_next(p1_pits[i + 1])
            p2_pits[i].set_next(p2_pits[i + 1])

        #connect the ends of the stores and pits for player 1 and 2
        p1_pits[-1].set_next(p1_store)
        p1_store.set_next(p2_pits[0])
        p2_pits[-1].set_next(p2_store)
        p2_store.set_next(p1_pits[0])

        # Set the opposite pits
        # player2: 6 5 4 3 2 1
        # player1: 1 2 3 4 5 6
        for i in range(0, self.get_num_pits()):
            p1_pits[i].set_adjacent(p2_pits[self.get_num_pits()-1-i])
            p2_pits[i].set_adjacent(p1_pits[self.get_num_pits()-1-i])

        # Initialize all the pits with the specified number of seeds
        [pit.set_seeds(self.get_num_seeds()) for pit in p1_pits + p2_pits]

        # Creates board for the containers. Represent the board
        # with a nested dictionary, where the first level is player id (1 or 2), and
        # the second is the pit/store id.
        board = {1: {}, 2: {}}
        for pit in p1_pits:
            board[1][pit.get_id()] = pit
        for pit in p2_pits:
            board[2][pit.get_id()] = pit
        board[1]['store'] = p1_store
        board[2]['store'] = p2_store
        self._board = board

    def is_game_over(self):
        """method which returns a boolean representing whether the game is over.  The game is over when
         a player has zero seeds left in their pits."""
        for player in [1, 2]:
            if all(self.get_empty_pits(player)):
                return True
        return False

    def print_board(self):
        """prints the current board information in the following format:
    player1:
    store: number of seeds in player 1’s store
    player 1 seeds number from pit 1 to 6 in a list

    player2:
    store: number of seeds in player 2’s store
    player 2 seeds number from pit 1 to 6 in a list
        """
        print("player1:")
        print(f"store: {self.get_store_seeds(1)}")
        print(self.get_pit_seeds(1))

        print("player2:")
        print(f"store: {self.get_store_seeds(2)}")
        print(self.get_pit_seeds(2))



    def return_winner(self):
        """method to determine winner of Mancala game, returns either 1 or 2 for the winner,
        none if game is not over and 0 if it's a tie"""

        # Game not over
        if not self.is_game_over():
            return None

        # seed totals for each player = remaining seeds in their pits + seeds in their store
        player1_total = sum(self.get_pit_seeds(1)) + self.get_store_seeds(1)
        player2_total = sum(self.get_pit_seeds(2)) + self.get_store_seeds(2)

        # Return the winner
        if player1_total == player2_total:
            return 0 #tie

        elif player1_total > player2_total:
            return 1 #player1 wins

        else:
            return 2 #player2 wins

    def final_total(self):
        """method that determines final totals for each player by moving any seeds remaining in the pits to their respective
        player store."""

        # Access store value in nested dict
        p1_store = self._board[1]['store']
        p2_store = self._board[2]['store']

        # Add the remaining seeds in the pits to the stores.
        p1_store.add_seeds(sum(self.get_pit_seeds(1)))
        p2_store.add_seeds(sum(self.get_pit_seeds(2)))

        # Clear the seeds from the pits
        [p.clear_seeds() for p in self.get_pits(1)+self.get_pits(2)]

    def play_turn(self, player_id, pit_number):
        # check if either player 1 or 2 is chosen
        if player_id not in (1, 2):
            print("Invalid player number")
            return

        # check if valid pit number
        if not self.is_valid_pit(pit_number):
            print("Invalid number for pit")
            return

        # check if pit number is empty (no seeds)
        pit = self._board[player_id][pit_number]
        if pit.get_seeds() == 0:
            print("Invalid selection. Player must choose a non-empty pit.")
            return

        # Initialize traversal
        seed_count = pit.get_seeds()
        pit.clear_seeds()
        current = pit

        # while there's still remaining seeds to sow
        while seed_count > 0:

            # Gets the next seed
            current = current.get_next()

            #Special Rule 2: When the last seed in your hand lands in one of your own pits, if that pit had been empty you
            # get to keep all of the seeds in your opponents pit on the opposite side. Put those captured seeds,
            # as well as the last seed that you just played on your side, into the store.
            if seed_count == 1 and current.get_player() == player_id and current.get_type() == 'pit' \
                    and current.get_seeds() == 0:
                # Get the opposing player's pit.
                adjacent = current.get_adjacent()

                # Add the opposing and current seed to the player store.
                store = self._board[player_id]['store']
                store.add_seeds(adjacent.get_seeds() + 1)

                adjacent.clear_seeds() # Clear the seeds from the opposing pit.
                seed_count -= 1 # Decrement the current seed count.

            # Otherwise, sow the seed while skipping the opposing player's store
            elif not (current.get_player() != player_id and current.get_type() == 'store'):
                current.increment_seeds() # Increment the current container.
                seed_count -= 1 # Decrement the current seed count.

            # Special Rule 1: If last seed falls in the players own store, the player gets another turn
            if seed_count == 0 and current.get_player() == player_id and current.get_type() == 'store':
                print(f"player {player_id} take another turn")
                return 'skip'

    def is_valid_pit(self, num):
        """Check if pit input number is valid."""
        if num < 1 or num > self._num_pits:
            return False
        return True


class Container:
    """Container class representing a pit or store for a given player. Containers are connected
     to form an entire Mancala board such that one can iterate through the board recursively """

    def __init__(self, container_id, player_id, container_type):
        """Initializes a container."""
        self._id = container_id
        self._player = player_id
        self._type = container_type #string representing either 'store' or 'pit'
        self._seeds = 0     #represents number of seeds currently stored
        self._next = None   #Container object representing the next container (counter-clockwise)
        self._adjacent = None   #Container object representing opposing players pit

    # Get methods
    def get_id(self):
        """Returns the container id."""
        return self._id

    def get_player(self):
        """Returns the player id."""
        return self._player

    def get_type(self):
        """Returns the container type."""
        return self._type

    def get_seeds(self):
        """Returns the number of seeds."""
        return self._seeds

    def get_next(self):
        """Returns the next container."""
        return self._next

    def get_adjacent(self):
        """Returns the opposing container."""
        return self._adjacent

    # Set methods
    def set_seeds(self, num):
        """Sets the number of seeds."""
        self._seeds = num

    def add_seeds(self, num):
        """Adds the number of seeds to existing seeds"""
        self._seeds = self._seeds + num

    def set_next(self, nxt):
        """Sets the next node."""
        self._next = nxt

    def set_adjacent(self, adj):
        """Sets the adjacent node."""
        self._adjacent = adj

    def clear_seeds(self):
        """method to removes all the seeds currently stored"""
        self._seeds = 0

    def increment_seeds(self):
        """increments the number of seeds stored in the container by 1"""
        self._seeds += 1



