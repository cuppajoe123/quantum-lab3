# Lab 2

## Tasks

1. Initialize a state with 2 Qubits, and apply $X$ and $X^2$ gates on those qubits respectively. The output should look like as follows.

    ```bash
    Quantum state:
    |10⟩: 1.000
    ```

2. Apply $H$ gate on a qubit and see the output.

3. Apply $H$ gate on two qubits and see the output.

4. Verify $H^2 = I$ property on $|0⟩$ and $|1⟩$

5. Apply $H$ and $CX$ gates to get $|\Phi^+⟩ = \frac{1}{\sqrt{2}}(|00⟩ + |11⟩)$. The output should look like as follows:

    ```bash
    Quantum state:
    |00⟩: 0.707
    |11⟩: 0.707
    ```

6. Similar to task 5, create a three qubit state as $\frac{1}{\sqrt{2}}(|000⟩ + |111⟩)$.

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
