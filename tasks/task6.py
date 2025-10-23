from state import State, run


def run_task():
    state = State(3)
    state.h(0).cx(0,2).x(2).cx(0,1)
    print(state)
