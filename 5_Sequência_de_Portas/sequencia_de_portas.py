import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.mplot3d import Axes3D
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

# --- FUNÇÕES ---
def simular_circuito(portas):
    qc = QuantumCircuit(1)
    for gate in portas:
        if gate == 'h':
            qc.h(0)
        elif gate == 'x':
            qc.x(0)
        elif gate == 'y':
            qc.y(0)
        elif gate == 'z':
            qc.z(0)
    qc.save_statevector()
    simulator = AerSimulator()
    result = simulator.run(qc).result()
    statevector = result.get_statevector()
    return statevector.data

def calcular_probabilidades(statevector):
    prob_0 = np.abs(statevector[0]) ** 2
    prob_1 = np.abs(statevector[1]) ** 2
    return prob_0, prob_1

def visualizar_bloch(statevector):
    alpha = statevector[0]
    beta = statevector[1]
    theta = 2 * np.arccos(np.abs(alpha))
    phi = np.angle(beta) - np.angle(alpha)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111, projection='3d')
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    sphere_x = np.outer(np.cos(u), np.sin(v))
    sphere_y = np.outer(np.sin(u), np.sin(v))
    sphere_z = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(sphere_x, sphere_y, sphere_z, color='c', alpha=0.15, linewidth=0)
    ax.quiver(0, 0, 0, x, y, z, length=1.0, color='r', arrow_length_ratio=0.1)
    ax.text(0, 0, 1.3, "|0⟩", fontsize=12)
    ax.text(0, 0, -1.4, "|1⟩", fontsize=12)
    ax.set_title('Visualização do Qubit na Esfera de Bloch', fontsize=16)
    ax.set_aspect('equal')
    plt.show()

# Histórico de simulações
historico = []

def criar_ruido():
    noise_model = NoiseModel()
    error = depolarizing_error(0.05, 1)
    noise_model.add_all_qubit_quantum_error(error, ['x', 'y', 'z', 'h'])
    return noise_model

def simular_circuito(num_qubits, portas, usar_ruido=False):
    qc = QuantumCircuit(num_qubits)
    for idx, gate_seq in enumerate(portas):
        for gate in gate_seq:
            if gate == 'h':
                qc.h(idx)
            elif gate == 'x':
                qc.x(idx)
            elif gate == 'y':
                qc.y(idx)
            elif gate == 'z':
                qc.z(idx)
    qc.save_statevector()
    simulator = AerSimulator()
    noise_model = criar_ruido() if usar_ruido else None
    result = simulator.run(qc, noise_model=noise_model).result()
    statevector = result.get_statevector()
    return statevector.data

def calcular_probabilidades(statevector, num_qubits):
    probs = np.abs(statevector) ** 2
    return probs

