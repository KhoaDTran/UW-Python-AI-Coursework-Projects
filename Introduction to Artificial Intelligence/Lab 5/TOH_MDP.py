'''TOH_MDP.py
V9 Feb. 10, 2021, S. Tanimoto

This file defines a Markov Decision Process that uses the
states of a Towers-of-Hanoi puzzle, as well as its operators,
but which adds the following:

1. A set of actions.

2. general uncertainty in the effects of actions ("noise").
 
3. A specific probability distribution for each (s,a) pair,
over the set of possible new states s'.
This is implemented as the function T(s,a,sp) # sp = s'.

4. A reward function that maps each transition (s, a, sp)
to a real number. This is implemented as
  R(s, a, sp).

5. A discount factor gamma.  This can easily be changed, in order
to experiment with it.

Included is an "engine" for simulating the effects of actions in the
TOH microworld.

Most menu commands coming from the GUI implemented in Vis_TOH_MDP.py
are handled here in a function called MDP_command.

This version adds support for displaying the golden path (solution path).
Version 0.7b fixed an error when selecting Use Exploration Function on the menu.)
 
As in other recent versions, this version includes hooks to run a script
and for doing comparisons of the results of Q-Learning with results of
Value Iteration.

'''

import ValueIteration as VI
import Q_Learn as Q_Learn

from TowersOfHanoi import *
import TowersOfHanoi

Compare_QLearn_to_VI = False
try:
  import Compare_QLearn_to_VI
except: pass

TITLE = "TOH World: A Markov Decision Process for the Towers of Hanoi Puzzle"
ACTIONS = [op.name for op in OPERATORS] + ['Exit']
STATES_AND_EDGES = None
NOISE = 0.2
NGOALS = 1
LIVING_REWARD = 0
GAMMA = 0.9
ALPHA = 0.1
EPSILON = 0.1
NEED_Q_LEARN_SETUP = True
QUIET_MODE= False # Used during long Q-learning runs.

CLOSED = None
def generate_all_states():
  '''Basically create an explicit representation of the state-space
  graph by creating a hash that maps states to their adjacency lists,
  where each item on the adjacency list is an item of the form
  [operator_number, new_state]
'''
  global STATES_AND_EDGES, CLOSED
  # do special breadth-first search to generate all states and
  # their edges.
  STATES_AND_EDGES = {}
  initial_state = CREATE_INITIAL_STATE()
# STEP 1. Put the start state on a list OPEN
  OPEN = [initial_state]
  CLOSED = []
  COUNT = 0
  #BACKLINKS[initial_state] = None

# STEP 2. If OPEN is empty, output “DONE” and stop.
  while OPEN != []:

# STEP 3. Select the first state on OPEN and call it S.
#         Delete S from OPEN.
#         Put S on CLOSED.
#         If S is a goal state, output its description
    S = OPEN.pop(0)
    CLOSED.append(S)

    if GOAL_TEST(S):
      #print(GOAL_MESSAGE_FUNCTION(S))
      #path = backtrace(S)
      #print('Length of solution path found: '+str(len(path)-1)+' edges')
      #return
      pass
    COUNT += 1

# STEP 4. Generate the list L of successors of S and delete 
#         from L those states already appearing on CLOSED.
    L = []
    adj_lst = []
    for idx, op in enumerate(OPERATORS):
      if op.precond(S):
        new_state = op.state_transf(S)
        adj_lst.append((idx, new_state))
        if not (new_state in CLOSED):
          L.append(new_state)
          #BACKLINKS[new_state] = S
    STATES_AND_EDGES[S]=adj_lst

# STEP 5. Delete from L any members of L that occur on OPEN.
#         Insert all members of L at the front of OPEN.
    for s2 in OPEN:
      for i in range(len(L)):
        if (s2 == L[i]):
          del L[i]; break

    OPEN = OPEN + L
    #print_state_list("OPEN", OPEN)
# STEP 6. Go to Step 2.

GOAL2 = None
def compute_GOAL2():
    global GOAL2, N_disks
    GOAL2 = State({'peg1':[N_disks], 'peg2':[], 'peg3':list(range(N_disks-1,0,-1))})
    print("GOAL2 = "+str(GOAL2))

def goal_test2(s):
  global GOAL2
  return s==GOAL2

def is_valid_goal_state(s):
  if goal_test(s): return True
  if NGOALS==2 and goal_test2(s): return True
  return False

Terminal_state = State({'peg1':[],'peg2':[],'peg3':[]}) # The "Terminal" state
# consists of 3 pegs with NO disks.

ALL_STATES = None
#Q_VALUES = {}
Q_from_VI = {}
Q_from_QL = {}
V_from_VI = {}
V_from_QL = {}
POLICY_from_VI = {}
POLICY_from_QL = {}

