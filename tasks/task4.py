from state import State, run


def run_task():
    state = State(2, 2)
    state.h(0).cx(0,1)
    print(state)

    state = State(2)
    state.h(0).x(1).cx(0,1).s(0).s(0)
    print(state)
    
    
