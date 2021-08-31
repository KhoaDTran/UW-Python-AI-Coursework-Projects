'''Vis_TOH_MDP.py
Version 9, S. Tanimoto, Feb. 10, 2021.

This provides a visualization, in Tkinter, for the Towers of Hanoi
state space.

It also supports displaying values in each state, and highlighting
  any one state at a time.
Facilities are here for showing Q-states, and user interaction via
menus and a "driving console" to directly controlling an agent
solving the puzzle.

'''

import Q_Learn as Q_Learn

import tkinter as tk
WIDTH = 650
HEIGHT = 650
TITLE = "TOH World: A Markov Decision Process for the Towers of Hanoi (C) Univ. of Wash. CSE, 2018"
R = 20 # radius for state circles. OK when NDISKS = 3.
MAX_VAL = 100.0
MIN_VAL = -100.0

# Containers for Tk canvas items:
CIRCS = []
EDGE_LINES = []
PI_LINES = []
STATES_TO_LABELS = {}

CONSOLEVAR = None; COMPARE_VAR = None

VI_MENU = None
VI_AGENT_MENU = None
QLEARN_MENU = None
TK_Canvas = None

SEGMENTS = []
SEGMENTS_FOR_POLICY_0 = []
SEGMENTS_FOR_POLICY_1 = []
NOISE_VAR=None; NGOALS_VAR=None; GOLDEN_PATH_VAR=None; R_VAR=None; G_VAR=None
DISPLAY_VALS_VAR=None; Q_VAR=None; EPSILON_VAR=None; EXPL_VAR=None
VI_POLICY_VAR=None; QL_POLICY_VAR=None
ALPHA_VAR=None; EPSILON_VAR=None
NGOAL=None
def create_TK_Canvas():
  root = tk.Tk()
  root.title(TITLE)
  global TK_Canvas, CONSOLEVAR, VI_MENU, VI_AGENT_MENU, QLEARN_MENU, R, SEGMENTS #, SEGMENTS_FOR_POLICY
  global NOISE_VAR, NGOALS_VAR, R_VAR, G_VAR, DISPLAY_VALS_VAR, Q_VAR, ALPHA_VAR, EPSILON_VAR, EXPL_VAR
  global VI_POLICY_VAR, QL_POLICY_VAR, GOLDEN_PATH_VAR
  global COMPARE_VAR
  TK_Canvas = tk.Canvas(root,width=WIDTH, height=HEIGHT)
  TK_Canvas.configure(background="#ccccff") # Blue-gray
  TK_Canvas.pack(fill="both", expand=True)
  TK_Canvas.create_rectangle(0, HEIGHT*0.3-70, WIDTH, HEIGHT, fill="#888888") # Background to make q values more visible.

  menubar = tk.Menu(root)

  # create a pulldown menu, and add it to the menu bar
  filemenu = tk.Menu(menubar, tearoff=0)
  filemenu.add_command(label="Restart with 2 disks", command=lambda :MDP_command("NDISKS",2))
  filemenu.add_command(label="Restart with 3 disks", command=lambda :MDP_command("NDISKS",3))
  filemenu.add_command(label="Restart with 4 disks", command=lambda :MDP_command("NDISKS",4))
  filemenu.add_command(label="Exit", command=exit)
  menubar.add_cascade(label="File", menu=filemenu)

  # create more pulldown menus
  NOISE_VAR = tk.IntVar()
  MDP_Noise_menu = tk.Menu(menubar, tearoff=0)
  MDP_Noise_menu.add_checkbutton(label="0% (deterministic)", var=NOISE_VAR, onvalue=1, offvalue=2,\
                      command=lambda :MDP_command("noise",0))
  MDP_Noise_menu.add_checkbutton(label="20%", var=NOISE_VAR, onvalue=2, offvalue=1,\
                      command=lambda :MDP_command("noise",0.2))
  menubar.add_cascade(label="MDP Noise", menu=MDP_Noise_menu)

  MDP_Rewards_menu = tk.Menu(menubar, tearoff=0)
  NGOALS_VAR = tk.IntVar()
  MDP_Rewards_menu.add_checkbutton(label="One goal, R=100", var=NGOALS_VAR, onvalue=1, offvalue=2,\
                      command=lambda :MDP_command("ngoals",1))
  MDP_Rewards_menu.add_checkbutton(label="Two goals, R=100 and R=10", var=NGOALS_VAR, onvalue=2, offvalue=1,\
                      command=lambda :MDP_command("ngoals",2))

  R_VAR = tk.IntVar()
  MDP_Rewards_menu.add_checkbutton(label="Living R=0", var=R_VAR, onvalue=1,\
                      command=lambda :MDP_command("living_reward",0))
  MDP_Rewards_menu.add_checkbutton(label="Living R= -0.01", var=R_VAR, onvalue=2,\
                      command=lambda :MDP_command("living_reward",-0.01))
  MDP_Rewards_menu.add_checkbutton(label="Living R= -0.1", var=R_VAR, onvalue=3,\
                      command=lambda :MDP_command("living_reward",-0.1))
  MDP_Rewards_menu.add_checkbutton(label="Living R= +0.1", var=R_VAR, onvalue=4,\
                      command=lambda :MDP_command("living_reward",0.1))

  GOLDEN_PATH_VAR = tk.BooleanVar()
  MDP_Rewards_menu.add_checkbutton(label="Show golden path (optimal solution)", var=GOLDEN_PATH_VAR, onvalue=True,\
                      command=lambda :MDP_command("show_golden_path",True))
  menubar.add_cascade(label="MDP Rewards", menu=MDP_Rewards_menu)

  G_VAR = tk.IntVar()
  gammamenu = tk.Menu(menubar, tearoff=0)
  gammamenu.add_checkbutton(label="\u03b3 = 1.0", var=G_VAR, onvalue=1,\
                      command=lambda :MDP_command("set_gamma",1.0))
  gammamenu.add_checkbutton(label="\u03b3 = 0.99", var=G_VAR, onvalue=2,\
                      command=lambda :MDP_command("set_gamma",0.99))
  gammamenu.add_checkbutton(label="\u03b3 = 0.9", var=G_VAR, onvalue=3,\
                      command=lambda :MDP_command("set_gamma",0.9))
  gammamenu.add_checkbutton(label="\u03b3 = 0.5", var=G_VAR, onvalue=4,\
                      command=lambda :MDP_command("set_gamma",0.5))
  menubar.add_cascade(label="Discount", menu=gammamenu)

  DISPLAY_VALS_VAR = tk.IntVar()
  VI_MENU = tk.Menu(menubar, tearoff=0)
  VI_MENU.add_checkbutton(label="Show state values (V) from VI", var=DISPLAY_VALS_VAR, onvalue=1,\
                      command=lambda :MDP_command("show_values", 1))
  VI_MENU.add_checkbutton(label="Show Q values from VI", var=DISPLAY_VALS_VAR, onvalue=2,\
                      command=lambda :MDP_command("show_values", 2))
  VI_MENU.add_command(label="Reset state values (V) and Q values for VI to 0",\
                      command=lambda :MDP_command("Value_Iteration",0))
  VI_MENU.add_command(label="1 step of VI",\
                      command=lambda :MDP_command("Value_Iteration",1))
  VI_MENU.add_command(label="10 steps of VI",\
                      command=lambda :MDP_command("Value_Iteration",10))
  VI_MENU.add_command(label="100 steps of VI",\
                      command=lambda :MDP_command("Value_Iteration",100))
  VI_POLICY_VAR = tk.BooleanVar()
  VI_MENU.add_checkbutton(label="Show Policy from VI", var=VI_POLICY_VAR, onvalue=True,\
                      command=lambda :MDP_command("Show_Policy_from_VI",True))
  menubar.add_cascade(label="Value Iteration", menu=VI_MENU)

  VI_AGENT_MENU = tk.Menu(menubar, tearoff=0)
  VI_AGENT_MENU.add_command(label="Reset state to s0",\
                      command=lambda :MDP_command("Agent",0))
  VI_AGENT_MENU.add_command(label="Perform 1 action",\
                      command=lambda :MDP_command("Agent",1))
  VI_AGENT_MENU.add_command(label="Perform 10 actions",\
                      command=lambda :MDP_command("Agent",10))
  VI_AGENT_MENU.add_command(label="Perform 100 actions",\
                      command=lambda :MDP_command("Agent",100))
  menubar.add_cascade(label="VI Agent", menu=VI_AGENT_MENU)

  QLEARN_MENU = tk.Menu(menubar, tearoff=0)
  Q_VAR = tk.BooleanVar()
  QLEARN_MENU.add_checkbutton(label="Show state values (V) from QL", var=DISPLAY_VALS_VAR, onvalue=3,\
                      command=lambda :MDP_command("show_values", 3))
  QLEARN_MENU.add_checkbutton(label="Show Q values from QL", var=DISPLAY_VALS_VAR, onvalue=4,\
                      command=lambda :MDP_command("show_values", 4))
  QLEARN_MENU.add_command(label="Reset state values (V) and Q values for QL to 0",\
                      command=lambda :MDP_command("QLearn",-2))
  QLEARN_MENU.add_command(label="Reset state to s0",\
                      command=lambda :MDP_command("QLearn",-1))
  CONSOLEVAR = tk.BooleanVar()
  QLEARN_MENU.add_checkbutton(label="User driving console", var=CONSOLEVAR, onvalue=True, offvalue=False,\
                      command=open_user_driving_console)
  QLEARN_MENU.add_command(label="Perform 1 action",\
                      command=lambda :MDP_command("QLearn",1))
  QLEARN_MENU.add_command(label="Perform up to 10 actions",\
                      command=lambda :MDP_command("QLearn",10))
  QLEARN_MENU.add_command(label="Perform up to 100 actions",\
                      command=lambda :MDP_command("QLearn",100))
  QLEARN_MENU.add_command(label="Train for 1000 transitions",\
                      command=lambda :MDP_command("QLearn",-1000))
  QL_POLICY_VAR = tk.BooleanVar()
  QLEARN_MENU.add_checkbutton(label="Show Policy from QL", var=QL_POLICY_VAR, onvalue=True,\
                      command=lambda :MDP_command("Show_Policy_from_QL",True))
  QLEARN_MENU.add_command(label="Compare results of Q-Learning and Value Iteration",\
          command=lambda :MDP_command("compare",0))
  QLEARN_MENU.entryconfig("Compare results of Q-Learning and Value Iteration", state="disabled")
  menubar.add_cascade(label="Q-Learning", menu=QLEARN_MENU)

  QL_PARAM_MENU = tk.Menu(menubar, tearoff=0)
  ALPHA_VAR = tk.IntVar()
  QL_PARAM_MENU.add_checkbutton(label="Fixed \u03b1=0.1", var=ALPHA_VAR, onvalue=1,\
                      command=lambda :MDP_command("alpha",1))
  QL_PARAM_MENU.add_checkbutton(label="Fixed \u03b1=0.2", var=ALPHA_VAR, onvalue=2,\
                      command=lambda :MDP_command("alpha",2))
  QL_PARAM_MENU.add_checkbutton(label="Custom \u03b1", var=ALPHA_VAR, onvalue=3,\
                      command=lambda :MDP_command("alpha",3))
  EPSILON_VAR = tk.IntVar()
  QL_PARAM_MENU.add_checkbutton(label="Fixed \u03b5=0.1", var=EPSILON_VAR, onvalue=1,\
                      command=lambda :MDP_command("epsilon",1))
  QL_PARAM_MENU.add_checkbutton(label="Fixed \u03b5=0.2", var=EPSILON_VAR, onvalue=2,\
                      command=lambda :MDP_command("epsilon",2))
  QL_PARAM_MENU.add_checkbutton(label="Custom \u03b5", var=EPSILON_VAR, onvalue=3,\
                      command=lambda :MDP_command("epsilon",3))
  EXPL_VAR = tk.BooleanVar()
  QL_PARAM_MENU.add_checkbutton(label="Use exploration function (and reset Q values)", var=EXPL_VAR, onvalue=True,\
                      command=lambda :MDP_command("Exploration",0))
  menubar.add_cascade(label="QL Params", menu=QL_PARAM_MENU)
  # Check if autograder is available:
  try:
      import basic_autograder as bag
      filemenu.add_command(label="Basic autograde", command=bag.basic_autograde)
  except: pass    
  try:
      import advanced_autograder as aag
      filemenu.add_command(label="Advanced autograde", command=aag.advanced_autograde)
  except: pass
  # Check is a special script is available (to setup for testing, etc.)
  try:
      import script_for_TOH_MDP as script
      filemenu.add_command(label="Run script", command=lambda :MDP_command("Run_script",True))
  except: pass    

  # Finally, do some initialization needed for policy display and displaying the user driving console.
  Ra = R * 1.6  
  SEGMENTS = [ (int(R*x), int(R*y), int(Ra*x), int(Ra*y)) for (x, y) in DRIVING_ARROW_XYS]

