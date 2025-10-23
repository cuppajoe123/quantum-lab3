from state import State, run


def run_task():
    state = State(1)
    state.x(0).h(0)
    print(state)
    state.t(0).t(0).t(0).t(0).t(0).t(0).t(0).t(0)
    print(state)
