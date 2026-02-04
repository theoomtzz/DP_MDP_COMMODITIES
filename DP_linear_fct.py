import numpy as np
import matplotlib.pyplot as plt

def bang_bang(T: int, w: float):

    """
    Def: Implements the bang-bang controller for the following state equation:
         X_{t+1} = X_t + r * X_t * (1 - a_t)

    Input:
        - T: maturity
        - w: return of the fund

    Output:
        - Array of actions
    """

    # Initialization of the parameters

    # Initialization of the actions matrix
    Actions = np.zeros(T + 1)  # Because time starts at 0
    Actions[-1] = 1  # We consume everything at the end (goal: maximize
                     # consumption, and "a" is the action taken between 0 and 1,
                     # respectively: consume nothing or everything)

    # Initialization of phi
    next_phi = 1  # At the end, phi equals one because we want to consume everything
    previous_phi = None

    # Initialization of the counter for the while loop
    count = 2

    # Bang-bang controller
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


# The choice of T impacts the results of the chosen actions

def plane_equation(Actions, w):

    # Initialization of the parameters

    # Initialize the state
    States = np.ones(len(Actions))
    States[0] = 1000000  # Initialization of the state at 1,000,000 $
    previous_state = States
    i = 0

    # X_{t+1} = X_t + X_t * r * (1 - a)
    # X_{t+2} = X_{t+1} + X_{t+1} * r * (1 - a)

    for i in range(0, len(Actions) - 1):
        States[i + 1] = States[i] + States[i] * w * (1 - Actions[i])
        i += 1

    return States


def total_consumptions(Actions: list, State: list, r: float, T: int):

    # R = sum (r * X_t * a_t)
    R = np.flip(np.cumsum(np.flip(State * Actions * r)))

    return R


def consum_all(T: int):
    """
    Def: Implements a strategy that consists of consuming everything at each time step:
         X_{t+1} = X_t + r * X_t * (1 - a_t)

    Input:
        - T: maturity

    Output:
        - Array of actions
    """

    # Initialization of the parameters

    # Initialization of the actions matrix
    Actions = np.ones(T + 1)  # Because time starts at 0

    return Actions


def main(T, w):


    bang_bang_actions = bang_bang(T, w)
    bang_bang_states = plane_equation(bang_bang_actions, w)
    bang_bang_returns = total_consumptions(bang_bang_actions, bang_bang_states, w, T)

    consum_all_actions = consum_all(T)
    consum_all_states = plane_equation(consum_all_actions, w)
    consum_all_returns = total_consumptions(consum_all_actions, consum_all_states, w, T)

    T = np.array([t + 1 for t in range(0, T + 1)])

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

    ax1.set_title("Total consumption as a function of time (bang-bang)")
    ax1.set(xlabel="Time (Years)", ylabel="Total consumption in Dollars")
    ax1.plot(T, bang_bang_returns, '-', linewidth=0.5)

    ax2.set_title("Action as a function of time (bang-bang)")
    ax2.set(xlabel="Time (Years)", ylabel="Taken action")
    ax2.plot(T, bang_bang_actions, '+', linewidth=0.5)

    ax3.set_title("Total consumption as a function of time (consume all)")
    ax3.set(xlabel="Time (Years)", ylabel="Total consumption in Dollars")
    ax3.plot(T, consum_all_returns, '-', linewidth=0.5)

    ax4.set_title("Action as a function of time (consume all)")
    ax4.set(xlabel="Time (Years)", ylabel="Taken action")
    ax4.plot(T, consum_all_actions, '+', linewidth=0.5)

    plt.show()
    return


main(30, 0.1)
