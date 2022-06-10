import threading
import logging
import time
class multithread():
    def __init__(self) -> None:
        print("Multi thread class is created.\nInformation about object:"+
        "There are two type threading method in this class\nFirst one: Logging thread\nSecond one: Printing thread")
    def nothing():
        pass
    def createLogThread(self,fun=nothing,*arg):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        self.logthread = threading.Thread(target=fun, args=arg)
        logging.info("initializing thread")
        self.logthread.start()
    def destoryLogThread(self):
        self.logthread.join()
        print("thread is killed")
    def createPriThread(self,fun=nothing,*arg):
        self.prithread = threading.Thread(target=fun,args=arg)
        print("initializing thread")
        self.prithread.start()
    def destroyPriThread(self):
        self.prithread.join()
        print("thread is killed")