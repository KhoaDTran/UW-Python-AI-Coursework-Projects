'''script_for_TOH_MDP.py

Test script for controlling TOH_MDP programmatically.

You are not required to edit this script. 
However, it demonstrates a hook that might turn out to be
useful during debugging or running experiments.

The script can be run from the app's File menu.
However, this script file must be in the same folder as the
rest of the code or it will be ignored.

This version demonstrates both (a) app setup (e.g., as if you
manually selected the menu item File: Restart with 2 disks, etc.,
and (b) running QL training until a convergence criterion is
satisfied.



'''

print("Importing script_for_TOH_MDP")


def run(the_globals):
    g=the_globals # abbreviate this for convenience.
    print("The script is being run.")
    # Reset the app to 2 disk mode.
    g['MDP_command']("NDISKS",2)

    # Skip the 2-goal setup, unless the VI extract policy method supports it.
    # Set the MDP to have two goal states.
    #g['MDP_command']("ngoals",2)

    # Set up and run Value Iteration, to get optimal V's, Q's, and Policy.
    g['Vis'].DISPLAY_VALS_VAR.set(1) # Mode for displaying the state values from Value Iteration.
    g['MDP_command']("Value_Iteration",0) # Resets state values and enables VI.
    g['MDP_command']("Value_Iteration",10) # Run 10 iterations of VI.
    g['Vis'].VI_POLICY_VAR.set(True) # Enable display of VI policy.
    g['MDP_command']("Show_Policy_from_VI",0) # Display optimal policy.

    # Set up the GUI to show Q learning values.        
    g['Vis'].DISPLAY_VALS_VAR.set(4) # Now set mode for displaying the Q-values from Q learning.
    g['MDP_command']("QLearn",-2)   # Command to initialize Q-values for Q learning.
    g['Vis'].QL_POLICY_VAR.set(True) # Enable display of QL policy.
    g['MDP_command']("Show_Policy_from_QL",0) # Turn on display of latest QL policy.
    
    # Initialize the Q_Learn agent.
    g['init_Q_Learn_if_needed']() 

    g['train_quietly'](100) # Do 100 transitions of active Q-Learning.

    # For a list of available convergence criteria, search for CFS in the file TOH_MDP.py.
    # Note that policies involve meeting or exceeding a threshold, whereas
    # state and q-value converges involve getting a mean-square error value BELOW the threshold.
    # Thresholds are in percentages for policy matching, but in actual squared values for
    # state and q values.  These values can get as high as 10,000 (assuming living reward 0),
    # because the goal state's value can be 100, meaning the square of 100=0 can be 10000.
    g['train_until'](criterion="Policy match on golden path", threshold=100, max_iterations=10000)
    # Note that training could go on for a long time if the results of VI are not really there.
    # Or things could converge prematurely if the VI policy has not been obtained from
    # running Value Iteration to completion.
    
    print("Done with the run function in the script.")
    
