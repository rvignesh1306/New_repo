
import itertools
import numpy as np

def admittance_matrix(node_list, spice_parameters):
    
    global node_dictionary 
    node_dictionary = {node: index for index, node in enumerate(node_list)}
    
    global voltage_sources
    voltage_sources = [voltage_params for voltage_params in spice_parameters if voltage_params[0].startswith('V')]
    matrix_size = len(node_list) + len(voltage_sources) 
    
    G_temp = [[0 for _ in range(matrix_size)] for _ in range(matrix_size)]

    for name, node1, node2, value in spice_parameters:
        if node1 != '0' or node2 != '0':  
            if node1 in node_dictionary and node2 in node_dictionary:
                i = node_dictionary[node1]
                j = node_dictionary[node2]
                conductance = 1 / float(value)
                
                G_temp[i][i] += conductance
                G_temp[j][j] += conductance
                G_temp[i][j] -= conductance
                G_temp[j][i] -= conductance
                
    voltage_row_index = len(node_list)  
    for name, node1, node2, value in voltage_sources:
        if node1 in node_dictionary:
            i = node_dictionary[node1]
            G_temp[i][voltage_row_index] = 1  
            G_temp[voltage_row_index][i] = 1  

        if node2 in node_dictionary:
            j = node_dictionary[node2]
            G_temp[j][voltage_row_index] = -1  
            G_temp[voltage_row_index][j] = -1  
        elif node2 == '0':
            G_temp[voltage_row_index][voltage_row_index] = 0  

        voltage_row_index += 1  

    return G_temp           


def voltage_matrix(node_list, spice_parameters):
    global node_dictionary, voltage_sources
    
    voltage_matrix_temp = [[0] for _ in range(len(node_list) + len(voltage_sources))]
    
    for i in range(len(node_list)):
        voltage_matrix_temp[i][0] = f"V{1+i}"
        
    for j in range(len(voltage_sources)):
        voltage_matrix_temp[len(node_list) + j][0] = f"I{1+j}"
        
    return voltage_matrix_temp
    
def excitation_matrix(node_list, spice_parameters):
    global node_dictionary
    global voltage_sources
    
    excitation_matrix_temp = [[0] for _ in range(len(node_list) + len(voltage_sources))]
    
    for items in spice_parameters:
        name, node1, node2, value = items
        if name.startswith("I"):
            if node1 in node_dictionary:
                i = node_dictionary[node1]
                excitation_matrix_temp[i][0] = value
    
        if name.startswith("V"):
            num_value = name[1:]
            excitation_matrix_temp[len(node_list) + int(name[1:]) - 1][0] = value
            
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
    
    
    
spice_netlist_file = "circuit1.sp"

with open(spice_netlist_file, 'r') as file:
    spice_parameters = []
    for lines in file:
        lines_list = lines.split()
        spice_parameters.append(lines_list)
        #print(lines_list)
    node_list = nodes(spice_parameters)
    G = admittance_matrix(node_list,spice_parameters)
    V_temp = voltage_matrix(node_list,spice_parameters) 
    J = excitation_matrix(node_list, spice_parameters)
    V = linear_equation_solution(G,J)
    print(f"admittance matrix : {G}")
    print(f"Voltage matrix : {V_temp}")
    print(f"exciation matrix : {J}")
    
    
    for i in range(len(V_temp)):
        print(f"{V_temp[i][0]} : {V[i][0]}")
            
                
    

    
    
    
    
                
                
        
        
        
        
        
        

    

        
    
        
        
    
        
        