GOLDEN_PATH = []
SILVER_PATH = []
def T(s, a, sp):  # Here is the heart of the MDP: its transition model.
  '''The typical action is associated with one operator, and with the noise
  at 20% it has an 80% chance of having its effect produced by that operator.
  It has a 20% chance of "noise" which means all other possible next
  states (except Exit) operators share evenly in that probability.
  The Exit operator is the only allowable operator in the goal state(s).
  When a non-applicable operator is chosen by the agent, the effect will
  be 80% no-op (but living reward is taken), and a 20% chance that one of
  the applicable ops will be chosen (2 or 3)

  IF no noise: Every applicable operator has its effect, and
  Every non applicable operator is a no-op.

  If noise, an action has 0.8 chance of it being applied and 0.2 chance
  that some other state is chosen at random from the set of remaining
  sucessors and the current state.  
  '''
  #print("Computing T(s,a,sp) for s="+str(s)+"; a='"+a+"; sp="+str(sp))
# Handle goal state transitions first...
  if is_valid_goal_state(s):
    if a=="Exit" and sp == Terminal_state: return 1.0
    else: return 0.0
    
#  if goal_test(s):
#    if a=="Exit" and sp == Terminal_state: return 1.0
#    else: return 0.0
#  elif NGOALS==2 and goal_test2(s):
#    if a=="Exit" and sp == Terminal_state: return 1.0
#    else: return 0.0

  if a=="Exit": return 0 # Exit action not allowed anywhere else.

# What are the normally applicable operators for s?
  applicables = [op for op in OPERATORS if op.is_applicable(s)]
  nonapplicables = [op for op in OPERATORS if not op.is_applicable(s)]
# Find the resulting state for each.
  poss_new_states = [op.state_transf(s) for op in applicables] + [s]
# Prob. is 0.8 if action and new state match.
  for i in range(len(applicables)):
    if a == applicables[i].name and sp== poss_new_states[i]:
      return 1.0 - NOISE
  for i in range(len(nonapplicables)): # Case of an action serving as a no-op.
    if a == nonapplicables[i].name and sp==s:
      return 1.0 - NOISE
# What is a next state's share of the noise?
  napplicables = len(applicables)
  if napplicables==0: return 0
  noise_share = NOISE / napplicables
# Handle remaining
  if sp in poss_new_states:
    return noise_share
# Otherwise, we must be looking at a state sp not near s.  
  return 0.0

def R(s, a, sp):
  '''Rules: Exiting from the correct goal state yields a
  reward of +100.  Exiting from an alternative goal state
  yields a reward of +10.
  The cost of living reward is -0.1.
  '''
# Handle goal state transitions first...
  if goal_test(s):
    if a=="Exit" and sp == Terminal_state: return 100.0
    else: return 0.0
  elif NGOALS==2 and goal_test2(s):
    if a=="Exit" and sp == Terminal_state: return 10.0
    else: return 0.0
# Handle all other transitions:
  return LIVING_REWARD

def initialize_V_from_VI(v):
  '''Get ready for Value Iteration. Normally all V are set to 0.'''
  global V_from_VI, ALL_STATES
  if not ALL_STATES: print("In initialize_V_from_VI, ALL_STATES is None.")
  V_from_VI = {}
  for s in ALL_STATES:
    V_from_VI[s]=v

def initialize_V_from_QL(v):
  '''Get ready for Value Iteration. Normally all V are set to 0.'''
  global V_from_QL, ALL_STATES
  if not ALL_STATES: print("In initialize_V_from_VI, ALL_STATES is None.")
  V_from_QL = {}
  for s in ALL_STATES:
    V_from_QL[s]=v

LAST_REWARD = None
Agent_state = None
TERMINATED = None
def initialize_episode():
  global LAST_REWARD, TERMINATED, Agent_state
  LAST_REWARD = 0
  Agent_state = ALL_STATES[0]
  TERMINATED = False
  Q_Learn.set_starting_state(Agent_state)