# display the menu
  root.config(menu=menubar)
  #print("VIS initialization finished")

def init_menu_settings():
    global NOISE_VAR, NGOALS_VAR, R_VAR, GVAR, ALPHA_VAR, EPSILON_VAR, DISPLAY_VALS_VAR 
    NOISE_VAR.set(2)
    NGOALS_VAR.set(1)
    R_VAR.set(1)
    G_VAR.set(3)
    Q_VAR.set(False)
    ALPHA_VAR.set(1)
    EPSILON_VAR.set(1)
    enable_most_ql_menu_items(True)
    enable_value_iteration(True)
    DISPLAY_VALS_VAR.set(0)
    
def enable_value_iteration(tf):
    if tf:
        for i in range(1,6):
          VI_MENU.entryconfig(i, state="normal")
    else:
        for i in range(3,6):
          VI_MENU.entryconfig(i, state="disabled")

def enable_policy_extraction(tf):
    if tf: VI_MENU.entryconfig("Show Policy from VI", state="normal")
    else: VI_MENU.entryconfig("Show Policy from VI", state="disabled")

def enable_QL_policy_item(tf):
    if tf: QLEARN_MENU.entryconfig("Show Policy from QL", state="normal")
    else: QLEARN_MENU.entryconfig("Show Policy from QL", state="disabled")
  