def exportar_csv(historico):
    file = filedialog.asksaveasfilename(defaultextension=".csv")
    if file:
        with open(file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Qubits', 'Portas', 'Probabilidades'])
            for h in historico:
                writer.writerow([h['num_qubits'], h['portas'], h['probs']])
        messagebox.showinfo("Exportação", "Resultados exportados com sucesso!")

def explicar():
    msg = (
        "Você pode escolher o número de qubits e aplicar portas (h, x, y, z) em cada um.\n"
        "A simulação pode incluir ruído (erros aleatórios nas portas).\n"
        "O resultado mostra as probabilidades de cada estado possível.\n"
        "O histórico armazena todas as simulações feitas nesta sessão."
    )
    messagebox.showinfo("Explicação", msg)

def rodar_simulacao():
    try:
        num_qubits = int(entry_qubits.get())
        portas = []
        for i in range(num_qubits):
            seq = entries_portas[i].get().lower().replace(" ", "")
            portas.append(seq)
        usar_ruido = var_ruido.get()
        statevector = simular_circuito(num_qubits, portas, usar_ruido)
        probs = calcular_probabilidades(statevector, num_qubits)
        historico.append({'num_qubits': num_qubits, 'portas': portas, 'probs': probs})
        # Se for 1 qubit, mostra a fórmula padrão
        if num_qubits == 1:
            alpha = statevector[0]
            beta = statevector[1]
            formula = f"Estado do qubit: |ψ⟩ = ({alpha:.3f})|0⟩ + ({beta:.3f})|1⟩\n"
        else:
            formula = ""
        resultado = formula + "\n".join([f"|{format(i, f'0{num_qubits}b')}>: {p:.2%}" for i, p in enumerate(probs)])
        text_resultado.config(state='normal')
        text_resultado.delete(1.0, tk.END)
        text_resultado.insert(tk.END, resultado)
        text_resultado.config(state='disabled')
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def atualizar_portas():
    for widget in frame_portas.winfo_children():
        widget.destroy()
    try:
        n = int(entry_qubits.get())
        global entries_portas
        entries_portas = []
        for i in range(n):
            tk.Label(frame_portas, text=f"Portas para qubit {i}:").pack()
            e = tk.Entry(frame_portas)
            e.pack()
            entries_portas.append(e)
    except:
        pass

# GUI
root = tk.Tk()
root.title("Simulador Quântico Completo")

tk.Label(root, text="Número de qubits:").pack()
entry_qubits = tk.Entry(root)
entry_qubits.pack()
entry_qubits.insert(0, "2")
entry_qubits.bind("<Return>", lambda e: atualizar_portas())

frame_portas = tk.Frame(root)
frame_portas.pack()
entries_portas = []
atualizar_portas()

var_ruido = tk.BooleanVar()
tk.Checkbutton(root, text="Simular ruído", variable=var_ruido).pack()

tk.Button(root, text="Rodar Simulação", command=rodar_simulacao).pack(pady = 5)
tk.Button(root, text="Exportar Histórico", command=lambda: exportar_csv(historico)).pack(pady = 5)
tk.Button(root, text="Explicação", command=explicar).pack(pady = 5)

text_resultado = tk.Text(root, height=10, width=50, state='disabled')
text_resultado.pack()

root.mainloop()

# --- BLOCO PRINCIPAL ---
if __name__ == "__main__":
    print("=====================================================")
    print("     Bem-vindo ao Simulador Quântico Interativo!     ")
    print("=====================================================")
    print("Você pode aplicar uma sequência de portas quânticas ao qubit (que começa em |0>).")
    print("Opções de Portas: 'h', 'x', 'y', 'z'")
    print("  'h' (Hadamard): Cria uma superposição (50% |0> e 50% |1>).")
    print("  'x' (Pauli-X): Inverte o estado (Também chamado de Inversor).")
    print("  'y' (Pauli-Y): Rotaciona em torno do eixo Y.")
    print("  'z' (Pauli-Z): Aplica uma mudança de fase.")

    # Pergunta ao usuário por uma sequência de portas
    portas_escolhidas = input("\nDigite a sequência de portas (ex: h, x, y e z) ou (ex: hz, xy ou hx): ").lower().replace(" ", "")

    # Validação para garantir que todas as letras digitadas são válidas
    if not all(gate in 'hxyz' for gate in portas_escolhidas) or not portas_escolhidas:
        print("\nSequência inválida ou vazia! Usando a sequência padrão 'h'.")
        portas_escolhidas = 'h'

    print(f"\n--> Iniciando a simulação com a sequência '{portas_escolhidas}'...")
    final_state_vector = simular_circuito(1, [portas_escolhidas])
    print(f"--> Vetor de Estado Final: {final_state_vector}")
    alpha = final_state_vector[0]
    beta = final_state_vector[1]
    print(f"Estado do qubit: |ψ⟩ = ({alpha:.3f})|0⟩ + ({beta:.3f})|1⟩")

    probabilidades = calcular_probabilidades(final_state_vector, 1)
    prob_0, prob_1 = probabilidades[0], probabilidades[1]
    print("-----------------------------------------------------")
    print("      Probabilidades de Medição      ")
    print(f"--> Chance de encontrar o qubit no estado |0>: {prob_0:.2%}")
    print(f"--> Chance de encontrar o qubit no estado |1>: {prob_1:.2%}")
    print("-----------------------------------------------------")

    print("\n--> Gerando visualização 3D...")
    visualizar_bloch(final_state_vector)
    print("--> Simulação concluída.")