import time
def Agent_turn(a, reset=False):
    global Agent_state, Terminal_state, LAST_REWARD, TERMINATED
    #print("Entering Agent_turn")
    if reset:
      if not QUIET_MODE:
        print("Putting the Agent back at the initial state.")
      New_Agent_state = CLOSED[0]
      # Set the old one to something bogus, so comparison code below
      # will detect the difference.
      Agent_state = Terminal_state
      TERMINATED=False # Ready for a new episode
    else:
      if not QUIET_MODE: print("Agent is transitioning to ...")
      try:
        (New_Agent_state, r) = simulate(Agent_state, a)
      except Exception as e:
        print("Illegal action: "+str(a)+" in Agent_turn.")
      if not QUIET_MODE:
          print(str(New_Agent_state))
          print("Received reward "+str(r))
      LAST_REWARD = r
      # If no state change happened, don't alter highlighting.
      if Agent_state==New_Agent_state:
          if not QUIET_MODE:
              time.sleep(0.1) # And don't wait so long.
          return
      if not QUIET_MODE:
        Vis.unhighlight(Agent_state)
        Vis.highlight(New_Agent_state)
      Agent_state = New_Agent_state
    if Agent_state==Terminal_state:
        TERMINATED = True
        if not QUIET_MODE:
            Vis.highlight(New_Agent_state)
        Agent_state = New_Agent_state
    Vis.set_driving_console_status(allow_exit_only=(is_valid_goal_state(Agent_state)))
    if not QUIET_MODE:
      time.sleep(0.25) # Quarter second pause between moves of the agent.

def run_Agent(param):
    '''Run the agent for several transitions, depending on
    the value of param.  It uses the policy from VI.
    Return True if more turns can still be taken.'''
    global Agent_state, Terminal_state
    for i in range(param):
        if Agent_state==Terminal_state:
          print("Terminal state reached!")
          return False
        a = VI.apply_policy(Agent_state)
        Agent_turn(a)
    return True

def run_QL_agent(param, action=None):
    '''Return True if more turns can still be taken.'''
    global TERMINATED
    #print("In run_QL_agent, action = "+action)
    global Agent_state, Terminal_state
    for i in range(param):
        if Agent_state==Terminal_state:
          print("Terminal state reached!")
          TERMINATED = True
          return False
        if action:
          a = action
        else:
          a = VI.apply_policy(Agent_state) # Should prob. use a different policy method.
        Agent_turn(a)
        #print("Need to perform a Q update here.")
    return True

VI_POLICY = None
QL_POLICY = None

try:
  import script_for_TOH_MDP as script
  # Hook for optional "scripting via a special menu item on the File
  # menu that shows up if this file is in the same folder.
except: pass

