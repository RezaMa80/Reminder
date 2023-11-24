#WORK_TIME=3600
#SNOOZE_TIME=300
#BREAK_TIME=300
#AFK_THRESHOLD=60


from tkinter import Tk, ttk
from pynput import mouse, keyboard

BREAKING = 1
WORKING = 2

def readConfig(config):
    startIndex = configData.index(config) + len(config) + 1
    try:
        endIndex = configData.index('\n', startIndex)
    except ValueError:
        endIndex = len(configData)

    return int(configData[startIndex:endIndex])

def writeWindowStatus(text):
    F_data = open('Data', 'w')
    F_data.write(text)
    F_data.close()

def stop_C():
    writeWindowStatus('Open')
    exit()

def hide_C():
    root.withdraw()
    writeWindowStatus('Show')

def onClosing():
    writeWindowStatus('Open')

def secondToHour(number):
    number = int(number)
    return str(number//60) + ':' + str(number%60)

def popUp():
    root.deiconify()
    root.attributes('-topmost', True)
    root.attributes('-topmost', False)

def clock():
    global second, breakTime, goal
    breakTime += 1

    if breakTime >= AFK_THRESHOLD:
        if breakTime == AFK_THRESHOLD:
            second = min(second, WORK_TIME)

            goal = second//(WORK_TIME/BREAK_TIME)
            second -= AFK_THRESHOLD//(WORK_TIME/BREAK_TIME)
        elif second - WORK_TIME//BREAK_TIME >= 0:
            second -= WORK_TIME//BREAK_TIME
        
        second = max(second, 0)

        L_status.config(text = 'Break for ' + secondToHour(goal))
        L_time.config(text = secondToHour(breakTime))
    else:
        if second >= WORK_TIME:
            if second == WORK_TIME or (second - WORK_TIME)%SNOOZE_TIME == 0:
                L_status.config(text = 'You should take a break')
                popUp()
        else:
            L_status.config(text = 'You\'re working')

        second += 1
        L_time.config(text = secondToHour(second))

    root.after(1000, clock)

def action(arg1 = '', arg2 = '', arg3 = '', arg4 = ''):
    global breakTime
    breakTime = 0

F_data = open('Data')
windowStatus = F_data.read()
F_data.close()

mouse.Listener(on_move = action, on_click = action, on_scroll = action).start()
keyboard.Listener(on_press = action, on_release = action).start()

if windowStatus == 'Open':
    #writeFile('Show')

    F_config = open('Config.txt')
    configData = F_config.read()

    WORK_TIME = readConfig('WORK_TIME')
    SNOOZE_TIME = readConfig('SNOOZE_TIME')
    BREAK_TIME = readConfig('BREAK_TIME')
    AFK_THRESHOLD = readConfig('AFK_THRESHOLD')

    status = WORKING
    second = 0
    breakTime = 0

    root = Tk()

    L_status = ttk.Label(root, text = '')
    L_status.pack()

    L_time = ttk.Label(root, text = 0)
    L_time.pack()

    B_stop = ttk.Button(root, text = 'Stop', command = stop_C)
    B_stop.pack()

    B_Hide = ttk.Button(root, text = 'Hide', command = hide_C)
    B_Hide.pack()

    clock()
    root.protocol("WM_DELETE_WINDOW", onClosing)
    root.mainloop()
else:
    writeWindowStatus('Open')