def enable_vi_action_menu_items(tf):
    if tf:
      for i in range(1,4):
        VI_AGENT_MENU.entryconfig(i, state="normal")
    else: 
      for i in range(1,4):
        VI_AGENT_MENU.entryconfig(i, state="disabled")

def enable_most_ql_menu_items(tf):
  if tf:
      for i in range(1,7):
        QLEARN_MENU.entryconfig(i, state="normal")
  else:
      for i in range(1,7):
        QLEARN_MENU.entryconfig(i, state="disabled")

def enable_compare_menu_item(tf):
  try:
    if tf:
      QLEARN_MENU.entryconfig("Compare results of Q-Learning and Value Iteration", state="normal")
    else:
      QLEARN_MENU.entryconfig("Compare results of Q-Learning and Value Iteration", state="disabled")
  except: pass
  
NDISKS = 0 # gets overwritten in first call to basic_plot.
DIVISOR = 1 # "      "   # Used in computing barycentric coordinates.
CANONICAL_STATE = {} # An identity mapping that is useful only for hashing
  # different "copies" of states to the specific instances that have the
  # coordinates field attached to them.
#STATES_TO_LABELS = {}
Q_TEXT_FONT = None
VALUE_FONT = None
MDP_command = None
GOLDEN_PATH_EDGES=None; SILVER_PATH_EDGES=None
def basic_plot(SEdict, ndisks, mdp_command, ngoals, golden_path, silver_path):
    global NDISKS, R, DIVISOR, MDP_command, CANONICAL_STATE
    global CIRCS, EDGE_LINES, STATES_TO_LABELS, Q_TEXT_FONT, VALUE_FONT
    global SEGMENTS_FOR_POLICY_0, SEGMENTS_FOR_POLICY_1
    global DISPLAY_VALS_VAR, PI_LINE_BUFS, VI_POLICY_VAR, QL_POLICY_VAR, GOLDEN_PATH_VAR
    global NGOALS, GOLDEN_PATH, SILVER_PATH, GOLDEN_PATH_EDGES, SILVER_PATH_EDGES
    MDP_command = mdp_command # Register this callback for many menu items to invoke.
    NGOALS=ngoals; GOLDEN_PATH=golden_path; SILVER_PATH=silver_path
    # If any TK_Canvas items already exist from a previous run, delete them now.
    for item in CIRCS: TK_Canvas.delete(item)
    for item in EDGE_LINES: TK_Canvas.delete(item)
    for (state, item) in STATES_TO_LABELS.items(): TK_Canvas.delete(item)
    clear_all_policy_displays()
    GOLDEN_PATH_EDGES=[] ; SILVER_PATH_EDGES=[]
    # Compute the cartesian coordinates of each state.
    NDISKS = ndisks
    if NDISKS==4:
        R = 13
        Q_TEXT_FONT = ("Helvetica", 5)
        VALUE_FONT = ("Helvetica", 9)
    if NDISKS==3:
        R = 20
        Q_TEXT_FONT = ("Helvetica", 9)
        VALUE_FONT = ("Helvetica", 11)
    if NDISKS==2:
        R = 45
        Q_TEXT_FONT = ("Helvetica", 10)
        VALUE_FONT = ("Helvetica", 14)
    DIVISOR = (2**(NDISKS))-1
    if not TK_Canvas:
        create_TK_Canvas()
        init_menu_settings()

    LANDMARKS = [(WIDTH*0.1, HEIGHT*0.91), (WIDTH*0.5, HEIGHT*0.27), (WIDTH*0.9, HEIGHT*0.91)]

    CANONICAL_STATE = {} # Get rid of old mapping in case this is a redo from the file menu.

    for s in SEdict.keys():
        #print(s)
        Wghts = barycentric(s) # Go compute barycentric coords.
        # Now use them to get the x and y coordinates.
        x = 0;
        y = 0
        for i in range(3):
            x += Wghts[i] * LANDMARKS[i][0]
            y += Wghts[i] * LANDMARKS[i][1]
        x = int(x)
        y = int(y)
        s.coords = (x,y) #Save the coordinates.
        CANONICAL_STATE[s]=s # Crazy but needed.

    # Next draw all edges out of each state.
    # Each edge will be drawn twice, but it doesn't matter.
    for s in SEdict.keys():
        x0, y0 = s.coords
        for item in SEdict[s]:
            op, sp = item
            spp = CANONICAL_STATE[sp] # Get the canonical copy of this state.
            x1, y1 = spp.coords
            line = TK_Canvas.create_line(x0, y0, x1, y1)
            EDGE_LINES.append(line)
            if s in GOLDEN_PATH and sp in GOLDEN_PATH:
              GOLDEN_PATH_EDGES.append(line)

            # NOTE SILVER PATHS CANNOT BE RELIABLY DISPLAYED WITH THE CURRENT
            # SOFTWARE ARCHITECTURE HERE, DUE TO THE FACT THAT THEY ARE GENERATED
            # AFTER THE LAYOUT HERE HAS BEEN SET UP, SO THEIR LINE SEGMENTS CANNOT EASILY
            # BE IDENTIFIED AND ADJUSTED.
            #if NGOALS==2:
            #  if s in SILVER_PATH and sp in SILVER_PATH:
            #    SILVER_PATH_EDGES.append(line)

    # Finally, draw the nodes, one for each state. 
    for s in SEdict.keys():
        x,y = s.coords
        s.circ = TK_Canvas.create_oval(x-R, y-R, x+R, y+R, fill='yellow')
        CIRCS.append(s.circ)

    # Anticipate request for policy by computing SEGMENTS_FOR_POLICY
    Ra = int(R*1.5)
    SEGMENTS_FOR_POLICY_0 = [ (int(R*x), int(R*y), int(Ra*x), int(Ra*y)) for (x, y) in POLICY_XYS_0] +\
                          [ (0, R, 0, 2*R) ] # Exit action and others go straight down.
    SEGMENTS_FOR_POLICY_1 = [ (int(R*x), int(R*y), int(Ra*x), int(Ra*y)) for (x, y) in POLICY_XYS_1] +\
                          [ (R/5, R, R/5, 2*R) ] # Exit action and others go straight down.
    DISPLAY_VALS_VAR.set(0) # Reset the display mode to yellow disks.
    enable_vi_action_menu_items(False)
    VI_POLICY_VAR.set(False)
    QL_POLICY_VAR.set(False)
    enable_QL_policy_item(False)
    GOLDEN_PATH_VAR.set(False)

