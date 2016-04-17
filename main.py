!/usr/bin/env python

import sys
import time
import asyncio
from bilibiliClient import bilibiliClient

class danmuProc(bilibiliClient):
    def __init__(self, roomId):
        super(danmuProc, self).__init__(roomId)

    def commentProc(self, commentUser, commentText):
        cmds=commentText.split('+')
        for cmd in cmds:
            print(commentUser+' 使用了 '+cmd)

        return

danmuji = danmuProc(sys.argv[1])

tasks = [
            danmuji.connectServer() ,
            danmuji.HeartbeatLoop() ,
        ]
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(asyncio.wait(tasks))
except KeyboardInterrupt:
    danmuji.connected = False
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.run_forever()

loop.close()
