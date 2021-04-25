from io import BytesIO
import time
import datetime
import requests
import http.cookiejar as cookielib
import re
from PIL import Image
import CODE
import DES
from sql import DDL_DB


login_url = "https://portal1.ecnu.edu.cn/cas/login?service=https%3A%2F%2Felearning.ecnu.edu.cn%2Fwebapps%2Fcas-hdsfdx-BBLEARN%2Findex.jsp"


def login(username, password):
    print("开始模拟登录大夏学堂")

    print("正在创建cookie")
    m_session = requests.Session()
    # m_session.cookies = cookielib.LWPCookieJar(filename="r_Cookies.txt")
    print("cookie创建完成")

    print("正在获取lt与execution")
    lt, execution = get_params(m_session)
    print("lt与execution获取完成")

    print("正在处理验证码")
    code = get_code(m_session)
    print("验证码处理完成")

    data = {
        'code': code,
        'loginFace': "",
        "rsa": DES.Des(username + password + lt),
        "ul": str(len(username)),
        "pl": str(len(password)),
        "lt": lt,
        "execution": execution,
        '_eventId': "submit"
    }
    print("Data Form数据为：", data)

    print("向登录界面发送报文")
    page = m_session.post(login_url, data=data)
    print("发送报文成功:", page.status_code)
    print(username,password,len(page.headers))
    if len(page.headers) == 16:
        print("登陆成功")
        return m_session, True
    else:
        print("登陆失败")
        return m_session, False


def get_params(m_session):
    page = m_session.get(login_url)
    # print(page.text)
    reg1 = '<input type="hidden" id="lt" name="lt" value="(.+)" />'
    lt = re.findall(reg1, page.text)[0]
    reg2 = '<input type="hidden" name="execution" value="(.+)" />'
    execution = re.findall(reg2, page.text)[0]
    return lt, execution


def get_code(m_session):
    code_msg = m_session.get("https://portal1.ecnu.edu.cn/cas/code")
    pic = Image.open(BytesIO(code_msg.content))
    code = CODE.classify_code(pic)
    return code


def update_ddl(m_session, owner):
    print("开始获取ddl")

    # print("拉取大夏学堂页面")
    # page = m_session.get(tar_url)
    # print(r.text)

    print("获取课程成绩链接")
    courses = get_course_url(m_session)
    print("课程成绩链接获取成功：", courses)

    ddls = {}
    for course in courses:
        ddls[course] = update_course_ddl(m_session, course, courses[course])
    print("已获取到ddl：", ddls)

    print("正在更新信息")
    update_user(owner, ddls)
    print("信息更新完成")

    return ddls


def get_course_url(m_session):
    tar_url = "https://elearning.ecnu.edu.cn/webapps/portal/execute/tabs/tabAction"
    data = {
        "action": "refreshAjaxModule",
        "modId": "_3_1",
        "tabId": "_1_1",
        "tab_tab_group_id": "_30_1"
    }
    page = m_session.post(tar_url, data=data)
    # print(page.text)
    courses = {}
    reg = '<a href=" (.+)" target="_top">(.+)</a>'
    for course in re.findall(reg, page.text):
        courses[course[1]] = "https://elearning.ecnu.edu.cn/webapps/bb-mygrades-BBLEARN/myGrades?course_id=" \
                             + course[0][52:-5] \
                             + "&stream_name=mygrades&is_stream=false"
    # print(courses)

    return courses


def update_course_ddl(m_session, course, url):
    print("开始获取:" + course)
    page = m_session.get(url)
    # print(page.text)

    reg = """    <!-- Calculated Rows -->
      <div id="(.+)" position="(?:.+)" lastactivity="0" duedate="(.+)" class="sortable_item_row upcoming_item_row row expanded">
        
        <!-- Items Column -->
        <div class="cell gradable">
          (.+)<div class="activityType">
              到期日期: (.+)</div>
          <div class="itemCat">(.+)</div>
          <div class="eval-links horizontal">
            </div>
        </div>"""

    ddls = []
    now = time.time()
    for line in re.findall(reg, page.text):
        if int(line[1][:-3]) > now:
            ddls.append(line)

    return ddls


def format_ddl(ddls):
    res = "已为您检索全部未完成ddl，Aliy不对准确性做任何保障，可不要轻信Aliy。\n"
    today = time.time()
    for course in ddls:
        s = ""
        for line in ddls[course]:
            time_label = int(line[1][:-3])
            delta_time = time_label - today
            ddl = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_label))
            s += "任务名称：%s，任务类型：%s，截止时间：%s，剩余时间：%s\n" % (line[2], line[4], ddl, datetime.timedelta(seconds=delta_time))
        if s:
            s = course + ":\n" + s
            res+=s
    return res

def check_clock(time):
    DDL_DB.delete_useless_clock()
    return str(DDL_DB.read_clock_by_time(time))

def update_user(owner, ddls):
    for course in ddls:
        for clock in ddls[course]:
            DDL_DB.write_clock(owner, clock[1], clock[4], clock[0])
