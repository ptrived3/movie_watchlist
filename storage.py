import json
import os 

# read movie data from json file, if file doesnt exist return emoty list
def read_data(file_path):
    if not os.path.exists(file_path):
        return []
    
    # open file in read mode and load json data
    with open(file_path, "r") as file:
        return json.load(file)

# writes movie data to a json file and opens file in write mode and saves data as json    
def write_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


