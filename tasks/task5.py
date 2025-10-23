from state import State, run


def run_task():
    state = State(3)
    state.h(0).cx(0,1).cx(0,2).s(0).s(0)
    print(state)
