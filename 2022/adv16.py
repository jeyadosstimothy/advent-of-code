import sys
import json
import random

idx_mapping = {}
rev_idx_mapping = {}

flow_dict = {}

graph = {}

def valve_to_index(valve):
    if(valve in idx_mapping):
        return idx_mapping[valve]
    valve_idx = len(idx_mapping)
    idx_mapping[valve] = valve_idx
    return valve_idx

def index_to_valve(idx):
    return rev_idx_mapping[idx]

for line in sys.stdin:
    valve_flow, leads_to = line.strip().split(';')

    valve, flow = valve_flow.strip().split('=')
    valve = valve.strip()
    flow = int(flow.strip())

    valve_idx = valve_to_index(valve)

    flow_dict[valve_idx] = flow

    leads_to = [dest_valve.strip() for dest_valve in leads_to.strip().split(',')]
    leads_to_num = []
    for dest_valve in leads_to:
        leads_to_num.append(valve_to_index(dest_valve))
    graph[valve_idx] = leads_to_num

rev_idx_mapping = {v:k for k, v in idx_mapping.items()}
print(json.dumps(idx_mapping))

start_valve = 'AA'

dp = {}

def init_dp(valve_idx_1, valve_idx_2, closed_valves, instant):
    if(valve_idx_1 not in dp):
        dp[valve_idx_1] = {}
    if(valve_idx_2 not in dp[valve_idx_1]):
        dp[valve_idx_1][valve_idx_2] = {}
    if(closed_valves not in dp[valve_idx_1][valve_idx_2]):
        dp[valve_idx_1][valve_idx_2][closed_valves] = {}
    if(instant not in dp[valve_idx_1][valve_idx_2][closed_valves]):
        dp[valve_idx_1][valve_idx_2][closed_valves][instant] = -1

def memoized(valve_idx_1, valve_idx_2, closed_valves, instant):
    init_dp(valve_idx_1, valve_idx_2, closed_valves, instant)
    if(dp[valve_idx_1][valve_idx_2][closed_valves][instant] != -1):
        return dp[valve_idx_1][valve_idx_2][closed_valves][instant]
    
    init_dp(valve_idx_2, valve_idx_1, closed_valves, instant)
    if(dp[valve_idx_2][valve_idx_1][closed_valves][instant] != -1):
        return dp[valve_idx_2][valve_idx_1][closed_valves][instant]

    return -1

def memoize(valve_idx_1, valve_idx_2, closed_valves, instant, value):
    init_dp(valve_idx_1, valve_idx_2, closed_valves, instant)
    dp[valve_idx_1][valve_idx_2][closed_valves][instant] = value

    init_dp(valve_idx_2, valve_idx_1, closed_valves, instant)
    dp[valve_idx_2][valve_idx_1][closed_valves][instant] = value

def get_open_valves(closed_valves):
    i = 0
    open_valves = []
    closed_valves = closed_valves | (1 << len(graph))
    while closed_valves != 0:
        if(closed_valves & 1 == 0):
            open_valves.append(i)
        i = i + 1
        closed_valves = closed_valves >> 1
    return sorted(open_valves, key=lambda valve: flow_dict[valve], reverse=True)

counter = 0

