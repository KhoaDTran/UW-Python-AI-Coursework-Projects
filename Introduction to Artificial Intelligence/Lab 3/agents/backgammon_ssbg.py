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
        self.maxply = 2
        self.evalfunc = self.staticEval

    # returns a string representing a unique nick name for your agent
    def nickname(self):
        return "ktdt01"

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. If maxply==-1,
    # no limit is set
    def setMaxPly(self, maxply=-1):
        self.maxply = maxply

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        if (func is not None):
            self.evalFunc = func

    def initialize_move_gen_for_state(self, state, who, die1, die2):
        self.move_generator = self.GenMoveInstance.gen_moves(
            state, who, die1, die2)
    
    def get_all_possible_moves(self):
        """Uses the mover to generate all legal moves."""
        move_list = []
        done_finding_moves = False
        any_non_pass_moves = False
        while not done_finding_moves:
            try:
                m = next(self.move_generator)    # Gets a (move, state) pair.
                # print("next returns: ",m[0]) # Prints out the move.    For debugging.
                if m[0] != 'p':
                    any_non_pass_moves = True
                    move_list.append(m)    # Add the (move, state) pair to the list.
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:
            move_list.append('p')
        return move_list

    def useUniformDistribution():
        pass

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move
    def move(self, state, die1=1, die2=6):
        best_move, _ = self.expected_minimax(state, die1, die2, self.maxply)
        return best_move

    # Given a state and a roll of dice, returns the value of the best move for the
    # the state.whose_move
    def expected_minimax(self, state, die1=1, die2=6, plyLeft=2):
        agent = state.whose_move
        self.initialize_move_gen_for_state(state, state.whose_move, die1, die2)
        move_list = self.get_all_possible_moves()
        if move_list[0] == 'p':
            return 'p', self.staticEval(state)
        result_move = move_list[0]
        num = 0
        for item in move_list:
            if agent == R:
                num = math.inf
            else:
                num = -math.inf
            score = self.expected_helper(item[1], plyLeft - 1)
            if (score < num and agent == R) or (score > num and agent == W):
                num = score
                result_move = item[0]
        return result_move, num

    # Given a state, returns the score value of the state over the uniform distribution
    # of dice rolls
    def expected_helper(self, state, plyLeft=2):
        score = 0
        if plyLeft == 0:
            return self.staticEval(state)
        for die1 in range(1, 6 + 1):
            for die2 in range(1, 6 + 1):
                _, expected = self.expected_minimax(state, die1, die2, plyLeft)
                score += expected

        return score / 36

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
