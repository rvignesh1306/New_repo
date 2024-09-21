
# Online Python - IDE, Editor, Compiler, Interpreter
with open('testchip.v', 'r') as file:
    file_contents = file.readlines()

#Extracts the data from module till endmodule  
start_value = None
module_data = []
for i in range(len(file_contents)):
    if file_contents[i].startswith("module"):
        start_value = i
    elif file_contents[i].startswith("endmodule") and start_value is not None:
        module_data.append(file_contents[start_value:i+1])
        start_value = None
        
#creating a dictionary to store the module name and all of it's contents
module_info = {}
for value in module_data:
    key = value[0].split()[1]
    module_info[key] = value
    

count = True
        
def buffer_cell():
    global count
    count_values = data_conditioning(module_info[bufferCell.__name__], count_primitives = {})
    if count == True:
        result = count_and_print(count_values)
        print_final(result)
    else:
        return count_values
    
    
def Cell_1():
    global count
    count_values = data_conditioning(module_info[cellA.__name__], count_primitives= {})
    if count == True:
        result = count_and_print(count_values)
        print_final(result)
    else:
        return count_values
    
        
def Cell_2():
    global count
    count_values = data_conditioning(module_info[cellB.__name__], count_primitives = {})
    if count == True:
        result = count_and_print(count_values)
        print_final(result)
    else:
        return count_values
    
    
def Cell_3():
    global count
    count_values = data_conditioning(module_info[cellC.__name__], count_primitives = {})
    if count == True:
        result = count_and_print(count_values)
        print_final(result)
    else:
        return count_values
    
def Cell_4():
    global count
    count_values = data_conditioning(module_info[cellD.__name__], count_primitives = {})
    if count == True:
        result = count_and_print(count_values)
        print_final(result)
    else:
        return count_values
        
def Main():
    global count
    count_values = data_conditioning(module_info[TopCell.__name__], count_primitives = {})
    if count == True:
        result = count_and_print(count_values)
        print_final(result)
    else:
        return count_values
    
    
mapping_function = { 'bufferCell' : bufferCell,
                     'cellA' : cellA,
                     'cellB' : cellB,
                     'cellC' : cellC,
                     'cellD' : cellD,
                     'TopCell' : TopCell,
    
}
    
    
    
def count_and_print(data):
    global count 
    count = False
    accumulated_data = data.copy()
    for value in list(accumulated_data.keys()):
        if value in mapping_function:
            for _ in range(accumulated_data[value]):
                result = mapping_function[value]()
                for item in list(result.keys()):
                    if item in mapping_function:
                        recursive_result = count_and_print({item: result[item]})
                        #print(recursive_result)
                        for k, v in recursive_result.items():
                                if k in accumulated_data:
                                    accumulated_data[k] += v
                                else:
                                    accumulated_data[k] = v
                    
                for i, j in result.items():
                    if i in mapping_function:
                        continue
                    else:
                        if i in accumulated_data:
                            accumulated_data[i] += j
                        else:
                            accumulated_data[i] = j
                    
    #count = True
    return accumulated_data
    print(accumulated_data)
    
def data_conditioning (data, count_primitives):
    my_list = []
    modified_list = [items.strip() for items in data]
    filtered_list = list(filter(None,[contents for contents in modified_list if not (contents.startswith("//") or contents.startswith("module") or contents.startswith("input") or contents.startswith("output") or contents.startswith("wire") or contents.startswith("endmodule"))]))
    updated_list = [items.split() for items in filtered_list]
    for value in range(len(updated_list)):
        my_list.append(updated_list[value][0])
        
    #my_set = set(my_list)
    for value in my_list:
        if value in count_primitives:
            count_primitives[value] += 1 
        else:
            count_primitives[value] = 1
    return count_primitives

def print_final(item):
    filtered_dict = {key:value for key,value in item.items() if not key.startswith("cell")}    
    for key,value in filtered_dict.items():
        print(f"{key} : {filtered_dict[key]} placements")


module_name = input("Enter the module name")
if module_name in mapping_function:
    mapping_function[module_name]()

    