def find_max_pressure(
    graph,
    shortest_paths,
    valve_idx_1,
    valve_idx_2,
    closed_valves,
    time_limit,
    instant=0,
    curr_path=[], 
    result_path=[]):

    global counter
    counter = counter + 1
    
    memoized_result = memoized(valve_idx_1, valve_idx_2, closed_valves, instant)

    if counter % 10**7 == 0:
        print(
            counter,
            memoized_result,
            bin(closed_valves),
            instant,
            curr_path,
            (index_to_valve(valve_idx_1), index_to_valve(valve_idx_2)),
            result_path)
    
    if(memoized_result != -1):
        return memoized_result
    # print(bin(closed_valves), bin((1<<len(graph)) - 1))
    if(closed_valves == (1<<len(graph)) - 1):
        result = (0, result_path) 
        # print(result)
        memoize(valve_idx_1, valve_idx_2, closed_valves, instant, result)
        return result

    if(instant == time_limit):
        result = (0, result_path)
        # print(result)
        memoize(valve_idx_1, valve_idx_2, closed_valves, instant, result)
        return result
    
    max_pressure = 0
    max_path = result_path

    curr_valve_1_is_open = (closed_valves >> valve_idx_1) & 1 == 0
    curr_valve_2_is_open = (closed_valves >> valve_idx_2) & 1 == 0

    if curr_valve_1_is_open and curr_valve_2_is_open and valve_idx_1 != valve_idx_2:
        next_instant = instant + 1
        expected_pressure_release_valve_1 = (time_limit - next_instant) * flow_dict[valve_idx_1]
        new_closed_valves = (closed_valves | (1 << valve_idx_1))
        expected_pressure_release_valve_2 = (time_limit - next_instant) * flow_dict[valve_idx_2]
        new_closed_valves = (new_closed_valves | (1 << valve_idx_2))
        new_result_path = result_path + [
            ((time_limit - next_instant), flow_dict[valve_idx_1], index_to_valve(valve_idx_1)),
            ((time_limit - next_instant), flow_dict[valve_idx_2], index_to_valve(valve_idx_2)),
        ]
        max_pressure_dest_valve, max_path_dest_valve = find_max_pressure(
            graph, 
            shortest_paths,
            valve_idx_1,
            valve_idx_2,
            new_closed_valves,
            time_limit,
            next_instant,
            curr_path,
            new_result_path)
        if(expected_pressure_release_valve_1 + expected_pressure_release_valve_2 + max_pressure_dest_valve > max_pressure):
            max_pressure = expected_pressure_release_valve_1 + expected_pressure_release_valve_2 + max_pressure_dest_valve
            max_path = max_path_dest_valve
    
    if curr_valve_1_is_open:
        next_instant = instant + 1
        expected_pressure_release_valve_1 = (time_limit - next_instant) * flow_dict[valve_idx_1]
        new_closed_valves = (closed_valves | (1 << valve_idx_1))
        new_result_path = result_path + [((time_limit - next_instant), flow_dict[valve_idx_1], index_to_valve(valve_idx_1))]

        for open_valve_idx in get_open_valves(closed_valves):
            if(open_valve_idx == valve_idx_2):
                continue
            distance_and_path = shortest_paths[valve_idx_2][open_valve_idx]
            distance = distance_and_path['distance']
            path = distance_and_path['path']
            new_curr_path = curr_path + ['2.'+index_to_valve(path[0])]
            max_pressure_dest_valve, max_path_dest_valve = find_max_pressure(
                graph,
                shortest_paths,
                valve_idx_1,
                path[0],
                new_closed_valves,
                time_limit,
                next_instant,
                new_curr_path,
                new_result_path)
            
            if(expected_pressure_release_valve_1 + max_pressure_dest_valve > max_pressure):
                max_pressure = expected_pressure_release_valve_1 + max_pressure_dest_valve
                max_path = max_path_dest_valve
    
    if curr_valve_2_is_open:
        next_instant = instant + 1
        expected_pressure_release_valve_2 = (time_limit - next_instant) * flow_dict[valve_idx_2]
        new_closed_valves = (closed_valves | (1 << valve_idx_2))
        new_result_path = result_path + [((time_limit - next_instant), flow_dict[valve_idx_2], index_to_valve(valve_idx_2))]

        for open_valve_idx in get_open_valves(closed_valves):
            if(open_valve_idx == valve_idx_1):
                continue
            distance_and_path = shortest_paths[valve_idx_1][open_valve_idx]
            distance = distance_and_path['distance']
            path = distance_and_path['path']
            new_curr_path = curr_path + ['1.'+index_to_valve(path[0])]
            max_pressure_dest_valve, max_path_dest_valve = find_max_pressure(
                graph,
                shortest_paths,
                path[0],
                valve_idx_2,
                new_closed_valves,
                time_limit,
                next_instant,
                new_curr_path,
                new_result_path)
            if(expected_pressure_release_valve_2 + max_pressure_dest_valve > max_pressure):
                max_pressure = expected_pressure_release_valve_2 + max_pressure_dest_valve
                max_path = max_path_dest_valve

    for open_valve_idx_1 in get_open_valves(closed_valves):
        if(open_valve_idx_1 == valve_idx_1):
            continue
        distance_and_path_1 = shortest_paths[valve_idx_1][open_valve_idx_1]
        distance_1 = distance_and_path_1['distance']
        path_1 = distance_and_path_1['path']

        for open_valve_idx_2 in get_open_valves(closed_valves):
            if(open_valve_idx_2 == valve_idx_2):
                continue
            
            # if(open_valve_idx_1 == open_valve_idx_2):
            #     continue

            distance_and_path_2 = shortest_paths[valve_idx_2][open_valve_idx_2]
            distance_2 = distance_and_path_2['distance']
            path_2 = distance_and_path_2['path']
            if(instant + min(distance_1, distance_2) > time_limit):
                continue

            if(distance_1 < distance_2):
                next_instant = instant + distance_1
                new_curr_path = curr_path + [val for i, j in zip(path_1, path_2[:distance_1]) for val in ('1.'+index_to_valve(i), '2.'+index_to_valve(j))]
                max_pressure_dest_valve, max_path_dest_valve = find_max_pressure(
                    graph,
                    shortest_paths,
                    open_valve_idx_1,
                    path_2[distance_1 - 1],
                    closed_valves,
                    time_limit,
                    next_instant,
                    new_curr_path,
                    result_path)
                if(max_pressure_dest_valve > max_pressure):
                    max_pressure = max_pressure_dest_valve
                    max_path = max_path_dest_valve
            elif(distance_1 > distance_2):
                next_instant = instant + distance_2
                new_curr_path = curr_path + [val for i, j in zip(path_1[:distance_2], path_2) for val in ('1.'+index_to_valve(i), '2.'+index_to_valve(j))]
                max_pressure_dest_valve, max_path_dest_valve = find_max_pressure(
                    graph,
                    shortest_paths,
                    path_1[distance_2 - 1],
                    open_valve_idx_2,
                    closed_valves,
                    time_limit,
                    next_instant,
                    new_curr_path,
                    result_path)
                if(max_pressure_dest_valve > max_pressure):
                    max_pressure = max_pressure_dest_valve
                    max_path = max_path_dest_valve
            else:
                next_instant = instant + distance_2
                new_curr_path = curr_path + [val for i, j in zip(path_1, path_2) for val in ('1.'+index_to_valve(i), '2.'+index_to_valve(j))]
                max_pressure_dest_valve, max_path_dest_valve = find_max_pressure(
                    graph,
                    shortest_paths,
                    open_valve_idx_1,
                    open_valve_idx_2,
                    closed_valves,
                    time_limit,
                    next_instant,
                    new_curr_path,
                    result_path)
                if(max_pressure_dest_valve > max_pressure):
                    max_pressure = max_pressure_dest_valve
                    max_path = max_path_dest_valve

    # print(curr_valve_1_is_open, curr_valve_2_is_open, max_pressure, max_path)
    memoize(valve_idx_1, valve_idx_2, closed_valves, instant, (max_pressure, max_path))
    return (max_pressure, max_path)

