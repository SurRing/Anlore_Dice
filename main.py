from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio

from graia.application.message.elements.internal import Plain
from graia.application.friend import Friend

import category

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

@bcc.receiver("FriendMessage")
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    s = category.process(message.asDisplay(), friend.nickname)
    if s != None:
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(s)
        ]))

app.launch_blocking()
