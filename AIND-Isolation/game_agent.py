"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def heuristic_one(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")    

    '''
    This heuristic focuses on the possibility of limiting future moves for the opponent. 
    Assign higher evaluation function score to the state if the possibility of future
    moves for the opponent is scarce, and assign lower score if that is not the case.
    So, we go ahead and put up a recursion, finding  length of set of all the legal moves
    from the current state, and then going on length of set of legal moves available to
    from each of those states. 

    '''        
    player_legal_moves = game.get_legal_moves(player)
    player_total_moves = len(player_legal_moves)

    for move in player_legal_moves:
        board = game
        board = game.forecast_move(move)
        player_total_moves += len(board.get_legal_moves())

    opp_legal_moves = game.get_legal_moves(game.get_opponent(player)) 

    opp_total_moves = len(opp_legal_moves)

    for move in opp_legal_moves:
        board = game
        board = game.forecast_move(move)
        opp_total_moves += len(board.get_legal_moves()) 
    
    '''The weight of 2 with the opposition legal moves means we are penalizing
    highly for a board state, where the opponent has more move at it's disposal.
    We will be inclined to choosing the board states in which the opponent is
    fairly limited in in it's movements.'''

    return(float(player_total_moves - 2*opp_total_moves))

def custom_score(game, player):
    '''This heuristic evaluates a board state two folds, first it scores the board
    on the number of moves available to the player, with respect to the available
    moves to the opponent, and if the player has more moves available than the
    opponent, then the board is assigned a higher score, else the board is penalized.
    This heuristic also goes ahead and normalizes the difference in moves with the
    manhattan distance between the player. Taking in account the fact that, if the
    manhattan distance between the player and the opponent is large, the player will
    find it hard, to be able to block the moves for the opponent, and hence in this
    case, the board will be penalized, else rewarded.  
    '''    
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    player_legal_moves = game.get_legal_moves(player)
    opp_legal_moves = game.get_legal_moves(game.get_opponent(player))

    '''The weight of 2 with the opposition legal moves means we are penalizing
    highly for a board state, where the opponent has more move at it's disposal.
    We will be inclined to choosing the board states in which the opponent is
    fairly limited in in it's movements.''' 
    difference_in_moves = len(player_legal_moves) - 2*len(opp_legal_moves)
    position_of_player = game.get_player_location(player)
    position_of_opponent = game.get_player_location(game.get_opponent(player))
    manhattan_distance = abs(position_of_player[0]-position_of_opponent[0]) +  abs(position_of_player[1]-position_of_opponent[1])

    return(float(difference_in_moves/float(manhattan_distance)))