def show_golden_path():
  # Show or hide the golden path (and silver path, if NGOALS=2).
  # Query the variable associated with the menu item (Rewards menu, last item).
  # Display by recoloring and re-attributing the width of the line segments on the path.
  global GOLDEN_PATH_VAR, GOLDEN_PATH_EDGES, SILVER_PATH_EDGES
  if GOLDEN_PATH_VAR.get():
    show_soln_path(GOLDEN_PATH_EDGES, "gold")
    if NGOALS==2:
      show_soln_path(SILVER_PATH_EDGES, "LightCyan2")
  else:  
    show_soln_path(GOLDEN_PATH_EDGES, "black")
    if NGOALS==2:
      show_soln_path(SILVER_PATH_EDGES, "black")

def show_soln_path(edges, color):
  for edge in edges:
      TK_Canvas.itemconfig(edge, fill=color)
      
# Given a peg (list of disks) figure out one barycentric coord. for
# the state.
def make_weight(disks):
    global DIVISOR
    w = 0
    for dsk in disks:
        w += 2**(dsk-1)
    return w/DIVISOR

# Compute all 3 barycentric coordinates for state s.
def barycentric(s):
    d = s.d # Get the dictionary.
    return [make_weight(d[peg]) for peg in ['peg1','peg2','peg3']]

