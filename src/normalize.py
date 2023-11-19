import copy
import json
import numpy as np


def calcAvVelocity(json_load):
    actions = json_load['actions']
    delta_t = 0
    delta_z = 0
    for i in range(len(actions) - 1):
        delta_t += actions[i+1]['at'] - actions[i]['at']
        delta_z += np.abs(actions[i+1]['pos'] - actions[i]['pos'])
    return delta_z / delta_t


def sort_actions(action):
    return action['at']


# file_name: base file name used for the final output
def normalize(file_name, gain=1):
    file_music = file_name.replace('].funscript', ']_music.funscript')
    file_sex_part = file_name.replace(
        ']_music.funscript', ']_sex_part.funscript')
    json_open = open(file_music, 'r')
    json_music = json.load(json_open)
    json_open = open(file_sex_part, 'r')
    json_sex_part = json.load(json_open)

    # file check
    key_list = ['inverted', 'range', 'version']
    for key in key_list:
        if (json_music[key] != json_sex_part[key]):
            print('Mismatch of the values of ' + key)
            exit()
    inverted, metadata, range, version = json_music['inverted'], json_music[
        'metadata'], json_music['range'], json_music['version']

    # average velocity calculation and check
    v_music = calcAvVelocity(json_music)
    v_sex_part = calcAvVelocity(json_sex_part)
    if v_music < v_sex_part:
        print('v_music < v_sex_part. No normalization is executed')
        exit()

    # normalization
    r = v_sex_part / v_music * gain
    actions_music = json_music['actions']
    for action in actions_music:
        action['pos'] = int(np.floor(action['pos'] * r))

    # combine two script actions
    actions_sex_part = json_sex_part['actions']
    actions = actions_music + actions_sex_part
    sorted_actions = sorted(actions, key=sort_actions)

    # preserve the result to a funscript
    file_name = file_name.replace(']_music.funscript', '].funscript')
    json_output = {'actions': sorted_actions, 'inverted': inverted,
                   'metadata': metadata, 'range': range, 'version': version}
    json_open = open(file_name, mode='w')
    json.dump(json_output, json_open)
