"""
/eat list
/eat choose
/eat rest
/eat add canteen
/eat temp_add canteen
/eat remove canteen
/eat temp_remove canteen
"""
import re
import random

eat_reg = "^/eat (\w*) ?(.*)"
origin_canteen_list = ["河西一楼","河西二楼","河东一楼","河东二楼","黄焖鸡","全家","环球港","饼"]
rest_canteen_list = origin_canteen_list.copy()
help_msg = "当前可用指令包括：\n" \
               "/eat help 也就是这条信息啦！\n" \
               "/eat list 列出全部待选名单。\n" \
               "/eat rest 列出本轮未被选到的名单。\n" \
               "/eat shuffle 重新开始本轮。\n" \
               "/eat choose 从本轮未被选到的名单中随机选出一个。\n" \
               "/eat add canteen 将一个餐厅加入备选名单和本轮名单。\n" \
               "/eat temp_add canteen 将一个餐厅加入本轮名单。\n" \
               "/eat remove canteen 将一个餐厅移出备选名单和本轮名单。\n" \
               "/eat temp_remove canteen 将一个餐厅移出本轮名单。"

def match(s):
    global rest_canteen_list
    m=re.match(eat_reg,s)
    if m==None:
        return "错误指令："+s+"\n请按照/eat {operation} [canteen]输入\n"+help_msg

    if m[1]=="help":
        return help_msg
    elif m[1]=="list":
        return "全体牌库为:"+origin_canteen_list.__str__()
    elif m[1]=="rest":
        return "当前未被抽到的:" + rest_canteen_list.__str__()
    elif m[1]=="shuffle":
        rest_canteen_list = origin_canteen_list.copy()
        return "已重新开始轮次！"
    elif m[1]=="choose":
        if rest_canteen_list==[]:
            rest_canteen_list = origin_canteen_list.copy()
        canteen = random.choice(rest_canteen_list)
        rest_canteen_list.remove(canteen)
        return "Aliy觉得我们今天不如吃%s吧！"%canteen
    elif m[1]=="add":
        origin_canteen_list.append(m[2])
        rest_canteen_list.append(m[2])
        return "Aliy已经把%s加入到备选名单里面啦！"%m[2]
    elif m[1]=="remove":
        origin_canteen_list.remove(m[2])
        rest_canteen_list.remove(m[2])
        return "Aliy已经把%s从备选名单里面去掉啦！"%m[2]
    elif m[1]=="temp_add":
        rest_canteen_list.append(m[2])
        return "Aliy也想多吃一次%s！"%m[2]
    elif m[1]=="temp_remove":
        rest_canteen_list.remove(m[2])
        return "Aliy吃%s的概率变小了。"%m[2]
    else:
        return "错误指令："+s+"\n请按照/eat {operation} [canteen]输入\n"+help_msg

def process(s, name):
    return match(s)