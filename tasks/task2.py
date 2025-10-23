from state import State, run


def run_task():
    state = State(1)
    state.h(0).h(0)
    print(state)

    state = State(1)
    state.h(0).s(0).h(0)
    print(state)

