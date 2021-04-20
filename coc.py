"""
/coc n
"""
import re
import random

coc_reg = "^/coc ?(\d*)"

def match(s):
    m = re.match(coc_reg,s)
    if m==None:
        return "不支持的人体炼成"

    n=5
    if m[1]!="":
        n = int(m[1])
    if n<1:
        return "做不到呢"
    if n>20:
        return "太多了，不可以"

    res = []

    for i in range(n):
        res.append([])
        res[i].append(5 * sum([random.randint(1,6) for x in range(3)]))
        res[i].append(5 * sum([random.randint(1, 6) for x in range(3)]))
        res[i].append(30 + 5 * sum([random.randint(1, 6) for x in range(2)]))
        res[i].append(5 * sum([random.randint(1, 6) for x in range(3)]))
        res[i].append(5 * sum([random.randint(1, 6) for x in range(3)]))
        res[i].append(30 + 5 * sum([random.randint(1, 6) for x in range(2)]))
        res[i].append(5 * sum([random.randint(1, 6) for x in range(3)]))
        res[i].append(30 + 5 * sum([random.randint(1, 6) for x in range(2)]))

    return res

def process(s, name):
    bodys = match(s)
    if type(bodys) != list:
        return bodys

    res = f"{name}进行了人体炼成:\n"
    for line in bodys:
        res += f"力量:{line[0]},体质:{line[1]},体型:{line[2]},敏捷:{line[3]},外貌:{line[4]},智力:{line[5]},意志:{line[6]},教育:{line[7]},总和:{sum(line)}\n"
    res+="注入灵魂吧！"

    return res