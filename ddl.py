import re
import time
import DDL
from sql import DDL_DB

login_reg = "^/ddl login (\d*) (.*)"
cmd_reg = "^/ddl (\w*)"

def match(s, friend):
    m = re.match(login_reg,s)
    if m!=None:
        m = re.match(login_reg,s)
        if m == None:
            return "参数错误"
        _ , suc = DDL.login(m[1],m[2])
        if suc:
            DDL_DB.write_user(friend.id, m[1], m[2])
            return "登陆成功"
        else:
            return "登陆失败"

    m=re.match(cmd_reg,s)
    if m==None:
        return "指令错误"
    if not DDL_DB.check_user(friend.id):
        return "请先登录"

    if m[1]=="check":
        return str(DDL.check_clock_by_user(friend.id))

    elif m[1]=="update":
        user = DDL_DB.read_user(friend.id)
        m_session, success = DDL.login(user[1], user[2])
        if success:
            ddls = DDL.update_ddl(m_session, user[0])
            return DDL.format_ddl(ddls)
        else:
            return "哎呀登录失败了"

    elif m[1] == "auto_update":
        DDL_DB.add_auto_update(friend.id)
        return "加入自动更新"
    else:
        return "/ddl login username password 更新登录信息\n" \
               "/ddl check 获取当前dll\n" \
               "/ddl update 更新ddl\n" \
               "/ddl auto_update 加入自动更新"


def process(s, friend):
    return match(s, friend)

