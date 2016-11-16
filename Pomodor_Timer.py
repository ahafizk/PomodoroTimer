#!/usr/bin/python
from threading import Thread,Lock
import time
import logging
import sys

logger = None #logger object
locker = None #lock object for thead synchronization
SECONDS = 60

def init_logger():
    '''
    this function initialize the logger handler for logging the status of the thread
    '''
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # create a log file handler
    handler = logging.FileHandler('pomodoro.log')
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add file handler to the logger
    logger.addHandler(handler)
    logger.info("Logger Object initialized successfully!")
    # return logger

def init_locker_object():
    global locker
    locker = Lock()
    if logger :
        if locker:
            logger.info("locker object created successfully!")
        else:
            logger.info("Locker object can't created!")


class PomodoroTimer(Thread):

    def __init__(self, thread_id, thread_name):
        #call the parent init method
        Thread.__init__(self)
        #initialize pomodoroTimer properties
        self.thread_id = thread_id
        self.thread_name = thread_name

        self.checkmark = 0 #count the number of Pomodoro Timer
        self.short_break_time = 5*SECONDS # minutes
        self.long_break_time = 15*SECONDS #15 minutes
        self.task_time = 25*SECONDS # 25 minutes

    #override the Thread.run method
    def run(self):

        while(True):
            try:
                locker.acquire() #try to gain the lock to do the task #step 1
                logger.info("New Task Started!")


                task_time = self.init_task() #  step 2
                logger.info("Set Pomodoro timer successfully!")


                self.execute_task(self.task_time) #step 3
                logger.info("Task Executed Successfully!")


                self.put_checkmark() #step 4
                logger.info("Set checkmark for each pomodoro!")

                if (self.checkmark<4): #step 5
                    req = None
                    logger.info("Request user to take a break!")
                    req = self.request_short_break()


                    if  req.lower() =='y':
                        logger.info("Taking break for 5 minutes.")
                        self.take_break(self.short_break_time)
                    elif  req.lower()=='q':
                        logger.info("Quit Pomodoro Timer!")
                        exit() #exit successfully

                    elif req.lower()=='n':
                        logger.info("Continue to work!")
                    else:
                        logger.info("Unknown response from user!")

                elif self.checkmark==4: #step 6
                    logger.info("Reset the number of Pomodoro.")
                    self.reset_checkmark()
                    logger.info("Taking longer ({0} minutes) break.".format(self.long_break_time))
                    self.take_break(self.long_break_time) # take longer break
                locker.release()
            except (KeyboardInterrupt, RuntimeError, ValueError):
                logger.info("Pomodoro Timer terminated!")
                exit(1)


    def request_short_break(self):
        sys.stdout.flush()
        return raw_input("\rDo you want to take a 5 min break? Yes - y, No - n, Quit - q : ")


    def reset_checkmark(self):
        self.checkmark = 0

    def put_checkmark(self):
        self.checkmark = self.checkmark + 1 #increment the checkmark

    def init_task(self):
        return self.task_time # 25 minutes

    def execute_task(self, task_time):
        #execute the task
        #since task was not defined one way of executing task may be sleep for the specified time or checking
        #while loop for a specified amount of time
        # end_time = datetime.now()+ timedelta(minutes=task_time)
        # while (end_time>datetime.now()):
        #     pass
        while(task_time>0):
            sys.stdout.flush()
            sys.stdout.write( "\rWorking: {:02d}:{:02d}".format(*divmod(task_time, 60)))

            logger.info("Working: {:02d}:{:02d} ".format(*divmod(task_time, 60)))
            time.sleep(1)
            task_time = task_time - 1

    def take_break(self,break_time):
        """

        :param break_time: in seconds
        """
        #take a break in a specified time

        logger.info("Taking break for {0} minutes".format(break_time))
        while(break_time>0):
            sys.stdout.flush()
            sys.stdout.write( "\rBreak: {:02d}:{:02d}".format(*divmod(break_time, 60)))

            logger.info("Break: {:02d}:{:02d} ".format(*divmod(break_time, 60)))
            time.sleep(1) # break_time minutes * 60 seconds
            break_time = break_time - 1
        logger.info("Break time End!")




def initialize():
    #initialize logger and locker object
    init_logger()
    init_locker_object()

if __name__=='__main__':

    try:
        # initialize logger and locker objects
        initialize()

        # Create new Pomodoro Timer thread
        thread = PomodoroTimer(1, "Pomodoro Timer")


        # Start new Threads
        logger.info("Pomodoro Timer started.")
        thread.start()

        logger.info("Wait for the Pomodoro Timer to complete.")
        #wait for the thread to complete
        thread.join()


        logger.info("Main thread Completed!")
    except:

        e = sys.exc_info()[0]
        print e
        print "Main Thread Terminated!"