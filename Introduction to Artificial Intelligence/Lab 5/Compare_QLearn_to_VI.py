'''Compare_QLearn_to_VI.py
Added to the starter code to facilitate
quantitative comparison of Q Learning with Value Iteration results.
Extracts policies whenever comparing them.

S. Tanimoto,
Paul G. Allen School of Computer Sci. & Engineering,
Univ. of Washington.
'''

import TOH_MDP as MDP
#print("From Compare_QLearn_to_VI, "+MDP.TITLE)

def full_compare():
    print("Let's do a full comparison... ")
    print("Policy comparison:")
    all_subsets = [("all states", MDP.get_all_states()), ("golden path", MDP.get_golden_path())]
    if MDP.NGOALS==2:
        if MDP.SILVER_PATH==[]:
            print("Error: SILVER_PATH is empty")
        else:
            all_subsets+=[("silver path", MDP.get_silver_path())]
    for (name, subset) in all_subsets:
        results = compare_policies(subset)
        print("For "+name+", policies agree on "+\
              str(results[0])+" states out of "+str(results[1])+\
              "; percentage="+str(100*results[2])+".")
    print('') # newline

    print("Comparison of state values:")
    for (name, subset) in all_subsets:
        results = compare_state_vals(subset)
        print("For "+name+", mean squared error is "+str(results)+".")
    print('') # newline
        
    print("Comparison of Q values:")
    for (name, subset) in all_subsets:
        results = compare_q_vals(subset)
        print("For "+name+", mean squared error is "+str(results)+".")
    print('') # newline
    
def compare_policies(state_subset):
    # For the given states, compute the number of states on
    # which the VI and QL-based policies match.
    match_count = 0
    n_states = 0
    POLICY_from_VI=MDP.VI.extract_policy(MDP.CLOSED, MDP.ACTIONS)
    POLICY_from_QL=MDP.Q_Learn.extract_policy(MDP.CLOSED, MDP.ACTIONS)
    for s in state_subset:
        if s==MDP.Terminal_state: continue
        n_states += 1
        try:
            a_VI = POLICY_from_VI[s]
            a_QL = POLICY_from_QL[s]
            if a_VI==a_QL: match_count += 1
        except: pass
    return (match_count, n_states, match_count / n_states)

def compare_state_vals(state_subset):
    sum_sq_diffs = 0.0
    n_states = 0
    for s in state_subset:
        if s==MDP.Terminal_state: continue
        n_states += 1
        v_VI = MDP.V_from_VI[s]
        v_QL = MDP.V_from_QL[s]
        sum_sq_diffs += (v_VI - v_QL)**2
    mean_sq_error = sum_sq_diffs / n_states
    return mean_sq_error

def compare_q_vals(state_subset):
    sum_sq_diffs = 0.0
    n_q_vals = 0
    for s in state_subset:
        if s==MDP.Terminal_state: continue
        for a in MDP.ACTIONS:
            try:
                q_VI = MDP.Q_from_VI[(s,a)]
                q_QL = MDP.Q_from_QL[(s,a)]
                sum_sq_diffs += (q_VI - q_QL)**2
                n_q_vals += 1
            except: pass
    mean_sq_error = sum_sq_diffs / n_q_vals
    return mean_sq_error
   
    
