from Tkinter import Tk, Label, Button, StringVar, DISABLED, NORMAL
import tkMessageBox

# import time
SECONDS = 60
MILISECONDS = 1000


class PomodoroTimerUI:
    def __init__(self, root):

        """

        Initialize gui properties and fields
        """
        self.remain_sec = 25 * SECONDS  # is the time for which task will be executed
        self.task_time = 25 * SECONDS
        self.timer_state = False  #
        self.short_break = 5 * SECONDS  #

        #set UI properties
        self.root = root
        root.title("Pomodoro Timer")


        self.root.resizable(width=False, height=False)
        self.root.geometry('{0}x{1}'.format(200, 200))
        self.str_time = StringVar()  # string representation  of the time
        self.str_time.set("Work: {:02d}:{:02d}".format(*divmod(self.task_time, SECONDS)))
        # self.label = Label(self.root, text="{:02d}:{:02d}".format(*divmod(self.task_time * 60, 60)), width=10)
        self.label = Label(self.root, textvariable=self.str_time)
        self.label.pack(fill='x', padx=10, pady=10)
        self.btn_start = Button(self.root, text='Start', command=self.start_timer)
        self.btn_start.pack()
        self.btn_pause = Button(self.root, text='Pause', command=self.pause_timer)
        self.btn_pause.pack()
        self.btn_reset = Button(self.root, text='Reset', command=self.reset_timer)
        self.btn_reset.pack()
        self.btn_reset.configure(state=DISABLED)  # initially reset button keeps disabled
        self.btn_pause.configure(state=DISABLED)  # initially reset button keeps disabled

    def pause_timer(self):
        """
        pause button handler
        :rtype: None
        """
        self.timer_state = not self.timer_state
        self.btn_reset.configure(state=NORMAL)  # activate the reset button
        self.btn_start.configure(state=NORMAL)
        self.btn_pause.configure(state=DISABLED)

    def reset_timer(self):
        """
        reset button handler
        :rtype: None
        """
        self.str_time.set("Work: {:02d}:{:02d}".format(*divmod(self.task_time, SECONDS)))
        self.remain_sec = self.task_time
        self.timer_state = False
        self.btn_start.configure(state=NORMAL)
        self.btn_pause.configure(state=DISABLED)
        self.btn_reset.configure(state=DISABLED)

    def start_timer(self):
        """
        start button handler
        :rtype: None
        """
        self.root.update()
        self.btn_pause.configure(state=NORMAL)
        self.btn_reset.configure(state=DISABLED)
        self.btn_start.configure(state=DISABLED)
        self.timer_state = not self.timer_state
        self.pomo_timer(self.remain_sec)

    def break_timer(self, remain_time):

        """
        Update time when user takes break
        :rtype: None
        """
        if (remain_time > 0):
            self.str_time.set("Break: {:02d}:{:02d}".format(*divmod(remain_time, SECONDS)))
            remain_time = remain_time - 1
            self.root.after(MILISECONDS, self.break_timer, remain_time)  # call break_timer every 1 second
        else:
            self.timer_state = not self.timer_state
            self.btn_start.configure(state=NORMAL)
            self.str_time.set("Work: {:02d}:{:02d}".format(*divmod(self.task_time, SECONDS)))
            self.remain_sec = self.task_time

    def take_break(self, choice=False):

        self.btn_pause.configure(state=DISABLED)
        self.root.update()
        if choice == True:
            print 'Taking 5 minutes break!'
            self.break_timer(self.short_break)

        else:
            self.timer_state = not self.timer_state
            self.btn_start.configure(state=NORMAL)
            self.str_time.set("Work: {:02d}:{:02d}".format(*divmod(self.task_time, SECONDS)))
            self.remain_sec = self.task_time
            self.root.update()

    def pomo_timer(self, remain_sec=None):

        """
        It runs for each pomodoro onece the start button click by the user
        :rtype: None
        """
        if (self.timer_state):
            if remain_sec is not None:

                self.remain_sec = remain_sec  # set the time for the task to be done

            if self.remain_sec <= 0:
                self.str_time.set("Work: 00:00")
                root.update()
                choice = tkMessageBox.askyesno("Choice", "Would you like to take 5 minutes break!")
                self.take_break(choice)

            else:
                self.str_time.set("Work: {:02d}:{:02d}".format(*divmod(self.remain_sec, SECONDS)))
                self.remain_sec = self.remain_sec - 1
                self.root.after(1000, self.pomo_timer)  # call pomo_timer every 1 second


if __name__ == '__main__':
    root = Tk()
    pui = PomodoroTimerUI(root)
    root.mainloop()