n_iterations = 0
#from threading import Thread
def MDP_command(cmd, param):
  global GAMMA, ALL_STATES, CLOSED
  global ACTIONS, NOISE, LIVING_REWARD, NGOALS, SILVER_PATH, N_disks
  global V_from_VI, Q_from_VI, V_from_QL, Q_from_QL, POLICY_from_VI, POLICY_from_QL
  global Agent_state, n_iterations, NEED_Q_LEARN_SETUP, LAST_REWARD, TERMINATED, Terminal_state
  global ALPHA, EPSILON, QUIET_MODE
  #print("In MDP_command, cmd = "+cmd+"; param = "+str(param))
  if cmd=="NDISKS":
    N_disks = param
    TowersOfHanoi.N_disks = param
    try:
        Vis.unhighlight(Agent_state)
    except: pass
    set_up_state_space()
    return
  if cmd=="noise":
    NOISE = param
  if cmd=="ngoals":
    NGOALS = param
    if NGOALS==2: SILVER_PATH=make_solution_path(path_type="silver")
    else: SILVER_PATH = []

  if cmd=="living_reward":
    LIVING_REWARD = param
  if cmd=="set_gamma":
    GAMMA = param
    update_qlearn_params()
    return

  if cmd=="show_values":
    if param==1:
      Vis.display_values(V_from_VI)
      #for s in V_from_VI.keys(): Vis.reshow_state(s,V_from_VI[s])

    if param==2: Vis.show_q_values(Q_from_VI, CLOSED); #Vis.reshow_all_q_values(Q_from_VI, CLOSED)

    if param==3:
      compute_V_from_QL()
      Vis.display_values(V_from_QL)
      #for s in V_from_QL.keys(): Vis.reshow_state(s,V_from_QL[s])

    if param==4: Vis.show_q_values(Q_from_QL, CLOSED); #Vis.reshow_all_q_values(Q_from_QL, CLOSED)
    return
  if cmd=="Value_Iteration":
    if param==0:   # Reset VI state values to 0.
      n_iterations = 0
      initialize_V_from_VI(0)
      init_q_values(Q_from_VI)
      if Vis.DISPLAY_VALS_VAR.get()==1:
        Vis.display_values(V_from_VI)
      elif Vis.DISPLAY_VALS_VAR.get()==2:
         Vis.show_q_values(Q_from_VI, CLOSED)
      Vis.enable_value_iteration(True)
      Vis.enable_vi_action_menu_items(False)
      update_policy_displays(which="VI")
      return
    if param==1:
      (V_from_VI, max_delta) = VI.one_step_of_VI(ALL_STATES, ACTIONS, T, R, GAMMA, V_from_VI.copy())
      n_iterations += 1
      print("After "+str(n_iterations)+" iterations, max_delta = "+str(max_delta))
      Vis.enable_policy_extraction(True)
      Q_from_VI = VI.return_Q_values(CLOSED, ACTIONS)
      update_policy_displays(which="VI")
    if param > 1:
      for i in range(param):
        (V_from_VI, max_delta) = VI.one_step_of_VI(ALL_STATES, ACTIONS, T, R, GAMMA, V_from_VI.copy())
        n_iterations += 1
        print("After "+str(n_iterations)+" iterations, max_delta = "+str(max_delta))
        if max_delta < 0.00000001:
          print("VI has converged after iteration "+str(n_iterations)+".")
          break
      Vis.enable_policy_extraction(True)
      Q_from_VI = VI.return_Q_values(CLOSED, ACTIONS)
      update_policy_displays(which="VI")
    # Update the display of values or q-values, whichever is enabled currently.
    mode=Vis.DISPLAY_VALS_VAR.get()
    if mode==1:
      for s in V_from_VI.keys():
         Vis.reshow_state(s,V_from_VI[s])
    if mode==2:
      Vis.show_q_values(Q_from_VI, CLOSED)
      return
  if cmd=="Show_Policy_from_VI":   # THIS CMD SHOULD ACTUALLY BE UNNECESSARY NOW.
      update_policy_displays(which="VI")
  if cmd=="Show_Policy_from_QL":   # THIS CMD SHOULD ACTUALLY BE UNNECESSARY NOW.
      update_policy_displays(which="QL")
  if cmd=="Agent":
    if param==0 or Agent_state==Terminal_state:
      Vis.unhighlight(Agent_state)
      Agent_turn(ACTIONS[0], reset=True)
      initialize_episode()
    elif param==1:
      a = VI.apply_policy(Agent_state)
      Agent_turn(a)      
    else:
      Vis.TK_Canvas.after(10, lambda: run_Agent(param))
  if cmd=="QLearn":
    init_Q_Learn_if_needed()
    if param==-1 or Agent_state==Terminal_state: # Reset the agent to s0, ready for a new episode.
      Vis.unhighlight(Agent_state)
      Agent_turn(ACTIONS[0], reset=True)
      initialize_episode()
    elif param==-2:
      # Reset all state and Q values to 0.
      init_q_values(Q_from_QL, QL=True)
      initialize_V_from_QL(0)
      #Vis.reshow_all_q_values(Q_from_QL, CLOSED)
      if Vis.DISPLAY_VALS_VAR.get()==3:
         compute_V_from_QL()
         Vis.display_values(V_from_QL)
         return
      if Vis.DISPLAY_VALS_VAR.get()==4:
         Vis.show_q_values(Q_from_QL, CLOSED)
      update_policy_displays(which="QL")
      return
    elif param==0:
      user_drives_agent_via_text_input()
#    elif param==1:
#      a = Q_Learn.choose_next_action(Agent_state, LAST_REWARD, TERMINATED)
#      Agent_turn(a)
#      increment_transition_count()
    elif param>0: # Perform up to n transitions of Q learning. 
      for i in range(param):
        a = Q_Learn.choose_next_action(Agent_state, LAST_REWARD, TERMINATED)
        Agent_turn(a)
        if TERMINATED:
          # Make one more call to the Q_Learn agent so it can do a q-update based
          # on the reward in going from a goal state to the Terminal_state.
          # The returned "action" a should be None, but probably does not matter.
          a = Q_Learn.choose_next_action(Agent_state, LAST_REWARD, TERMINATED)
          print("Sent final reward for this episode: R="+str(LAST_REWARD))
          print("Episode ended after transition "+str(get_transition_count()))
          increment_episode_count()
          print(str(get_episode_count())+" episodes so far in this Q-learning run.")
          TERMINATED = False # Make it easier to start the next set of transitions.
          break
        increment_transition_count()
      update_policy_displays(which="QL")
    elif param==-1000:
        # Do 1000 transitions as quickly as possible, using as many episodes
        # as needed.
      train_quietly(1000)
      update_policy_displays(which="QL")
      return
  if cmd=="Exploration":
      if Vis.EXPL_VAR.get():
        init_q_values(Q_from_QL)
        mode=Vis.DISPLAY_VALS_VAR.get()
        if mode==4:
          Vis.reshow_all_q_values(Q_from_QL)

        Q_Learn.setup(ALL_STATES, ACTIONS, Q_from_QL, update_q_value, is_valid_goal_state, Terminal_state, use_exp_fn=True )
        update_policy_displays(which="QL")
  if cmd=="alpha":
    if param==1:
      ALPHA = 0.1
    elif param==2:
      ALPHA = 0.2
    elif param==3:
      ALPHA = -1
    update_qlearn_params()
    return
  if cmd=="epsilon":
    if param==1:
      EPSILON = 0.1
    elif param==2:
      EPSILON = 0.2
    elif param==3:
      EPSILON = -1
    update_qlearn_params()
    return
  if cmd=="User_chose":
    init_Q_Learn_if_needed()
    a = param
    Agent_turn(a)
    increment_transition_count()
    Q_Learn.handle_transition(a, Agent_state, LAST_REWARD)
    update_policy_displays(which="QL")
  if cmd=="Get_Q_Values":
    return((ALL_STATES, Q_VALUES)) # Needs updating to refer to one of the types of Q values.
  if cmd=="compare":
    #Compare_QLearn_to_VI.receive_globals(globals())
    #Q_from_VI = VI.return_Q_values(CLOSED, ACTIONS)
    compute_V_from_QL()
    Compare_QLearn_to_VI.full_compare()
  if cmd=="Run_script":
    script.run(globals())
    update_policy_displays(which="both")
  if cmd=="show_golden_path":
    Vis.show_golden_path()
 
  #else: print("Unknown command: "+command+" with parameter: "+str(param))

