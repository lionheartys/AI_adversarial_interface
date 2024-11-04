import os

from flask import Flask, request, jsonify
from functools import wraps
import yaml

def return_0_1(code: int =200 , message: str = "done", data: dict = {"v":"k"}):
    #  this code for returning response of POST(GET) with json format
    response = {
        "code": code,
        "message": message,
        "data": data
    }

    return jsonify(response)


# ## there are several functions about interface POST(GET) key. Every key has a unique function
# def test_model():
#     return  0


def share_weight(contain_id, shared_path):
    ##  this function for sharing weights of one model generated by different adversarial methods.
    return 0

def update_dict_1_level(original, new):
    # just update dict key
    for key, value in new.items():
        if key not in original:
            original[key] = value

def update_dict_2_level(original, new):
    # if new dict's model is same with origin, update the 2 level key 'weight_number', 'weight_name',
    # 'test_method', and 'download_addr'
    for key, value in new.items():
        if key not in original:
            original[key] = value
        else:
            if isinstance(original[key]['weight_number'], int):
                original[key]['weight_number'] = original[key]['weight_number'] + new[key]['weight_number']
            else:
                original[key]['weight_number'] = int(original[key]['weight_number']) + int(new[key]['weight_number'])

            for kkey in ['weight_name', 'test_method', 'download_addr']:
                if isinstance(original[key][kkey], str) and isinstance(new[key][kkey], str):
                    original[key][kkey] = [original[key][kkey], new[key][kkey]]
                elif isinstance(original[key][kkey], list) and isinstance(new[key][kkey], str):
                    original[key][kkey].append(new[key][kkey])
                elif isinstance(original[key][kkey], str) and isinstance(new[key][kkey], list):
                    original[key][kkey] = new[key][kkey].append(original[key][kkey])
                elif isinstance(original[key][kkey], list) and isinstance(new[key][kkey], list):
                    original[key][kkey].extend(new[key][kkey])


def init_read_yaml_for_model():
    yaml_file_path = './config/adver_white_box.yaml'

    with open(yaml_file_path, 'r') as yaml_file:
        data_dict = yaml.safe_load(yaml_file)

    # print(data_dict)

    new_data_dict = os.listdir("./config")
    for item in new_data_dict:
        if item != 'adver_white_box.yaml':
            # print(item)
            with open(os.path.join("./config", item)) as yaml_file:
                new_data = yaml.safe_load(yaml_file)
                update_dict_1_level(data_dict, new_data)

    # print(data_dict)
    return data_dict


def init_read_yaml_for_model_duplicate():
    yaml_file_path = './config/adver_white_box.yaml'

    with open(yaml_file_path, 'r') as yaml_file:
        data_dict = yaml.safe_load(yaml_file)

    # print(data_dict)

    new_data_dict = os.listdir("./config")
    for item in new_data_dict:
        if item != 'adver_white_box.yaml':
            with open(os.path.join("./config", item)) as yaml_file:
                new_data = yaml.safe_load(yaml_file)
                update_dict_2_level(data_dict, new_data)

    # print(data_dict)
    return data_dict

def update_yaml():
    ## do we need this funcion?  To be added
    return 0


if __name__ == "__main__":

    model_dict = init_read_yaml_for_model_duplicate()

    print(model_dict)