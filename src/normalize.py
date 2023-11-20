import copy
import json
import numpy as np


def sexPartDetection(actions, threshold):
    start_pts = [actions[0]['at']]
    end_pts = []
    for i in range(len(actions) - 1):
        t0 = actions[i]['at']
        t1 = actions[i+1]['at']
        if t1 - t0 > threshold:
            end_pts.append(t0)
            start_pts.append(t1)
    end_pts.append(actions[-1]['at'])
    print('Detected ' + str(len(start_pts)) + ' sex parts')
    return start_pts, end_pts


def trimMusicScript(json_music, start_pts, end_pts):
    actions = json_music['actions']
    l_init = len(actions)
    for i in reversed(range(l_init - 1)):
        t0 = actions[i]['at']
        t1 = actions[i+1]['at']
        judge0 = [s < t0 < e for s, e in zip(start_pts, end_pts)]
        judge1 = [s < t1 < e for s, e in zip(start_pts, end_pts)]
        judge = any([max(z) for z in zip(judge0, judge1)])
        if judge:
            del actions[i]
    l_fin = len(json_music['actions'])
    print('Trimmed music script: from ' + str(l_init) + ' to ' + str(l_fin))


def calcAvVelocity(json_load, start_pts, end_pts, music):
    actions = json_load['actions']
    delta_t = 0
    delta_z = 0
    for i in range(len(actions) - 1):
        t0 = actions[i]['at']
        t1 = actions[i+1]['at']
        judge0 = [s < t0 < e for s, e in zip(start_pts, end_pts)]
        judge1 = [s < t1 < e for s, e in zip(start_pts, end_pts)]
        judge = any([min(z) for z in zip(judge0, judge1)])
        if (music and not judge) or (not music and judge):
            delta_t += t1 - t0
            delta_z += np.abs(actions[i+1]['pos'] - actions[i]['pos'])
    return delta_z / delta_t


# file_name: base file name used for the final output
def normalize(file_name, threshold=2000):
    file_music = file_name.replace('].funscript', ']_music.funscript')
    file_sex_part = file_name.replace(
        '].funscript', ']_sex_part.funscript')
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

    # sex part detection and trimming
    start_pts, end_pts = sexPartDetection(json_sex_part['actions'], threshold)
    trimMusicScript(json_music, start_pts, end_pts)

    # average velocity calculation and check
    v_music = calcAvVelocity(json_music, start_pts, end_pts, music=True)
    v_sex_part = calcAvVelocity(json_sex_part, start_pts, end_pts, music=False)
    if v_music < v_sex_part:
        print('v_music < v_sex_part. No normalization is executed')
        exit()

    # normalization
    r = v_sex_part / v_music
    actions_music = json_music['actions']
    for action in actions_music:
        action['pos'] = int(0.5 * range * (1-r) + action['pos'] * r)

    # combine two script actions
    actions_sex_part = json_sex_part['actions']
    actions = actions_music + actions_sex_part
    sorted_actions = sorted(actions, key=lambda action: action['at'])

    # preserve the result to a funscript
    json_output = {'actions': sorted_actions, 'inverted': inverted,
                   'metadata': metadata, 'range': range, 'version': version}
    json_open = open(file_name, mode='w')
    json.dump(json_output, json_open)

    print('Music part is normalized with the weight ' +
          str(r) + ' and parts are combined')
