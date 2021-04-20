import re
import eat
import dice
import coc
import help

cmd_reg = "^/"
eat_reg = "^/eat"
dice_reg = "^/r"
coc_reg = "^/coc"
help_reg = "^/help"

def match(s, name):
    if not re.match(cmd_reg, s):
        return None
    if re.match(eat_reg, s):
        return eat.process(s, name)
    elif re.match(dice_reg, s):
        return dice.process(s, name)
    elif re.match(coc_reg, s):
        return coc.process(s, name)
    elif re.match(help_reg, s):
        return help.process(s, name)

def process(s, name):
    return match(s, name)