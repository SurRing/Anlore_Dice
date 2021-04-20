"""
/rd
"""
import re
import random

dice_cmd_reg = "^/r(([+-]\d*d\d*)|([+-]\d*))*"
dice_reg = "([+-]?)(\d*)d(\d*)"
num_reg = "(?!\d|d)[+-]?\d+(?!\d|d)"

def match(s):
    global dice_reg
    global num_reg

    if re.match(dice_cmd_reg,s)==None:
        return "不支持的骰子"
    dices = re.findall(dice_reg,s)
    nums = re.findall(num_reg,s)

    res = []

    for dice in dices:
        a=1
        b=100
        if dice[1]!="":
            a=int(dice[1])
        if dice[2]!="":
            b=int(dice[2])
        if a==0 or b==0:
            continue
        if a>100:
            return "你想用骰子淹死Aliy吗？"
        if b>10000:
            return "不行不行，太大了"

        sign = 1
        if dice[0] == '-':
            sign = -1
        for i in range(a):
            res.append(sign*random.randint(1,b))

    for num in nums:
        res.append(int(num))

    return res

def process(s, name):
    nums = match(s)
    if type(nums) != list:
        return nums

    res = name + "投掷了:" + s[1:] + "=%d" % nums[0]
    for x in nums[1:]:
        res += "%+d" % x
    res += "="
    res += str(sum(nums))

    return res
#print(match("/r5d-7d6+3-4"))