def update_policy_displays(which="both"): # "VI" or "QL" or "both"
  # Check the boolean variables that control policy display, and
  # for each that is true, update and (re)show the corresponding policy.
  # This should be called whenever Q values might have changed from either
  # menu, but it's good to specify which, to avoid unnecessary work doing extra policy extraction.
  global POLICY_from_VI, POLICY_from_QL
  if Vis.VI_POLICY_VAR.get() and which!="QL":
      POLICY_from_VI=VI.extract_policy(CLOSED, ACTIONS)
      Vis.show_policy(POLICY_from_VI)
      Vis.enable_vi_action_menu_items(True)
  else:
      if not Vis.VI_POLICY_VAR.get() :
        Vis.clear_a_policy_display(0)
  if Vis.QL_POLICY_VAR.get() and which!="VI":
      POLICY_from_QL=Q_Learn.extract_policy(CLOSED, ACTIONS)
      #print("For debugging... POLICY_from_QL is: "); print(str(POLICY_from_QL))
      Vis.show_policy(POLICY_from_QL, policy_number=1, use_alt_segments=True, color="blue")
      #QL_POLICY = pi # save policy from Value Iteration to compare with VI_POLICY
      if POLICY_from_VI: compare_policies(POLICY_from_VI, POLICY_from_QL)
      Vis.enable_compare_menu_item(True)
  else:
    if not Vis.QL_POLICY_VAR.get():
       Vis.clear_a_policy_display(1)

def train_quietly(n_transitions, check_for_convergence=False):
      global QUIET_MODE, POLICY_from_VI, POLICY_from_QL, CLOSED, ACTIONS
      #if check_for_convergence!=False : POLICY_from_VI = VI.extract_policy(CLOSED, ACTIONS)
      Vis.unhighlight(Agent_state)
      QUIET_MODE = True
      for i in range(n_transitions):
        a = Q_Learn.choose_next_action(Agent_state, LAST_REWARD, TERMINATED)
        Agent_turn(a)
        #print("Now in state: "+str(Agent_state))
        if TERMINATED:
          # Make one more call to the Q_Learn agent so it can do a q-update based
          # on the reward in going from a goal state to the Terminal_state.
          # The returned "action" a should be None, but probably does not matter.
          a = Q_Learn.choose_next_action(Agent_state, LAST_REWARD, TERMINATED)
          #print("Episode ended after transition "+str(get_transition_count()))
          increment_episode_count()
          #print(str(get_episode_count())+" episodes so far in this Q-learning run.")
          Agent_turn(ACTIONS[0], reset=True) # Start a new episode to continue training
          initialize_episode()
          #print("Starting next episode")
        else:
          increment_transition_count()
          if check_for_convergence!=False:
              # Make sure policy from QL is based on latest update.
              POLICY_from_QL = Q_Learn.extract_policy(CLOSED, ACTIONS)

              if check_for_convergence(): break
          if i % 100 == 99: print(".", end='') # Show SOME progress, even though "silent".
      QUIET_MODE = False
      Vis.highlight(Agent_state)
      Vis.show_q_values(Q_from_QL, CLOSED)
      print(str(get_episode_count())+" episodes so far.")
      print("Transition count is now "+str(get_transition_count()))
      return get_transition_count()

CFS = ["Policy match on golden path",\
       "Policy match on all states",\
       "Policy match on silver path",\
       "State mean-squared error on golden path",\
       "State mean-squared error on all states",\
       "State mean-squared error on silver path",\
       "Q-value mean-squared error on golden path",\
       "Q-value mean-squared error on all states",\
       "Q-value mean-squared error on silver path",\
   ]
