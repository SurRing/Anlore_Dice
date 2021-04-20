import re
import DDL

ddl_reg = "^/ddl (\d+) (.+)"

def match(s):
    m = re.match(ddl_reg,s)
    if m==None:
        return "你谁啊？"
    m_session, success = DDL.login(m[1],m[2])
    if success:
        return DDL.format_ddl(DDL.get_ddl(m_session))
    else:
        return "哎呀登录失败了"


def process(s, name):
    return match(s)