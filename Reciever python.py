import serial
import pyautogui
import asyncio

print('Starting...')


ps = ''
t = 0.1
current_key = ''
last_key = ''
count = 0
printed = False
set = False

try:
    ser = serial.Serial('/dev/cu.usbmodem14101', 115200)  # replace with the appropriate port and baud rate
    ser.timeout = 1
    connected = True
    print(f'Connected to ' + ser.name)
except:
    print('Please check the port')
    connected = False

async def release_key():
    await asyncio.sleep(t)
    pyautogui.keyUp(current_key)

async def pressbutton(x, y, b1):
    global current_key
    #print(b1)
    if x < 400 and checkSafeRange(y) == True: #down
        current_key = 's'
        pyautogui.keyDown(current_key)
        asyncio.ensure_future(release_key())
        return

    elif x > 600 and checkSafeRange(y) == True: #up
        current_key = 'w'
        pyautogui.keyDown(current_key)
        asyncio.ensure_future(release_key())
        return
    elif y > 600 and checkSafeRange(x) == True: #right
        current_key = 'd'
        pyautogui.keyDown(current_key)
        asyncio.ensure_future(release_key())
        return
    elif y < 400 and checkSafeRange(x) == True: #left
        current_key = 'a'
        pyautogui.keyDown(current_key)
        asyncio.ensure_future(release_key())
        return
    elif b1 == 1023: #joystick button
        current_key = 'shift'
        pyautogui.keyDown(current_key)
        asyncio.ensure_future(release_key())
        return
    else:
        #print('no key pressed')
        return

def checkSafeRange(i):
    if 400 < i < 600:
        return True
    else:
        return False

async def read_serial():

    while True:
        global set
        if connected:
            sel = ser.readline().decode('utf-8').rstrip()
            sl = sel.split(',')
            #print(sl)
            if len(sl) == 3:
                x = int(sl[0])
                y = int(sl[1])
                b1 = int(sl[2])
                await pressbutton(x, y, b1)
            else:
                if set == False:
                    counter = 0
                    set = True
                counter+=1
                read_serial()
                if counter == 5:
                    print('No/invalid data')
                    break

        else:
            print('No connection')
            break



async def main():
    await read_serial()

if __name__ == "__main__":
    print('Running...')
    asyncio.run(main())
 