VALUE_LABELS = None        
STATS_LABELS = None        
Q_ITEMS = []
def clear_any_vals_and_q_vals():
  # facilitate changes in what to display by making it easy to
  # get rid of the current display.
    global VALUE_LABELS, Q_ITEMS
    if VALUE_LABELS:
        for lab in VALUE_LABELS: TK_Canvas.delete(lab)
    VALUE_LABELS = []
    if len(Q_ITEMS) >0: # or not Q_VAR.get():
        for item in Q_ITEMS:
            TK_Canvas.delete(item)
        Q_ITEMS = []

def clear_a_policy_display(policy_number):
    global PI_LINE_BUFS
    for line in PI_LINE_BUFS[policy_number]:
        TK_Canvas.delete(line)
    PI_LINE_BUFS[policy_number] = []

def clear_all_policy_displays():
  for i in range(2): clear_a_policy_display(i)
  
    
# The following takes a dictionary mapping states to values.
# It uses the coordinates of states already computed.
# So the states here should be the same instances as in the SEdict.
# If not, this code may need to be modified to do the canonical mapping again.
VALUE_LABELS = None        
def display_values(V):
    global VALUE_LABELS, STATES_TO_LABELS, CANONICAL_STATE, VALUE_FONT
    print("In display_values, number of items is "+str(len(V)))
    #if VALUE_LABELS:
    #    for lab in VALUE_LABELS: TK_Canvas.delete(lab)
    #VALUE_LABELS = []
    clear_any_vals_and_q_vals()
    for s, v in V.items():
        try:
          #print("CANONICAL_STATE[s] is "+str(CANONICAL_STATE[s]))
          sc = CANONICAL_STATE[s]
          x,y = sc.coords
          #print("Coords are: "+str((x,y)))
          label = TK_Canvas.create_text(x, y, font=VALUE_FONT, text=str(v))
          VALUE_LABELS.append(label)
          STATES_TO_LABELS[s] = label
          reshow_state(s, v)     # Color the background appropriately.
        except: pass # Terminal_state has no coordinates.
# The following will draw or redraw a text label at the top of the display.
def display_stats(stats_string):
    global STATS_LABELS
    if STATS_LABELS:
        for lab in STATS_LABELS: TK_Canvas.delete(lab)
    STATS_LABELS = []
    STATS_LABELS.append(TK_Canvas.create_text(WIDTH/2,20, text=stats_string))

#HIGHLIGHTED_STATE = None
#def highlight_state(s):
#    global HIGHLIGHTED_STATE
#    if HIGHLIGHTED_STATE:
#        s_old = HIGHLIGHTED_STATE
#        TK_Canvas.itemconfigure(s_old.circ, fill='yellow')
#        #x,y = s_old.coords
#        #s_old.circ = TK_Canvas.create_oval(x-R, y-R, x+R, y+R, fill='yellow')
#    HIGHLIGHTED_STATE = s
#    x,y = s.coords
#    TK_Canvas.itemconfigure(s.circ, fill='red')

#def highlight(s):
#    TK_Canvas.after(20, lambda: highlight2(s))

def highlight(s):
    Rh = R+4
    try:
      sc = CANONICAL_STATE[s]
      x,y = sc.coords
      sc.highlight = TK_Canvas.create_oval(x-Rh, y-Rh, x+Rh, y+Rh, outline='blue', width=3)
      TK_Canvas.update_idletasks()
    except: pass
    TOH_state_vis(s) # Draw the puzzle in this state.

#def unhighlight(s):
#    TK_Canvas.after(20, lambda: unhighlight2(s))
    
