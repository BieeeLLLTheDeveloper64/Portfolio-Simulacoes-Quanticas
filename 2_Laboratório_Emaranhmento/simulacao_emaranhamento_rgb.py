import matplotlib
matplotlib.use('TkAgg')
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_state_qsphere
import matplotlib.pyplot as plt

def create_bell_state():
    bell_circuit = QuantumCircuit(2)
    bell_circuit.h(0)
    bell_circuit.cx(0, 1)
    return bell_circuit

def show_qsphere(circuit):
    simulator = AerSimulator()
    circuit.save_statevector()
    result = simulator.run(circuit).result()
    statevector = result.get_statevector()
    fig = plot_state_qsphere(statevector)
    plt.show()


if __name__ == "__main__":
    while True:
        print("\nPortas disponíveis: [z0] Z no qubit 0, [z1] Z no qubit 1, [s0] S no qubit 0, [s1] S no qubit 1, [t0] T no qubit 0, [t1] T no qubit 1, [n] Nenhuma, [q] Sair")
        escolha = input("Escolha uma porta para aplicar antes da Q-Sphere: ").strip().lower()
        qc = create_bell_state()
        if escolha == "z0":
            qc.z(0)
        elif escolha == "z1":
            qc.z(1)
        elif escolha == "s0":
            qc.s(0)
        elif escolha == "s1":
            qc.s(1)
        elif escolha == "t0":
            qc.t(0)
        elif escolha == "t1":
            qc.t(1)
        elif escolha == "n":
            pass
        elif escolha == "q":
            break
        else:
            print("Opção inválida.")
            continue
        show_qsphere(qc)
