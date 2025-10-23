from state import State, run


def run_task():
    state = State(1)
    state.s(0)
    print(state)

    state = State(1)
    state.x(0)
    state.s(0)
    print(state)

    state = State(1)
    state.h(0)
    state.s(0)
    print(state)