def unhighlight(s):
    try:
      sc = CANONICAL_STATE[s]
      TK_Canvas.delete(sc.highlight)
      del sc.highlight
    except: pass
    
def reshow_state(s, value, color=None):
  global VALUE_FONT, STATES_TO_LABELS, TK_Canvas
  try:
    if not color: color = value_to_color(value)
    sc = CANONICAL_STATE[s]
    TK_Canvas.itemconfigure(sc.circ, fill=color)
    label = STATES_TO_LABELS[s]
    if value<0: vstr = str(value)[:5]
    else: vstr = str(value)[:4]
    #txtcolor = "black"
    #if abs(value) < MAX_VAL*0.8: txtcolor = "white"
    txtcolor = "white"
    TK_Canvas.itemconfigure(label, text=vstr, font=VALUE_FONT, fill=txtcolor)
  except: pass
  
def value_to_color(v):
    ''' If v is negative return a shade of red that is
   brightest at -5 and nothing at 0.
   Otherwise, return a shade of green that is brightest at 5
   and nothing at 0.  The color is represented as a hex
   string such as xff0000.'''
    if v<0:
       if v < MIN_VAL: v = MIN_VAL
    if v > MAX_VAL: v = MAX_VAL
    v /= MAX_VAL
    r = 0; g = 0; b = 0
    if v < 0:
      r = int(-(v * 255))
    else:
      g = int(v * 255)
    
    red = hex(r)[2:]
    green = hex(g)[2:]
    blue = hex(b)[2:]
    if len(red) == 1:
      red = "0" + red
    if len(green) == 1:
      green = "0" + green
    if len(blue) == 1:
      blue = "0" + blue
    color = "#" + red + green + blue
    return color

PI_LINE_BUFS = [[],[]]
def show_policy(pi, policy_number=0, use_alt_segments=False, color="brown"):
    global PI_LINE_BUFS
    for line in PI_LINE_BUFS[policy_number]:
        TK_Canvas.delete(line)
    PI_LINE_BUFS[policy_number] = []
    for s in pi.keys():
      try:
        sc = CANONICAL_STATE[s]
        a = pi[s]
        #if a=="Exit": continue  # OK, now we handle Exit actions (we draw a down arrow.
        (xc,yc) = sc.coords
        (dx0, dy0, dx1, dy1) = action_to_arrow_coords(a, use_alt_segments=use_alt_segments)
        PI_LINE_BUFS[policy_number].append(TK_Canvas.create_line(xc+dx0, yc+dy0, xc+dx1, yc+dy1, arrow=tk.LAST, fill=color))
      except:
        print("Note: state not in CANONICAL_STATE table: "+str(s))
              
# deprecated:
def old_show_policy(pi):
    global PI_LINES, SEGMENTS_FOR_POLICY
    print(SEGMENTS_FOR_POLICY)
    for line in PI_LINES:
        TK_Canvas.delete(line)
    PI_LINES = []
    for s in pi.keys():
        sc = CANONICAL_STATE[s]
        a = pi[s]
        #if a=="Exit": continue  # OK, now we handle Exit actions (we draw a down arrow.
        (xc,yc) = sc.coords
        (dx0, dy0, dx1, dy1) = action_to_arrow_coords(a)
        PI_LINES.append(TK_Canvas.create_line(xc+dx0, yc+dy0, xc+dx1, yc+dy1, arrow=tk.LAST, fill="blue"))

# Support for drawing arrows in 6 different directions, for displaying policies.
import math
DRIVING_ARROW_DIRECTIONS = [(-math.pi * 2 * n / 6) for n in range(6)]
DIRECTIONS_0 = [(-math.pi * 2 * n / 6)-0.1 for n in range(6)]
DIRECTIONS_1 = [(-math.pi * 2 * n / 6)+0.1 for n in range(6)]

DRIVING_ARROW_XYS  = [(math.cos(d), math.sin(d)) for d in DRIVING_ARROW_DIRECTIONS]
POLICY_XYS_0  = [(math.cos(d), math.sin(d)) for d in DIRECTIONS_0]
POLICY_XYS_1  = [(math.cos(d), math.sin(d)) for d in DIRECTIONS_1]

def action_to_arrow_coords(a, use_alt_segments=False):
    global SEGMENTS_FOR_POLICY_0, SEGMENTS_FOR_POLICY_1
    segments = SEGMENTS_FOR_POLICY_0
    if use_alt_segments:
      segments = SEGMENTS_FOR_POLICY_1 # displaced, so can be seen with the others.
    try:
      idx = ACTIONS.index(a)
      return segments[idx]
    except:
      print("Invalid action: "+str(a)+" when drawing policy.")
      return segments[-1]

