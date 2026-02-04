import numpy as np
import matplotlib.pyplot as plt
def bang_bang(T: int, w: float):

    """

    Def: implement the bang bang controleur for the following plane equation ( Xt+1 = Xt + r * Xt(1-at))
    Input: maturity, return of the fund
    Output: array of action

    """
# Initialisation of the parameters

    # Initialisation of the actions matrix
    Actions = np.zeros(T + 1) # Bc time start at 0 
    Actions[-1] = 1 # We consumme all at the end (goal maximise the 
                  # consumption, and "a" is the action taken between 0 and 1 respectively consum non or all )

    # Initialisation of phi
    next_phi = 1 # at the end phi equal one bc we want to consumme all 
    previous_phi = None

    # Init of the counter for while 
    count = 2

# Bang Bang controler

    while count < T + 2:

        if next_phi < (1 / w):
            Actions[-count] = 1
            previous_phi = 1 + next_phi
       
        else: 
            Actions[-count] = 0
            previous_phi = (1 + w) * next_phi

        next_phi = previous_phi
        count += 1

    return Actions

# The choice of T impact the resulta of the taken action 

def plane_equation(Actions, w):

# Init of the parameter 
    
    #Init State 
    States = np.ones(len(Actions))
    States[0] = 1000000 # Init of the state at 1 000 000 $
    previous_state = States
    i = 0

    # Xt+1 = Xt + Xt * r * ( 1 - a )
    # Xt+2 = Xt+1 + Xt+1 * r * ( 1 - a )

    for i in range(0, len(Actions) - 1):
        States[i + 1] = States[i] + States[i] * w * (1 - Actions[i])
        i += 1

    return(States)



def total_consumptions(Actions: list, State: list, r: float, T: int):

    # R = sum (r * Xt * at)
    R = np.flip(np.cumsum(np.flip(State * Actions * r)))

    return(R)

def consum_all(T: int):
    """

    Def: implement a strategie which consist to consumm all at each time ( Xt+1 = Xt + r * Xt(1-at))
    Input: maturity
    Output: array of action

    """
# Initialisation of the parameters

    # Initialisation of the actions matrix
    Actions = np.ones(T + 1) # Bc time start at 0 

    return Actions

def main(T, w):
    bang_bang_actions = bang_bang(T, w)
    bang_bang_states = plane_equation(bang_bang_actions, w)
    bang_bang_returns = total_consumptions(bang_bang_actions, bang_bang_states, w, T)
    """print(f"Actions: {bang_bang_actions}")
    print(f"States: {bang_bang_states}")
    print(f"Returns: {bang_bang_returns}")"""
    consum_all_actions = consum_all(T)
    consum_all_states = plane_equation(consum_all_actions, w)
    consum_all_returns = total_consumptions(consum_all_actions, consum_all_states, w, T)
    
    T = np.array([t + 1 for t in range(0, T+1)])

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    ax1.set_title("Total consumption as a function of time (bang bang)")
    ax1.set(xlabel = "Time (Years)", ylabel = "Total consumption in Dollars")
    ax1.plot(T, bang_bang_returns, '-', linewidth = 0.5)

    ax2.set_title("Action as a function of time (bang bang)")
    ax2.set(xlabel = "Time (Years)", ylabel = "Taken Action")
    ax2.plot(T, bang_bang_actions, '+', linewidth=0.5)

    ax3.set_title("Total consumption as a function of time (consum all)")
    ax3.set(xlabel = "Time (Years)", ylabel = "Total consumption in Dollars")
    ax3.plot(T, consum_all_returns, '-', linewidth = 0.5)

    ax4.set_title("Action as a function of time (consum all)")
    ax4.set(xlabel = "Time (Years)", ylabel = "Taken Action")
    ax4.plot(T, consum_all_actions, '+', linewidth = 0.5)

    plt.tight_layout()
    plt.show()
    return

main(30 ,0.1)