def calculate_shortest_paths(graph):
    shortest_paths = {}
    for start in graph.keys():
        shortest_paths[start] = {}
        visited = set([start])
        queue = [(start, 0, [])]
        while(len(queue) != 0):
            curr, dist, path = queue[0]
            queue = queue[1:]
            shortest_paths[start][curr] = {'distance': dist, 'path': path}
            for next in graph[curr]:
                if(next in visited):
                    continue
                visited.add(next)
                queue.append((next, dist + 1, path + [next]))
    return shortest_paths

shortest_paths = calculate_shortest_paths(graph)
print(json.dumps(shortest_paths))

closed_valves = 0
for valve_idx, flow in flow_dict.items():
    if(flow == 0):
        closed_valves = closed_valves | (1 << valve_idx)

max_pressure, max_path = find_max_pressure(graph, shortest_paths, valve_to_index('AA'), valve_to_index('AA'), closed_valves, 26, curr_path=['1.AA', '2.AA'])
print(counter, max_pressure, max_path)

# OA=0; VP, VM
# GA=13; KV
# WD=0; SH, XQ
# TE=0; OY, DO
# JR=0; TR, LY
# JQ=0; TD, DZ
# VH=6; WY, YQ, NU
# NX=0; XQ, MN
# XL=0; AA, FA
# QY=0; NU, DO
# KV=0; GA, XQ
# NK=0; XW, XQ
# JU=0; QH, TB
# XZ=0; AA, SH
# XQ=18; GK, NX, WD, KV, NK
# VM=19; LY, OA, OY, AE
# LE=0; MN, NS
# HO=0; GO, QH
# PX=0; MN, VP
# MN=4; LE, UX, TB, NX, PX
# VB=0; XM, AA
# VP=21; XM, WT, BG, PX, OA
# KI=15; XU, MT
# NU=0; QY, VH
# WT=0; SH, VP
# OY=0; VM, TE
# VS=0; QH, SH
# XM=0; VB, VP
# HI=17; TD
# TB=0; JU, MN
# BG=0; VP, GK
# HN=16; BO
# MT=0; KI, BO
# OX=0; DZ, ZF
# QH=5; FA, DW, VS, JU, HO
# YQ=0; VH, AE
# DW=0; ML, QH
# WY=0; HS, VH
# GO=0; HO, DO
# UX=0; AA, MN
# AE=0; YQ, VM
# DZ=9; HS, OX, JQ
# NS=0; SH, LE
# LY=0; JR, VM
# BO=0; HN, MT
# HS=0; WY, DZ
# XW=0; NK, AA
# DO=11; TE, XU, ZF, QY, GO
# FA=0; XL, QH
# AA=0; VB, XL, XZ, XW, UX
# VW=14; ML
# SH=8; NS, WT, XZ, VS, WD
# XU=0; DO, KI
# ZF=0; OX, DO
# GK=0; XQ, BG
# ML=0; VW, DW
# TD=0; HI, JQ
# TR=25; JR