import math
#Q_TEXT_DELTAS = [(int(R*math.sin(th)), int(R*math.cos(th))) for th in [2*math.pi * (i+0.5)/6.0 for i in range(6)]]
Q_TEXT_DELTAS = [(R,R),(1.5*R, 0),(R,-R),(-R,-R),(-1.5*R,0),(-R, R)]
#print("Q_TEXT_DELTAS: "+str(Q_TEXT_DELTAS))
Q_ARCS_AND_TEXT = {} # For updating Q values via Tk.configure
def show_q_values(q_values, S):
    '''For each state in S, except goal states, and the Terminal_state (if there) show 6 sectors,
    color-coded by Q-value.
    Make q-value text items sensitive to button clicks in case number is illegible.
    Another possibility: hide V values.
       '''
    global DISPLAY_VALS_VAR, Q_ITEMS, Q_ARCS_AND_TEXT, Q_TEXT_DELTAS, R, Q_TEXT_FONT
    print("in show_q_values, number of items is: "+str(len(q_values)))
    #if len(Q_ITEMS) >0 or not Q_VAR.get():
    #    for item in Q_ITEMS:
    #        TK_Canvas.delete(item)
    #    Q_ITEMS = []
    clear_any_vals_and_q_vals()
    if DISPLAY_VALS_VAR.get() in [2,4]:
        print("Starting to display q values")
        pass
    else:
        #print("Stopping displaying q values")
        return
    non_exit_actions = ACTIONS[:-1]
    #(S, q_values) = MDP_command("Get_Q_Values",0)
    #print("Got Q values")
    arc_r = R
    xscale=0.8
    yscale = 1
    if NDISKS==2:
        xscale=1.5; yscale=1.5
    elif NDISKS==4:
        xscale=0.3; yscale=0.5
    for s in S: 
        arcs_for_s = []
        try: 
            sc = CANONICAL_STATE[s] # get the equivalent state instance containing coordinates.
        except: continue
        (x,y) = sc.coords
        for i, a in enumerate(non_exit_actions):
            q = q_values[(s, a)]
            color = value_to_color(q)
            arc_item = TK_Canvas.create_arc(x-arc_r, y-arc_r, x+arc_r, y+arc_r,\
                                            start=(60*i)-30, extent=60, fill=color, outline="black")
            arcs_for_s.append(arc_item)
            Q_ITEMS.append(arc_item)
        for i, a in enumerate(non_exit_actions): # Loop separately for text, so it stays on top in all 6 sectors.
            q = q_values[(s, a)]
            qstr = " %3.1f " % q
            idx = (i + 1) % 6
            xc = x + int(xscale*Q_TEXT_DELTAS[idx][0])
            yc = y + int(yscale*Q_TEXT_DELTAS[idx][1])
            text_item = TK_Canvas.create_text(xc, yc, font=Q_TEXT_FONT, text=qstr, fill="#ffffff", tags=a)
            TK_Canvas.tag_bind(text_item, '<ButtonPress-1>', show_q_details)
            Q_ITEMS.append(text_item)
            Q_ARCS_AND_TEXT[(sc,a)] = (arcs_for_s[i], text_item)
            Q_ARCS_AND_TEXT[(sc,a)] = (arcs_for_s[i], text_item)
        # add code for Exit actions to handle them specially here.
        #try:
        if True:
            q = q_values[(s, 'Exit')]
            qstr = " %3.1f " % q
            color = value_to_color(q)
            exit_r = R / 2
            (x,y) = sc.coords
            arc_item = TK_Canvas.create_oval(x-exit_r, y-exit_r, x+exit_r, y+exit_r,\
                                            fill=color, outline="black")
            arcs_for_s.append(arc_item)
            Q_ITEMS.append(arc_item)
            text_item = TK_Canvas.create_text(x, y, font=Q_TEXT_FONT, text=qstr, fill="#ffffff", tags="Exit")
            TK_Canvas.tag_bind(text_item, '<ButtonPress-1>', show_q_details)
            Q_ITEMS.append(text_item)
            Q_ARCS_AND_TEXT[(sc,"Exit")] = (arc_item, text_item)
        #except: pass           
    enable_most_ql_menu_items(True)
            
#def clear_q_value_display():
#    global Q_VAR
#    Q_VAR.set(False)
#    show_q_values(None, None)

#def reshow_all_q_values(q_values, S):
#    '''For now, just call show_q_values.
#    Possible future version will just reconfigure existing TK_Canvas items.'''
#    show_q_values(q_values, S)

def update_q_value(s, a, value):
    '''Change the display for this one q-value. '''
    # Find the arc-text items pair
    global Q_ARCS_AND_TEXT
    try:
      sc = CANONICAL_STATE[s]
      (arc_item, text_item) = Q_ARCS_AND_TEXT[(sc, a)]
      new_color = value_to_color(value) 
      TK_Canvas.itemconfigure(arc_item, fill=new_color)
      qstr = " %3.1f " % value
      TK_Canvas.itemconfigure(text_item, text=qstr)
      print("In Vis.update_q_value; new q-value is "+str(value))
    except: print("No match in update_q_value for key "+str((s, a)))
    
