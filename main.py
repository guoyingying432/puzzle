#!/usr/bin/python3.8
import numpy as np
import puzzle
from queue import PriorityQueue,Queue
import time
import math


# 判断当前状态的逆序数
def inverse_num(num, puzzle1):
    row = int(math.sqrt(num + 1))
    tmp = puzzle1.reshape(num + 1)
    tmp = list(tmp)
    tmp.remove(0)
    inverse = 0
    for i in range(num):
        for j in range(num - i - 1):
            if tmp[i] > tmp[i + j + 1]:
                inverse += 1
    return inverse


# 判断奇数阶的puzzle是否有解
def is_sovable(num, puzzle1):
    row = int(math.sqrt(num + 1))
    num = inverse_num(num, puzzle1)
    if num % 2 == 0:
        return True
    else:
        return False
#制造随机数组
def random_beginning(num):
    row = int(math.sqrt(num + 1))
    tmp=np.arange(num+1)
    np.random.shuffle(tmp)
    tmp=tmp.reshape(row,row)
    return tmp

def random_odd_puzzle(num):
    tmp = random_beginning(num)
    while True:
        if is_sovable(num, tmp):
            return tmp
        else:
            print("unsolvable")
puzzle3=random_odd_puzzle(8)
print(puzzle3)

#用A*算法,欧拉函数作为启发函数，实现路径搜索
def A_star_Eular(num,puzzle1):
    standard=puzzle.standard(num)
    open_queue=PriorityQueue()
    #由于set集合不能自动判定ndarray类型的是否相等，所以需要手动判定
    close_queue=[]
    #列表里的第一个元素用来判断优先级，
    # 第二个元素用来存储当前走过多少步，
    # 第三个元素用来判断距离终点的距离，
    # 第四个元素用来保存当前状态，
    # 第五个元素用来保存走过的父节点
    open_queue.put([0+puzzle.Euler_distance(num,puzzle1),0,puzzle.Euler_distance(num,puzzle1),puzzle1,[]])
    close_queue.append(puzzle1)
    while not open_queue.empty():
        current_state=open_queue.get()
        parent_node=[current_state[4]]
        state=current_state[3]
        parent_node.append(state)
        next_state=puzzle.next_state(num,state)
        for states in next_state:
            if puzzle.is_same_array(standard,states):
                parent_node=[parent_node]
                parent_node.append(states)
                return current_state[1]+1,parent_node
            flag=True
            for item in close_queue:
                if puzzle.is_same_array(states,item):
                    flag=False
                    break
            if flag:
                close_queue.append(states)
                open_queue.put([current_state[1]+1+puzzle.Euler_distance(num,states),current_state[1]+1,puzzle.Euler_distance(num,states),states,parent_node])


#用A*算法,欧拉函数作为启发函数，实现路径搜索
def A_star_Manhattan(num,puzzle1):
    standard=puzzle.standard(num)
    open_queue=PriorityQueue()
    #由于set集合不能自动判定ndarray类型的是否相等，所以需要手动判定
    close_queue=[]
    #列表里的第一个元素用来判断优先级，
    # 第二个元素用来存储当前走过多少步，
    # 第三个元素用来判断距离终点的距离，
    # 第四个元素用来保存当前状态，
    # 第五个元素用来保存走过的父节点
    open_queue.put([0+puzzle.Manhattan_distance(num,puzzle1),0,puzzle.Manhattan_distance(num,puzzle1),puzzle1,[]])
    close_queue.append(puzzle1)
    while not open_queue.empty():
        current_state=open_queue.get()
        parent_node=[current_state[4]]
        state=current_state[3]
        parent_node.append(state)
        next_state=puzzle.next_state(num,state)
        for states in next_state:
            if puzzle.is_same_array(standard,states):
                parent_node=[parent_node]
                parent_node.append(states)
                return current_state[1]+1,parent_node
            flag=True
            for item in close_queue:
                if puzzle.is_same_array(states,item):
                    flag=False
                    break
            if flag:
                close_queue.append(states)
                #print(current_state[1]+1)
                open_queue.put([current_state[1]+1+puzzle.Manhattan_distance(num,states),current_state[1]+1,puzzle.Manhattan_distance(num,states),states,parent_node])


#BFS算法
def BFS(num,puzzle1):
    standard = puzzle.standard(num)
    open_queue = Queue()
    close_queue = []
    open_queue.put([puzzle1,[],0])
    while not open_queue.empty():
        current_state = open_queue.get()
        parent_node = [current_state[1]]
        state = current_state[0]
        parent_node.append(state)
        next_state = puzzle.next_state(num, state)
        for states in next_state:
            if puzzle.is_same_array(standard,states):
                parent_node=[parent_node]
                parent_node.append(states)
                return current_state[2]+1,parent_node
            flag=True
            for item in close_queue:
                if puzzle.is_same_array(states,item):
                    flag=False
                    break
            if flag:
                close_queue.append(states)
                #print(current_state[2]+1)
                open_queue.put([states,parent_node,current_state[2]+1])




start=time.perf_counter()
"""
puzzle3=[
    [1,2,3],
    [4,5,6],
    [7,8,0]
]
"""
"""
puzzle1=[
    [5, 2, 3],
    [0, 4, 1],
    [7, 6, 8]
]"""
puzzle1=puzzle3
#step,parent_node=A_star_Manhattan(15,puzzle1)

print("A*Manhattan")
start=time.perf_counter()
step,parent_node=A_star_Manhattan(8,puzzle1)
while parent_node:
    print(parent_node[1])
    parent_node=parent_node[0]
print(step)
end=time.perf_counter()
print("运行时间为：",end-start)
print("A*Eular")
start=time.perf_counter()
step,parent_node=A_star_Eular(8,puzzle1)
while parent_node:
    print(parent_node[1])
    parent_node=parent_node[0]
print(step)
end=time.perf_counter()
print("运行时间为：",end-start)
print("BFS")
start=time.perf_counter()
step,parent_node=BFS(8,puzzle1)
while parent_node:
    print(parent_node[1])
    parent_node=parent_node[0]
print(step)
end=time.perf_counter()
print("运行时间为：",end-start)


