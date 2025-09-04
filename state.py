"""
Quantum state simulator using functional programming techniques.
This module implements a quantum state class that supports various quantum gates
and operations without requiring matrix algebra.
"""

from math import sqrt, pi
from cmath import exp
import random
from typing import Optional, Dict
from functional import seq
from bitarray import frozenbitarray as bitarray
from bitarray import bitarray as mut_bitarray


# Helper functions for bit manipulation
def set_bit(x: bitarray, i: int, v: int) -> bitarray:
    """Set the i-th bit of bitarray x to value v (0 or 1)"""
    new = mut_bitarray(x)
    new[i] = v
    return bitarray(new)


def flip(x: bitarray, i: int) -> bitarray:
    """Flip (negate) the i-th bit of bitarray x"""
    mask = bitarray("0" * i + "1" + "0" * (len(x) - i - 1))
    return x ^ mask


class State:
    """
    Quantum state using a dictionary-like structure mapping bitstrings to amplitudes.
    """

    def __init__(self, n_qubits: int, n_bits: int = 0):
        """
        Initialize a quantum state with n_qubits qubits and n_bits classical bits.

        Args:
            n_qubits: Number of qubits in the system
            n_bits: Number of classical bits for measurement results

        The state starts in 0...0 (ground state).
        """
        assert n_qubits > 0 and n_bits >= 0

        self.n_qubits = n_qubits
        self.n_bits = n_bits  # Fixed: was m_bits
        self.state = seq(
            [
                (bitarray(format(i, f"0{n_qubits}b")), 1.0 if i == 0 else 0.0)
                for i in range(2**n_qubits)
            ]
        )
        self.cbits = [0] * n_bits
        self.measurement_qubits = set()  # Track which qubits should be measured
        self.measure_all_flag = False  # Track if measure_all was called

    def copy(self):
        """Returns a deep copy of the State object."""
        new_state = State(self.n_qubits, self.n_bits)
        new_state.state = seq(self.state)
        new_state.cbits = list(self.cbits)
        new_state.measurement_qubits = set(self.measurement_qubits)
        new_state.measure_all_flag = self.measure_all_flag
        return new_state

    def x(self, j: int):
        """
        Apply the NOT gate to the j-th qubit.

        This gate flips the basis states where qubit j is present.
        """
        print(f"-> Applying X gate to qubit {j}")
        self.state = self.state.smap(lambda b, a: (flip(b, j), a))
        return self

    def cx(self, j: int, k: int):
        """
        Apply the CX (controlled-NOT) gate with control qubit ctrl (j) and target (k) qubit trgt.
        """
        print(f"-> Applying CX gate with control {j} and target {k}")
        self.state = self.state.smap(lambda b, a: (b if not b[j] else flip(b, k), a))
        return self

    def s(self, j: int):
        """
        Apply the S (phase) gate to the j-th qubit.
        """
        print(f"-> Applying S gate to qubit {j}")
        self.state = self.state.smap(lambda b, a: (b, (1j ** b[j]) * a))
        return self

    def t(self, j: int):
        """
        Apply the T gate to the j-th qubit.
        """
        print(f"-> Applying T gate to qubit {j}")
        phase = exp(1j * pi / 4)
        self.state = self.state.smap(lambda b, a: (b, (phase ** b[j]) * a))
        return self

    def h(self, j: int):
        """
        Apply the Hadamard gate to the j-th qubit.
        """
        print(f"-> Applying Hadamard gate to qubit {j}")
        norm = 1 / sqrt(2)
        # Fixed: Corrected the phase factor
        self.state = (
            self.state.smap(
                lambda b, a: [
                    (set_bit(b, j, 0), a * norm),
                    (set_bit(b, j, 1), a * norm * ((-1) ** b[j])),  # Fixed phase
                ]
            )
            .flatten()
            .reduce_by_key(lambda x, y: x + y)
        )
        return self

    def measure(self, j: int, cbit: Optional[int] = None):
        """
        Mark the j-th qubit for measurement (deferred measurement).
        The actual measurement will be performed when run() is called.

        Args:
            j: Index of qubit to measure
            cbit: Optional classical bit to store the measurement result
        """
        print(f"-> Adding measurement for qubit {j}")
        self.measurement_qubits.add(j)
        return self

    def measure_all(self):
        """
        Mark all qubits for measurement (deferred measurement).
        The actual measurement will be performed when run() is called.
        """
        print("-> Adding measurement for all qubits")
        self.measure_all_flag = True
        return self

    def get_probabilities(self) -> Dict[str, float]:
        """
        Get the probability distribution of the current quantum state.

        Returns:
            Dictionary mapping bitstrings to their probabilities
        """
        probs = {}
        for bitstring, amplitude in self.state:
            prob = abs(amplitude) ** 2
            if prob > 1e-10:  # Ignore very small probabilities
                probs[bitstring.to01()] = prob
        return probs

    def __str__(self):
        """
        Return a string representation of the quantum state.

        Format: Each bitstring with its corresponding amplitude.
        """
        self.state = self.state.sorted(key=lambda x: x[0].to01())

        # Only show non-zero amplitudes
        non_zero_states = [(b, a) for b, a in self.state if abs(a) > 1e-10]

        if not non_zero_states:
            result = "Quantum state: |0⟩^n (all zero amplitudes)"
        else:
            result = "Quantum state:\n" + "\n".join(
                [f"|{b.to01()}⟩: {a:.3f}" for b, a in non_zero_states]
            )

        # Add classical register values if they exist
        if self.n_bits > 0:
            result += f"\n\nClassical register: {''.join(map(str, self.cbits))}"

        return result


