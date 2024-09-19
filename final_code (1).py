import itertools
import numpy as np

def admittance_matrix(node_list, spice_parameters):
    node_dictionary = {node: index for index, node in enumerate(node_list)}
    voltage_sources = [params for params in spice_parameters if params[0].startswith('V')]
    matrix_size = len(node_list) + len(voltage_sources)
    
    G_temp = np.zeros((matrix_size, matrix_size))
    
    for name, node1, node2, value in spice_parameters:
        if node1 != '0' and node2 != '0':  
            if node1 in node_dictionary and node2 in node_dictionary:
                i = node_dictionary[node1]
                j = node_dictionary[node2]
                conductance = 1 / float(value)
                
                G_temp[i][i] += conductance
                G_temp[j][j] += conductance
                G_temp[i][j] -= conductance
                G_temp[j][i] -= conductance
    
    voltage_row_index = len(node_list)  # Start adding rows/columns for voltage sources after the node rows
    for name, node1, node2, value in voltage_sources:
        if node1 in node_dictionary:  # Positive terminal
            i = node_dictionary[node1]
            G_temp[i][voltage_row_index] = 1
            G_temp[voltage_row_index][i] = 1

        if node2 in node_dictionary:  # Negative terminal
            j = node_dictionary[node2]
            G_temp[j][voltage_row_index] = -1
            G_temp[voltage_row_index][j] = -1
        elif node2 == '0':  # If negative terminal is grounded
            G_temp[voltage_row_index][voltage_row_index] = 0

        voltage_row_index += 1
    
    return G_temp

def voltage_matrix(node_list, spice_parameters):
    voltage_sources = [params for params in spice_parameters if params[0].startswith('V')]
    voltage_matrix_temp = [[''] for _ in range(len(node_list) + len(voltage_sources))]
    
    for i in range(len(node_list)):
        voltage_matrix_temp[i][0] = f"V{i+1}"
        
    for j in range(len(voltage_sources)):
        voltage_matrix_temp[len(node_list) + j][0] = f"I{j+1}"
        
    return voltage_matrix_temp

def excitation_matrix(node_list, spice_parameters):
    node_dictionary = {node: index for index, node in enumerate(node_list)}
    voltage_sources = [params for params in spice_parameters if params[0].startswith('V')]
    excitation_matrix_temp = np.zeros((len(node_list) + len(voltage_sources), 1))
    
    for name, node1, node2, value in spice_parameters:
        if name.startswith("I"):
            if node1 in node_dictionary:
                i = node_dictionary[node1]
                excitation_matrix_temp[i][0] = float(value)
    
        if name.startswith("V"):
            num_value = int(name[1:])
            excitation_matrix_temp[len(node_list) + num_value - 1][0] = float(value)
    
    return excitation_matrix_temp
            
def nodes(temp_list):
    node_set = set()
    for item in itertools.chain.from_iterable(temp_list):
        if str(item).startswith("n"):
            node_set.add(item)
    
    node_temp_list = sorted(list(node_set), key=lambda x: int(x[1:]))
    return node_temp_list

def linear_equation_solution(G, J):
    G_np = np.array(G, dtype=float)
    J_np = np.array(J, dtype=float)
    V_matrix = np.linalg.solve(G_np, J_np)
    return V_matrix
    
spice_netlist_file = "circuit2.sp"

with open(spice_netlist_file, 'r') as file:
    spice_parameters = [line.split() for line in file]
    
node_list = nodes(spice_parameters)
G = admittance_matrix(node_list, spice_parameters)
V_temp = voltage_matrix(node_list, spice_parameters) 
J = excitation_matrix(node_list, spice_parameters)
V = linear_equation_solution(G, J)

print(f"Admittance matrix : \n{G}")
print(f"Voltage matrix : \n{V_temp}")
print(f"Excitation matrix : \n{J}")

for i in range(len(V_temp)):
    print(f"{V_temp[i][0]} : {V[i][0]}")

