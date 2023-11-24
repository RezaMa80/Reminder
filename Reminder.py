from tkinter import Tk, ttk
from pynput import mouse, keyboard

# Extract value of the given key from data of config file
def readConfig(key):
    startIndex = configData.index(key) + len(key) + 1

    try:
        endIndex = configData.index('\n', startIndex)
        # Last line doesn't have \n so there will be an error
    except ValueError:
        endIndex = len(configData)

    return int(configData[startIndex:endIndex])

# Write the given text to 'Data' file
def writeWindowStatus(text):
    F_data = open('Data', 'w')
    F_data.write(text)
    F_data.close()

# Read the text from given file
def readWindowStatus(file = 'Data'):
    F_data = open(file)
    windowStatus = F_data.read()
    F_data.close()

    return windowStatus

# Close program
def stop_C():
    writeWindowStatus('Open')
    root.destroy()

# Hide window
def hide_C():
    root.withdraw()
    writeWindowStatus('Nothing')

# Return minute:second format of the given seconds
def toClock(number):
    number = int(number)
    hour = str(number//60)
    second = str(number%60)

    if len(hour) < 2:
        hour = '0' + hour

    if len(second) < 2:
        second = '0' + second

    return hour + ':' + second

# Unhide window and bring it to top
def popUp():
    root.deiconify()
    root.attributes('-topmost', True)
    root.attributes('-topmost', False)

# Reset break time
def action(arg1 = '', arg2 = '', arg3 = '', arg4 = ''):
    global breakTime
    breakTime = 0

# Trig every 1 second
def clock():
    global second, breakTime, goal
    breakTime += 1

    # Breaking
    if breakTime >= AFK_THRESHOLD:
        if breakTime == AFK_THRESHOLD:
            popUp()
            second = min(second, WORK_TIME)

            goal = second//(WORK_TIME/BREAK_TIME)
            second -= AFK_THRESHOLD*(WORK_TIME//BREAK_TIME)
        elif second - WORK_TIME//BREAK_TIME >= 0:
            second -= WORK_TIME//BREAK_TIME
        
        second = max(second, 0)

        L_status.config(text = 'Break for ' + toClock(goal))
        L_time.config(text = toClock(breakTime))

    # Working
    else:
        # Over working
        if second >= WORK_TIME:
            # Check snooze
            if second == WORK_TIME or (second - WORK_TIME)%SNOOZE_TIME == 0:
                L_status.config(text = 'You should take a break')
                popUp()
        else:
            L_status.config(text = 'You\'re working')

        second += 1
        L_time.config(text = toClock(second))

    if readWindowStatus() == 'Show':
        popUp()
        writeWindowStatus('Nothing')

    root.after(1000, clock)

if readWindowStatus() == 'Open':
    writeWindowStatus('Nothing')

    configData = readWindowStatus('Config.txt')
    WORK_TIME = readConfig('WORK_TIME')
    SNOOZE_TIME = readConfig('SNOOZE_TIME')
    BREAK_TIME = readConfig('BREAK_TIME')
    AFK_THRESHOLD = readConfig('AFK_THRESHOLD')

    second = 0
    breakTime = 0

    mouse.Listener(on_move = action, on_click = action, on_scroll = action).start()
    keyboard.Listener(on_press = action, on_release = action).start()

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
    root.protocol("WM_DELETE_WINDOW", hide_C)
    root.mainloop()
else:
    writeWindowStatus('Show')