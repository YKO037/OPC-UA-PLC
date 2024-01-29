from opcua import Client
import sys
from time import time


client = Client("opc.tcp://localhost:4840")
client.connect()

root_node = client.get_root_node()
objects = root_node.get_children()

# for obs in objects:
#     print(obs.get_path())

plc_vars = []  # Enter your variable names here
node_path = [] # Enter your node path here. It should be a list of strings.


"""Function to read all the variables from the plc."""

def read_from_opc(path):
    
    for var in plc_vars:
        var_node = root_node.get_child(path + [str(var)])
        value = var_node.get_value()
        print(f"{var} = {value}")


"""Function to write variables from the plc."""

def write_to_opc(path):
    print("")
    print("*********************PLC Variables*************************")
    print("")
    print(", ".join(plc_vars))

    user_selection = input("Enter the name/names of the variables you want to write from the list above. Multiple variable should be comma separated:\n")
    user_selection_list = user_selection.split(", ")

    for item in user_selection_list:
        if item in plc_vars:
           continue
        else:
            print("Variable name is invalid.")
            sys.exit()
           
    var_value = int(input("Enter the value of the variable you want to write,for boolean variables enter 0 or 1:\n"))
   
    
    for var in user_selection_list:
        var_node = root_node.get_child(path + [str(var)])
        var_type = var_node.get_data_type_as_variant_type()
        var_node.set_value(var_value, var_type)
       
        
def main():
    print("Welcome to the OPC-UA Plc Program")
    print("")
    print("1. Read all the variables from the plc")
    print("2. Write variables from the plc")
    print("3. Exit")
    print("")
    read_from_opc(node_path)
    continue_to_write = input("Do you want to continue to write the variables to the plc? (y/n): ")

    if continue_to_write.lower() == "y":
        write_to_opc(node_path)
        client.disconnect()
    else:
        print("Exiting the program")
        client.disconnect()
        sys.exit()

main()
