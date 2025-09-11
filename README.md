# Lab 3

## Tasks

1. Verify the effect of $S$ gate on $|0⟩$, $|1⟩$ and $|+⟩$.

2. Show how phase interferes with amplitude on $|+⟩$. Use $H^2$ and $HSH$. Compare the result with task 1.

3. Prepare state $|-⟩$. Apply T gates on it and get the same state.

4. Create bell states, $|\Phi^+⟩$ and $|\Psi^-⟩$.

5. Create a custom state $|GHZ_3^-⟩ = \frac{1}{\sqrt{2}}(|000⟩ - |111⟩)$.

6. Create a custom state $\frac{1}{\sqrt{2}}(|001⟩ + |110⟩)$.

## Setup

### On Linux/Mac (bash/zsh)

```bash
./setup.sh
source .venv/bin/activate
```

### On Windows (Command Prompt)

```powershell
.\setup.bat
.venv\Scripts\activate.bat
```

## Usage

`state.py` provides the implementation of our quantum simulation.

To initialize a circuit with 2 qubits and 2 classical bits, create a state as follows.

```python
from state import State

state = State(n_qubits=2, n_bits=2)
```

Check the script for implemented gates and how to use them. As an example, you can apply a T Gate on a qubit as follows.

```python
from state import State, run

# Create a single qubit circuit
state = State(1)

# Apply T Gate, which doesn't affect |0⟩ but changes the phase of |1⟩ by pi/4
state.t(0)

# Measure the value on the qubit
state.measure(0)

# Or, Use measure_all to measure all qubits in the state
# state.measure_all()

# Run 1000 times
results = run(state, 1000)
print(results)
```

Use `print` to print the quantum state.

```python
print(state)

# Outputs as follows
"""
>>> print(state)
Quantum state:
0: 1.00+0.00j
1: 0.00+0.00j
"""
```

`tasks` directory contains the task files, where you need to write your code inside the `run_task` function.

To test your output, run the following command:

```bash
python3 main.py <task number> # Replace task number with the number
```

For example, first task's answer should be written in `tasks/task1.py` file. To run it, use the following command.

```bash
python3 main.py 1
```
