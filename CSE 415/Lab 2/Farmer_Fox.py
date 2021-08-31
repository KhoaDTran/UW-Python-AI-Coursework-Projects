'''Farmer_Fox.py
by Khoa Tran
UWNetID: ktdt01
Student number: 1861460

Assignment 2, in CSE 415, Winter 2021.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''
#<METADATA>
SOLUZION_VERSION = "1.0"
PROBLEM_NAME = "Farmer_Fox"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['K. Tran']
PROBLEM_CREATION_DATE = "21-JAN-2021"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC=\
 '''This is a problem deals with the Farmer Fox Chicken Grain complication
 as the farmer has to find a way to move the chicken fox and grain from the left side of the 
 river to the right side, without having the chicken and grain being together, and the fox and the
 chicken being together.
'''
#</METADATA>

#<COMMON_CODE>
Fa=0  # index to access Farmer
Fo=1  # index to access Fox
Ch=2 # index to access Chicken
Gr=3 # index to access Grain
LEFT=0 # index for left side of river
RIGHT=1 # index for right side of thee river

class State():
    def __init__(self, d=None):
        if d==None: 
            d = [0, 0, 0, 0]
        self.d = d

    def __eq__(self, s2):
        if self.d == s2.d:
            return True
        return False
    
    def __str__(self):
        # Produces a textual description of a state.
        text = ""
        if self.d[Fa] == RIGHT:
            text += "\n Farmer on right side of river \n"
        else:
            text += "\n Farmer on left side of river \n"
        if self.d[Fo] == RIGHT:
            text += "\n Fox on right side of river \n"
        else:
            text += "\n Fox on left side of river \n"
        if self.d[Ch] == RIGHT:
            text += "\n Chicken on right side of river \n"
        else:
            text += "\n Chicken on left side of river \n"
        if self.d[Gr] == RIGHT:
            text += "\n Grain on right side of river \n"
        else:
            text += "\n Grain on left side of river \n"
        return text
    
    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State({})
        temp = self.d.copy()
        news.d = temp
        return news

    def can_move(self, obj):
        '''Tests whether it's legal to perform the move to the given object.'''
        # Check for object and farmer on same side of river
        if obj != Fa:
            if self.d[Fa] != self.d[obj]:
                return False
        # Check for chicken and grain not being together
        if (obj == Fo) and (self.d[Gr] == self.d[Ch]):
            return False
        # Check for fox and chicken not being together
        elif (obj == Gr) and (self.d[Fo] == self.d[Ch]):
            return False
        # Check for same conditions as the two above but for moving the farmer
        elif (obj == Fa) and ((self.d[Fo] == self.d[Ch]) or (self.d[Gr] == self.d[Ch])):
            return False
        return True
    
    def move(self, obj):
        '''Assuming it's legal to make the move, this computes
        the new state.'''
        news = self.copy()
        if self.d[Fa] == 1:
            news.d[Fa] = 0
        else:
            news.d[Fa] = 1

        if obj != 0:
            if self.d[obj] == 1:
                news.d[obj] = 0
            else:
                news.d[obj] = 1
        return news
    
def goal_test(s):
    '''s is a goal state if all items are on the right side of river'''
    if 0 in s.d:
        return False
    return True

def goal_message(s):
    return "Congratulations on avoiding illegal moves and transfering the fox, chicken, and grain to the right side of the river!"
             
class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)
#</COMMON_CODE>

#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State(d = [0,0,0,0])
#</INITIAL_STATE>

#<OPERATORS>
MC_combinations = [0, 1, 2, 3]

OPERATORS = [Operator(
  "Cross the river with " + str(item),
  lambda s, m1=item: s.can_move(m1),
  lambda s, m1=item: s.move(m1)) 
  for item in MC_combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>