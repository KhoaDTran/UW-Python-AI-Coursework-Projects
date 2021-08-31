'''
Name(s): Khoa Tran
UW netid(s): ktdt01@uw.edu
'''

from game_engine import genmoves
import math

W = 0
R = 1


class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.maxply = 3
        self.curr_state = None
        self.prune = False
        self.num_states = -1
        self.cutoffs = -1
        self.evalFunc = self.staticEval

    # returns a string representing a unique nick name for your agent
    def nickname(self):
        # TODO: return a string representation of your UW netid(s)
        return "ktdt01"

    # If prune==True, changes the search algorthm from minimax
    # to Alpha-Beta Pruning
    def useAlphaBetaPruning(self, prune=False):
        self.prune = prune
        self.num_states = 0
        self.cutoffs = 0

    # Returns a tuple containing the number explored
    # states as well as the number of cutoffs.
    def statesAndCutoffsCounts(self):
        return (self.num_states, self.cutoffs)

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. If maxply==-1,
    # no limit is set
    def setMaxPly(self, maxply=-1):
        self.maxply = maxply

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        if func is not None:
            self.evalFunc = func

    def initialize_move_gen_for_state(self, state, who, die1, die2):
        self.move_generator = self.GenMoveInstance.gen_moves(
            state, who, die1, die2)
    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move

    def move(self, state, die1=1, die2=6):
        result_move = None
        agent = state.whose_move
        self.initialize_move_gen_for_state(state, agent, die1, die2)
        move_list = self.get_all_possible_moves()
        if agent == R:
            num = math.inf
            for item in move_list:
                if not self.prune:
                    alpha = None
                    beta = None
                else:
                    alpha = -math.inf
                    beta = math.inf
                score = self.minimax(item[1], die1, die2, W, self.maxply, alpha, beta)
                if (num > score):
                    num = score
                    result_move = item[0]
        else:
            num = -math.inf
            for item in move_list:
                if not self.prune:
                    alpha = None
                    beta = None
                else:
                    alpha = -math.inf
                    beta = math.inf
                score = self.minimax(item[1], die1, die2, R, self.maxply, alpha, beta)
                if (num < score):
                    num = score
                    result_move = item[0]
        return result_move



    # Given a state, returns an integer which represents how good the state is
    # for the two players (W and R) -- more positive numbers are good for W
    # while more negative numbers are good for R
    def staticEval(self, state):
        barList = state.bar
        whiteOff = state.white_off
        redOff = state.red_off
        agent = state.whose_move
        count_red = 0
        count_white = 0
        count_white += (200 * len(whiteOff))
        count_red += (20 * len(redOff))
        if agent == R:
            count_red += 2
        elif agent == W:
            count_white += 2
        for item in barList:
            if (item == W):
                count_white -= 20
            else:
                count_red -= 20
        if genmoves.bearing_off_allowed(state, R):
            count_red += 40
        elif genmoves.bearing_off_allowed(state, W):
            count_white += 40
        
        return count_white - count_red
    
    def get_all_possible_moves(self):
        """Uses the mover to generate all legal moves. Returns an array of move commands"""
        move_list = []
        done_finding_moves = False
        any_non_pass_moves = False
        while not done_finding_moves:
            try:
                m = next(self.move_generator)    # Gets a (move, state) pair.
                # print("next returns: ",m[0]) # Prints out the move.    For debugging.
                if m[0] != 'p':
                    any_non_pass_moves = True
                    move_list.append(m)    # Add the move to the list.
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:
            move_list.append('p')
        return move_list

    def minimax(self, state, die1, die2, agent, plyLeft, alpha, beta):
        if (len(state.white_off) == 15 or len(state.red_off) == 15 or plyLeft == 0):
            return self.staticEval(state)
        who_move = 0
        if agent == R:
            who_move = W
        else:
            who_move = R
        self.num_states += 1
        self.initialize_move_gen_for_state(state, who_move, die1, die2)
        move_list = self.get_all_possible_moves()
        if move_list[0] == 'p':
            return self.staticEval(state)
        num = 0
        if agent == W:
            num = math.inf
            for item in move_list:
                score = self.minimax(item[1], die1, die2, R, plyLeft - 1, alpha, beta)
                if (num > score):
                    num = score
                if(alpha and beta):
                    beta = min(beta, score)
                    if beta <= alpha:
                        self.cutoffs += 1
                        break
            return num
        else:
            num = -math.inf
            for item in move_list:
                score = self.minimax(item[1], die1, die2, W, plyLeft - 1, alpha, beta)
                if (num < score):
                    num = score
                if(alpha and beta):
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        self.cutoffs += 1
                        break
            return num


