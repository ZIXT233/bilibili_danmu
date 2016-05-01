import sys
import time
import queue
import asyncio
import virtkey
import threading
from bilibiliClient import bilibiliClient

class danmuProc(bilibiliClient):
    def __init__(self, roomId):
        super(danmuProc, self).__init__(roomId)
        self.comments = queue.Queue(maxsize=0)
        t = threading.Thread(target=self.cmdProc)
        t.start()
        self.v = virtkey.virtkey()
               
    def _vkey(self, cmd):
        key = {'up':ord("w"),'down':ord("s"),'left':ord("a"),'right':ord("d"),
               'aa':ord("j"),'bb':ord("k"),'start':ord("z"),'select':ord("x")}
        try:
            self.v.press_unicode(key[cmd])
            time.sleep(0.1)
            self.v.release_unicode(key[cmd])
 
        except KeyError:
            return None
        return 1

    def cmdProc(self):
        while(1):
            commentUser, commentText = self.comments.get()
            cmds=commentText.split('+')
            if len(cmds) > 3:
                print(commentUser+' 命令太多啦!')
            for cmd in cmds:
                if not self._vkey(cmd):
                    return 1
                print(commentUser+'使用了'+cmd)
                time.sleep(0.3)
    def commentProc(self, commentUser, commentText):
        self.comments.put((commentUser, commentText))
        return 0

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