def train_until(criterion="Policy match on golden path", threshold=100, max_iterations=10000):
  # Make sure the imported functions can access the globals they need.
  #Compare_QLearn_to_VI.receive_globals(globals())
  # Create a lambda function that represents the convergence criterion.
  if criterion==CFS[0]:
    cf = lambda: Compare_QLearn_to_VI.compare_policies(state_subset=GOLDEN_PATH)[2]>=threshold
  elif criterion==CFS[1]:
    cf = lambda: Compare_QLearn_to_VI.compare_policies(state_subset=ALL_STATES)[2]>=threshold
  elif criterion==CFS[2]:
    cf = lambda: Compare_QLearn_to_VI.compare_policies(state_subset=SILVER_PATH)[2]>=threshold
  elif criterion==CFS[3]:
    cf = lambda: Compare_QLearn_to_VI.compare_state_vals(state_subset=GOLDEN_PATH)<=threshold
  elif criterion==CFS[4]:
    cf = lambda: Compare_QLearn_to_VI.compare_state_vals(state_subset=ALL_STATES)<=threshold
  elif criterion==CFS[5]:
    cf = lambda: Compare_QLearn_to_VI.compare_state_vals(state_subset=SILVER_PATH)<=threshold
  elif criterion==CFS[6]:
    cf = lambda: Compare_QLearn_to_VI.compare_q_vals(state_subset=GOLDEN_PATH)<=threshold
  elif criterion==CFS[7]:
    cf = lambda: Compare_QLearn_to_VI.compare_q_vals(state_subset=ALL_STATES)<=threshold
  elif criterion==CFS[8]:
    cf = lambda: Compare_QLearn_to_VI.compare_q_vals(state_subset=SILVER_PATH)<=threshold
  else:
    print("Unrecognized criterion function string: "+criterion)
    print("Use one of the following strings instead:")
    for s in CFS: print(s);
    return
    
  iter_no = train_quietly(max_iterations, check_for_convergence=cf)
  if cf():
    print("The convergence criterion has been satisfied at iteration "+str(iter_no))
  else:
    print("No convergence yet after "+str(iter_no)+" iterations.")
    
    
  


def simulate(s, a):
  '''Take a state s and action a, and figure out a new state sp and
  reward r, according to T and R.'''
  global NGOALS, Terminal_state
  # See if this is a goal state.  If so, force the Exit action.
  #if goal_test2(s):
  #  print("Got to a secondary goal.  NGOALS is "+str(NGOALS))
  if goal_test(s) or (NGOALS==2 and goal_test2(s)):
    return (Terminal_state, R(s, "Exit", Terminal_state))
  if a=='Exit': return (s, LIVING_REWARD) # This is not supposed to happen, but some
  # Q_Learn solutions might try it.
  # Next generate a random number in the range [0,1).
  rn = random.random()
  #print("rn="+str(rn))
  cum_prob = 0.0
  # Lazily generate possible next states and get their probabilities
  # under the action a from state s.
  # Add this prob into the cum_prob.
  # If cum_prob > rn, then accept this state as the outcome,
  # and get the corresponding reward.
  # The two most likely states are the "intended" state and the current state.
  # Do them first to minimize unnecessary computation.
  cum_prob += T(s, a, s)
  #print("cum_prob="+str(cum_prob))
  if cum_prob > rn:
    return (s, R(s, a, s))
  for op in OPERATORS:
    if op.is_applicable(s):
      sp = op.state_transf(s)
      cum_prob += T(s, a, sp)
      #print("cum_prob="+str(cum_prob))
      if cum_prob > rn:
        return (sp, R(s, a, sp))
  #print("cum_prob="+str(cum_prob))
  print("In TOH_MDP, simulate, no viable next state or reward were found for s=")
  print("  "+str(s)+", a="+a)
  return (s, 0) # Keeps the program running even if something was wrong.

import Vis_TOH_MDP as Vis
Vis.MDP_command = MDP_command  # Make callback generally available in imported module.
Vis.ACTIONS = ACTIONS # Also make actions available in the Vis module.

import random
def test_color_coding():
  # Make up values in the range [MIN_VAL, MAX_VAL). These two
  # parameters are imported from Vis_TOH_MDP.
  for s in STATES_AND_EDGES.keys():
    v = (random.random()*(Vis.MAX_VAL - Vis.MIN_VAL))+Vis.MIN_VAL
    Vis.reshow_state(s, v)

def user_drives_agent_via_text_input():
    print("Input d, e, w, a, z, or x to drive the agent in that direction, q for the exit action.")
    c = input("action: ")
    #if c=='!': break
    try:
      idx = "dewazxq".index(c)
      print("Index is: "+str(idx))
      a = ACTIONS[idx]
      print("Selected action is: "+a)
      Vis.TK_Canvas.after(10, lambda: run_QL_agent(1, a))
      increment_transition_count()
    except: print("Unrecognized action.  Retry ...")
    Vis.TK_Canvas.update_idletasks()
    
