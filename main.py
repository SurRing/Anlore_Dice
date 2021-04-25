import asyncio
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
from graia.scheduler import GraiaScheduler
from graia.scheduler.timers import crontabify
from graia.application.message.elements.internal import Plain
from graia.application.friend import Friend
import category
import DDL
import time

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080",  # 填入 httpapi 服务运行的地址
        authKey="INITKEYvdfpklX5",  # 填入 authKey
        account=3544812593,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)
scheduler = GraiaScheduler(
    loop, bcc
)

@bcc.receiver("FriendMessage")
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    s = category.process(message.asDisplay(), friend)
    if s != None:
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(s)
        ]))

@scheduler.schedule(crontabify("* * * * * *"))
def something_scheduled():
    now = time.localtime(time.time())
    if now.tm_min==0 and now.tm_sec == 0:
        for clock in DDL.check_clock(now):
            await app.sendFriendMessage(clock[0], MessageChain.create([
                Plain("您的任务：%s将在%s截止"%(clock[2],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(clock[1]))))
            ]))

app.launch_blocking()