SV_RECTS = []        
def TOH_state_vis(s):
    '''Display state s as a TOH snapshot.
    This could be part of an animation.'''
    global SV_RECTS, WIDTH
    for item in SV_RECTS:
        TK_Canvas.delete(item)
    SV_RECTS = []
    BIG_DIAM = 100 # diameter of largest disk
    BIG_RADIUS = BIG_DIAM / 2
    XCENTER = WIDTH / 2
    YBASE = 120
    if NDISKS==2: YBASE = 110
    DISK_HEIGHT=12
    BASE_WIDTH = int(BIG_DIAM * 3.5)
    BASE_HEIGHT = DISK_HEIGHT
    # Draw the base for the puzzle:
    SV_RECTS.append(TK_Canvas.create_rectangle(XCENTER-BASE_WIDTH/2, YBASE, XCENTER+BASE_WIDTH/2, YBASE-BASE_HEIGHT, fill="black"))
    
    peg_sep = int(BIG_DIAM * 1.2)
    peg_height = int(NDISKS * DISK_HEIGHT * 1.3)
    PEG_RADIUS = 8
    xpeg = XCENTER - peg_sep
    for p in ['peg1','peg2','peg3']:
        #Draw a peg:
        SV_RECTS.append(TK_Canvas.create_rectangle(xpeg - PEG_RADIUS, YBASE-BASE_HEIGHT, xpeg + PEG_RADIUS, YBASE-BASE_HEIGHT - peg_height, fill="brown"))
        #Draw the disks
        for i, disk in enumerate(s.d[p]):
            disk_radius = int(BIG_RADIUS * disk / NDISKS)
            SV_RECTS.append(TK_Canvas.create_rectangle(\
                xpeg - disk_radius,\
                YBASE-BASE_HEIGHT-(i*DISK_HEIGHT),\
                xpeg + disk_radius,\
                YBASE-BASE_HEIGHT - ((i+1)*DISK_HEIGHT),\
                fill="blue"))
        xpeg += peg_sep

DA_COLOR="#8000AA"
DRIVING_ARROWS = []            
def open_user_driving_console(): 
    '''Display 6 purple arrows on a section of the canvas) to respond
    to user clicks to enter actions to the agent.
    '''
    global SEGMENTS, DRIVING_ARROWS, CONSOLEVAR, DA_COLOR
    #print("Value of consolevar is "+str(consolevar.get()))
    if CONSOLEVAR.get(): # Controls whether to show or hide the console.
        
      if len(DRIVING_ARROWS)==0:
        XC = 100
        YC = 300
        inner_scale = 0.5
        outer_scale = 2
        for i in range(6):
            (px0, py0, px1, py1) = SEGMENTS[i]
            (x0, y0, x1, y1) = (inner_scale * px0, inner_scale * py0, outer_scale * px1, outer_scale * py1)
            an_arrow = TK_Canvas.create_line(x0+XC, y0+YC, x1+XC, y1+YC,\
                                                        width= 12, arrow=tk.LAST, fill=DA_COLOR,\
                                                        tags="Action"+str(i))
            TK_Canvas.tag_bind(an_arrow, '<ButtonPress-1>', handle_user_action_selection)
            DRIVING_ARROWS.append(an_arrow)
        rec = 9
        # Create a circle for the Exit action:
        exit_circle = TK_Canvas.create_oval(XC - rec, YC-rec, XC+rec, YC+rec, fill="gray",\
                                            tags="Action6")
        TK_Canvas.tag_bind(exit_circle, '<ButtonPress-1>', handle_user_action_selection)
        DRIVING_ARROWS.append(exit_circle)
    else:
        # Hide the driving console.
        for item in DRIVING_ARROWS:
            TK_Canvas.delete(item)
        DRIVING_ARROWS = []

LAST_DC_STATUS = False
def set_driving_console_status(allow_exit_only=False):
  global LAST_DC_STATUS, DA_COLOR
  if allow_exit_only==LAST_DC_STATUS: return
  LAST_DC_STATUS=allow_exit_only
  if len(DRIVING_ARROWS)==0: return
  if allow_exit_only:
    for i in range(6):
      TK_Canvas.itemconfigure(DRIVING_ARROWS[i], fill="gray")
    TK_Canvas.itemconfigure(DRIVING_ARROWS[6], fill=DA_COLOR)
  else:
    for i in range(6):
      TK_Canvas.itemconfigure(DRIVING_ARROWS[i], fill=DA_COLOR)
    TK_Canvas.itemconfigure(DRIVING_ARROWS[6], fill="gray")
  
            
def handle_user_action_selection(event):
    #print("User selected the action associated with widget: ", event.widget)
    global LAST_DC_STATUS
    id = event.widget.find_closest(event.x, event.y)[0]
    action_no = DRIVING_ARROWS.index(id)
    a = ACTIONS[action_no]
    print("Requested action is: "+a)
    if LAST_DC_STATUS and action_no < 6:
      print("Directional action not permitted in a goal state. Use 'Exit' action instead.")
      return
    else:
      MDP_command("User_chose", a)

# Beginnings of a function to handle clicks on q-value texts....
def show_q_details(event):
    id = event.widget.find_closest(event.x, event.y)[0]
    if id in Q_ITEMS:
        print("You clicked on id: "+str(id))
        try:
          print(TK_Canvas.itemcget(id, "text"))
          print(str(TK_Canvas.gettags(id)))
        except: pass
     
def make_sa_key(s, a):
  #return a tuple based on the canonical state for s.
  try:
    sc = CANONICAL_STATE[s]
    return (sc, a)
  except: return (s, a)
  