# The following code creates states and displays them.
# It also demonstrates how to show values on the states,
# draw a text label, and highlight a particular state.
def set_up_state_space():
  global ALL_STATES, CLOSED, Terminal_state, Agent_state, N_disks, STATES_AND_EDGES
  global NEED_Q_LEARN_SETUP, Q_from_VI, Q_from_QL
  global GOLDEN_PATH, SILVER_PATH, NGOALS
  make_goal_state()
  generate_all_states()
  ALL_STATES = CLOSED + [Terminal_state]
  #Agent_state = CLOSED[0] # Set the VI agent at the initial state.
  initialize_episode()

  GOLDEN_PATH = make_solution_path()
  if NGOALS==2: SILVER_PATH=make_solution_path(path_type="silver")
  else: SILVER_PATH = []
  Vis.basic_plot(STATES_AND_EDGES, N_disks, MDP_command, NGOALS,\
                 GOLDEN_PATH, SILVER_PATH)
#  Vis.display_stats('''There are no episodes or transitions yet,
#and epsilon = 0''')
  Vis.TOH_state_vis(Agent_state)
  Vis.enable_value_iteration(False)
  Vis.enable_policy_extraction(False)
  Vis.enable_compare_menu_item(False)
  Vis.enable_vi_action_menu_items(False)
  Vis.clear_any_vals_and_q_vals() # Here the arg. doesn't really matter.
  compute_GOAL2()
  NEED_Q_LEARN_SETUP = True
  #print("Initial state is "+str(Agent_state))
  initialize_V_from_VI(0)
  initialize_V_from_QL(0)
  init_q_values(Q_from_VI) # Prevent error msgs if updates are attempted early.
  init_q_values(Q_from_QL,QL=True) # Prevent error msgs if updates are attempted early.


def init_q_values(q_values,QL=False):
  global ALL_STATES, ACTIONS
  for s in ALL_STATES:
    for a in ACTIONS:
      sa_key = Vis.make_sa_key(s, a)
      q_values[sa_key]=0.0
  if QL:
    reset_transition_count()
    reset_episode_count()
  #print("did init_q_values()")

def compute_V_from_QL():
  # Q-learning does not require computing state values,
  # but we will need them for certain comparisons and
  # when the user wants to inspect them.
    global Q_from_QL, V_from_QL, CLOSED
    for s in CLOSED:
      # find max Q-val for this state.
      maxval = -1000000
      for a in ACTIONS:
        try:
          q = Q_from_QL[(s, a)]
          if q > maxval: maxval = q
        except: pass
      V_from_QL[s] = maxval
      
def update_q_value(s, a, value):
  global QUIET_MODE
  #sa_key=Vis.make_sa_key(s, a)
  #Q_VALUES[sa_key]=value
  if not QUIET_MODE:
    Vis.update_q_value(s, a, value)

def update_qlearn_params():
  global ALPHA, EPSILON, GAMMA
  global NEED_Q_LEARN_SETUP, ALL_STATES, ACTIONS, Q_from_QL
  if NEED_Q_LEARN_SETUP:
      Q_Learn.setup(ALL_STATES, ACTIONS, Q_from_QL,\
                    update_q_value, is_valid_goal_state,\
                    Terminal_state)
      Q_Learn.set_starting_state(ALL_STATES[0])
      NEED_Q_LEARN_SETUP = False

  Q_Learn.set_learning_parameters(ALPHA, EPSILON, GAMMA)

N_TRANSITIONS = 0
def reset_transition_count():
  global N_TRANSITIONS
  N_TRANSITIONS = 0

def increment_transition_count():
  global N_TRANSITIONS
  N_TRANSITIONS += 1

def get_transition_count():
  global N_TRANSITIONS
  return N_TRANSITIONS

N_EPISODES = 0
def reset_episode_count():
  global N_EPISODES
  N_EPISODES = 0

def increment_episode_count():
  global N_EPISODES
  N_EPISODES += 1

def get_episode_count():
  global N_EPISODES
  return N_EPISODES

def compare_policies(pi1, pi2):
  '''Find the percentage of matching entries.  Can be used to
  compare Value Iteration with Q Learning.'''
  nmatches = 0
  for s in CLOSED:
    try: 
      if pi1[s]==pi2[s]: nmatches += 1
    except: pass
  match_val = 100 * nmatches / len(CLOSED)
  print("The two policies match percentage is "+str(match_val))
  return match_val
  