def heuristic_three(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")    

    '''Inner square occupation heuristics, in this hueristics we evaluate the
    board state based on how many positions does the active player occupy in 
    the inner square of the game board, rewarding the states in which the active
    player occupies more center position, than the opponent, and penalizing the
    states in which the opponents occupies more position in inner square than
    the active player. We will also go ahead and ensemble it with the Manhatten
    distance, taking in account the fact that, if the active player occupies
    more inner square positions, and is closer to the opponent, he will be able
    to block moves for the opponent, and hence this board state will be 
    rewarded, and else it will be penalized.
    '''
    # Coordinates of position contained in inner square
    inner_square = [[2,1], [2,2], [2,3], [2,4],
                    [3,1], [3,2], [3,3], [3,4],
                    [4,1], [4,2], [4,3], [4,4]]
    
    player_one_count = 0
    player_two_count = 0
    not_occupied = 0
    for position in inner_square:
        if game.__board_state__[position[0]][position[1]] == 1:
                player_one_count += 1
        if game.__board_state__[position[0]][position[1]] == 2:
                player_two_count += 1                            
        else:
                not_occupied += 1

    position_of_player = game.get_player_location(player)
    position_of_opponent = game.get_player_location(game.get_opponent(player))
    manhattan_distance = abs(position_of_player[0]-position_of_opponent[0]) +  abs(position_of_player[1]-position_of_opponent[1])

    return((player_one_count - 5*(player_two_count + not_occupied))/float(manhattan_distance))

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        # Set of legal moves available to the current active player
        legal_moves = game.get_legal_moves()

        # If there are no legal moves available for the current player we can simple return
        # (-1, -1) without having to call minimax or alphabeta.

        if legal_moves == []:
            return((-1, -1))

        best_move = None

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            
            # Check if the method of tree search is 'minimax' or 'alphabeta'
            if self.method == 'minimax':
                # If the search method is 'minimax', check if self.iterative is True
                if self.iterative == True:
                    for depth in range(100):
                        _ , best_move = self.minimax(game, depth, maximizing_player=True)

                if self.iterative == False:
                    # If self.iterative is False, we can simply call the minimax method
                    # without implementing iterative deepening, and return the results
                    _ , best_move = self.minimax(game, self.search_depth, maximizing_player=True)    

            if self.method == 'alphabeta':    
                # If the search method is 'alphabeta', check if self.iterative is True
                if self.iterative == True:
                    for depth in range(100):
                        _ , best_move = self.alphabeta(game, depth, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
                if self.iterative == False:
                    # If self.iterative is False, we can simply call the minimax method
                    # without implementing iterative deepening, and return the results
                    _ , best_move = self.alphabeta(game, self.search_depth, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)                    

        
        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        return(best_move)

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

            
        legal_moves = game.get_legal_moves()

        # Two base cases for the problem will be when
        # the current note is the leaf not, which will be conditioned on the fact
        # whether there are any legal moves available or not

            # If there are no legal moves we can simply call the utility funtion
            # on the leaf node and return the utility scores

        if legal_moves == []:    
            return(game.utility(self), (-1, -1))

        # Second base condition for the recursion will be when desired depth is reached
        # that is when we reach to depth zero, we will just evaluate the current board state
        # using custom scoring funtion and return the score

        if depth == 0:
            # Simply call the custom score to evaluate the board and return the score
            return(self.score(game, self), (-1, -1))

        best_move = None

        # There can be two conditions depending on whether the player is the
        # maximizing player or the minimizing player, at a maximizing node
        # we will bubble up the maximum value of all the child nodes and at a 
        # minimizing node we will bubble up minimum value of all the nodes
        if maximizing_player == True:
                # The worst case score for maximizing player
                best_score = float('-inf')
                # Iterating over all the childnodes, and returning the one which
                # yields maximum score among all the child nodes(states), from the current
                # board state
                for move in legal_moves:
                    # forecast_move creates a deep copy of the game board, with 'move' 
                    # appled to the board
                    child_board = game.forecast_move(move)
                    score, _ = self.minimax(child_board, depth - 1, maximizing_player=False)
                    # Checks if score received after depth first recursion through this child
                    # node branch is more than the best score.
                    if score > best_score:
                        best_score = score
                        best_move = move

        if maximizing_player == False:    
                # The worst case score for minimizing player
                best_score = float('inf')
                # Iterating over all the childnodes, and returning the one which
                # yields maximum score among all the child nodes(states), from the current
                # board state
                for move in legal_moves:
                    # forecast_move creates a deep copy of the game board, with 'move' 
                    # appled to the board
                    child_board = game.forecast_move(move)
                    score, _ = self.minimax(child_board, depth - 1, maximizing_player=True)
                    # Checks if score received after depth first recursion through this child
                    # node branch is less than the best score.
                    if score < best_score:
                        best_score = score
                        best_move = move

        return(best_score, best_move)                

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        legal_moves = game.get_legal_moves()

        # Two base cases for the problem will be when
        # the current note is the leaf not, which will be conditioned on the fact
        # whether there are any legal moves available or not

            # If there are no legal moves we can simply call the utility funtion
            # on the leaf node and return the utility scores

        if legal_moves == []:    
            return(game.utility(self), (-1, -1))

        # Second base condition for the recursion will be when desired depth is reached
        # that is when we reach to depth zero, we will just evaluate the current board state
        # using custom scoring funtion and return the score

        if depth == 0:
            # Simply call the custom score to evaluate the board and return the score
            return(self.score(game, self), (-1, -1))

        best_move = None

        # There can be two conditions depending on whether the player is the
        # maximizing player or the minimizing player, at a maximizing node
        # we will bubble up the maximum value of all the child nodes and at a 
        # minimizing node we will bubble up minimum value of all the nodes
        if maximizing_player == True:
                # The worst case score for maximizing player
                best_score = float('-inf')
                # Iterating over all the childnodes, and returning the one which
                # yields maximum score among all the child nodes(states), from the current
                # board state
                for move in legal_moves:
                    # forecast_move creates a deep copy of the game board, with 'move' 
                    # appled to the board
                    child_board = game.forecast_move(move)
                    score, _ = self.alphabeta(child_board, depth - 1, alpha, beta, maximizing_player=False)
                    # Checks if score received after depth first recursion through this child
                    # node branch is more than the best score.
                    if score > best_score:
                        best_score = score
                        best_move = move

                    # Pruning the branch    
                    if best_score >= beta:    
                        return(best_score, best_move)

                    # Updating the values of alpha    
                    alpha = max(best_score, alpha)
                        
        if maximizing_player == False:    
                # The worst case score for minimizing player
                best_score = float('inf')
                # Iterating over all the childnodes, and returning the one which
                # yields maximum score among all the child nodes(states), from the current
                # board state
                for move in legal_moves:
                    # forecast_move creates a deep copy of the game board, with 'move' 
                    # appled to the board
                    child_board = game.forecast_move(move)
                    score, _ = self.alphabeta(child_board, depth - 1, alpha, beta, maximizing_player=True)
                    # Checks if score received after depth first recursion through this child
                    # node branch is less than the best score.
                    if score < best_score:
                        best_score = score
                        best_move = move

                    # Pruning the branch    
                    if best_score <= alpha:
                        return(best_score, best_move)

                    # Updating the value of beta    
                    beta = min(best_score, beta)        

        return(best_score, best_move)
