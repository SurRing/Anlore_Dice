"""
/help
"""
import re
import random

help_reg = "^/help"

def match(s):
    return "这里是Aliy！\n" \
           "爱护骰子是每个人的责任，请不要随意禁言或将骰子踢出群聊，这有可能导致骰子被封禁\n" \
           "如果有功能上的意见或建议请联系我的主人Anlore:563424794\n" \
           "/help 显示此文本\n" \
           "/eat help 显示eat模块帮助信息\n" \
           "/r[a=1]d[b=100] 投掷[a]枚[b]面骰\n" \
           "/coc [n=5] 进行[n]次人体炼成\n" \
           "说明:{opt}表示这里是一个必填项，该项将在说明中用{opt}表示，[n=a]表示这里是一个选填项，该项将在说明中用[n]表示，若留空则为默认值a"

def process(s, name):
    return match(s)