def init_Q_Learn_if_needed():
  global NEED_Q_LEARN_SETUP, ALL_STATES, ACTIONS, Q_from_QL, update_q_value
  global is_valid_goal_state, Terminal_state
  if NEED_Q_LEARN_SETUP:
      Q_Learn.setup(ALL_STATES, ACTIONS, Q_from_QL, update_q_value, is_valid_goal_state, Terminal_state)
      Q_Learn.set_starting_state(ALL_STATES[0])
      update_qlearn_params()
      Vis.enable_QL_policy_item(True)
      NEED_Q_LEARN_SETUP = False
  
def set_all_parameters(ndisks=3, noise=0.2, ngoals=1, living_reward=0, gamma=1,\
                       alpha = 0.1, epsilon=0.1):
  '''This is a stub for a function that could support testing under conditions controlled
  programmatically --- say by an autograder --- including values of parameters that cannot
  be specified via the menus.'''
  pass

# The following function "solves" the puzzle to find the golden path or the
# silver path. These are used when comparing policies from Value Iteration and
# Q-Learning.
# The method of solution is specific to the Towers of Hanoi puzzle.  Based on
# parity of: the number of disks plus one if the path type is silver, this method
# keeps moving the little disk to the right (or to the left) on every even-numbered turn,
# starting with the first turn (turn 0).  Then on the odd moves, it makes the only allowable
# move that does NOT involve the little disk.  Eventually, it gets to one of the
# goal states.
def make_solution_path(path_type="golden"):
   print("Looking for the "+path_type+" path")
   parity = (N_disks + (path_type=="silver") + 1) % 2
   #print("parity = "+str(parity))
   s = CLOSED[0]
   path=[s]
   op_grp1 = [OPERATORS[i] for i in [0,2,4]] # ops that move leftwards. (1->3, 3->2, 2->1)
   op_grp2 = [OPERATORS[i] for i in [1,5,3]] # ops that move rightwards. (1->2, 2->3, 3->1)
   if parity:
     little_disk_ops = op_grp2; other_ops = op_grp1
   else:
     little_disk_ops = op_grp1; other_ops = op_grp2
   #print("OPERATOR names: "+str([op.name for op in OPERATORS]))
   # The follow dictionaries indicate, for each operator, what its source peg
   # and destination peg are.  This information is used to prevent selecting a
   # next operator that moves the disk that was just moved, which could get us into
   # an infinite loop.
   source_peg = {OPERATORS[i]:[1,1,3,3,2,2][i] for i in range(6)}
   destination_peg = {OPERATORS[i]:[3,2,2,1,1,3][i] for i in range(6)}
   #print("little_disk_ops:")
   #print([op.name for op in little_disk_ops])
   #print("other_ops:")
   #print([op.name for op in other_ops])
   its_time_to_move_little_disk = True
   little_disk_op_idx=0
   last_peg = 0
   while not is_valid_goal_state(s):
     if its_time_to_move_little_disk:
       op = little_disk_ops[little_disk_op_idx]
       little_disk_op_idx = (little_disk_op_idx + 1) % 3
       #print("Move the little disk:")
     else:
       for i in range(6):
         op = OPERATORS[i]
         #print("Considering op whose source peg is "+str(source_peg[op]))
         if source_peg[op]==last_peg:
           #print("Source peg of op same as last peg. op is: "+op.name)
           continue
         if op.is_applicable(s):
           break
     if source_peg[op]==last_peg:
       print("No more moves for this path; it's probably the path to the apex of the triangle.")
       return path
     #print("current op is: "+op.name)
     new_state = op.apply(s)
     last_peg = destination_peg[op]
     #print("last peg is "+str(last_peg))
     path.append(new_state)
     its_time_to_move_little_disk = not its_time_to_move_little_disk
     s = new_state
     #print(str(s))
   #print(path_type+" path is: ")
   #for s in path: print(str(s))
   return path
           
set_up_state_space()

def get_all_states():
  global ALL_STATES
  return ALL_STATES

def get_golden_path():
  global GOLDEN_PATH
  return GOLDEN_PATH

def get_silver_path():
  global SILVER_PATH
  return SILVER_PATH
      
def testT():
   '''This is a sort of unit test for the T function, which represents the
   transition model of the MDP.'''
   global CLOSED, OPERATORS, ACTIONS
   print("Entering testT")
   s1 = CLOSED[10]; print("s1 is "+str(s1))
   suc = [op.state_transf(s1) for op in OPERATORS if op.precond(s1)] + [s1]
   print("suc = "+str(suc))
   for a in ACTIONS:
     print("Considering action: "+a)
     for sp in suc:
       print("T(s1, "+a+", sp)=" + str(T(s1,a,sp)) + " where sp="+str(sp))

#testT()