def run(state: State, shots: int = 1024) -> Dict[str, int]:
    """
    Run measurements on a prepared quantum state multiple times.
    Only measures qubits that were marked for measurement via measure() or measure_all().

    Args:
        state: A prepared quantum state (circuit already applied)
        shots: Number of measurement shots

    Returns:
        Dictionary mapping measurement outcomes to their counts
    """
    if shots <= 0:
        raise ValueError("Shots must be a positive integer")

    # Check if any measurements were requested
    if not state.measurement_qubits and not state.measure_all_flag:
        raise ValueError(
            "No measurements specified. Use measure() or measure_all() first."
        )

    # Determine which qubits to measure
    if state.measure_all_flag:
        qubits_to_measure = list(range(state.n_qubits))
        print(f"Running {shots} measurements on all qubits...")
    else:
        qubits_to_measure = sorted(list(state.measurement_qubits))
        print(f"Running {shots} measurements on qubits {qubits_to_measure}...")

    counts = {}

    for _ in range(shots):
        # Work on a copy of the state to avoid modifying the original
        temp_state = state.copy()

        # Measure each specified qubit
        result_bits = ["0"] * state.n_qubits
        for qubit in qubits_to_measure:
            # Convert state to a regular list for easier manipulation
            current_state = list(temp_state.state)

            # Compute the probability of measuring 0
            prob_0 = sum(abs(a) ** 2 for b, a in current_state if not b[qubit])

            measurement = int(random.random() >= prob_0)
            result_bits[qubit] = str(measurement)

            # Collapse the state based on measurement
            if measurement == 0:
                # Keep only states where qubit is 0, and normalize
                new_state = [
                    (b, a / sqrt(prob_0))
                    for b, a in current_state
                    if not b[qubit] and prob_0 > 0
                ]
            else:
                # Keep only states where qubit is 1, and normalize
                prob_1 = 1.0 - prob_0
                new_state = [
                    (b, a / sqrt(prob_1))
                    for b, a in current_state
                    if b[qubit] and prob_1 > 0
                ]

            # Convert back to seq
            temp_state.state = seq(new_state)

        # Create result string from measured qubits only
        if state.measure_all_flag:
            result = "".join(result_bits)
        else:
            # Only include measured qubits in result
            result = "".join([result_bits[q] for q in qubits_to_measure])

        counts[result] = counts.get(result, 0) + 1

    # Return sorted dictionary by binary string keys
    return dict(sorted(counts.items()))
