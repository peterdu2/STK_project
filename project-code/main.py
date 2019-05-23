import numpy as np
import pyscreenshot as ImageGrab
import cv2
import time
from PIL import Image
import pyautogui
import pyxhook
from mss import mss
import model
import socket
from sklearn.neural_network import MLPRegressor

new_hook = pyxhook.HookManager()

def OnKeyPress(event):
    key = event.Ascii
    if (key == 112):
        print('suh')

new_hook.KeyDown=OnKeyPress
new_hook.HookKeyboard()
new_hook.start()



def getImage():
    with mss() as sct:
        mon = {'top': 65, 'left': 50, 'width': 1020, 'height': 720}
        #sct.get_pixels(mon)
        img = np.array(sct.grab(mon))
        #img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
    return img


def right():
    print('RIGHT')
    pyautogui.keyDown('w')
    pyautogui.keyUp('a')
    pyautogui.keyUp('s')
    pyautogui.keyDown('d')

def left():
    print('LEFT')
    pyautogui.keyDown('w')
    pyautogui.keyDown('a')
    pyautogui.keyUp('s')
    pyautogui.keyUp('d')

def straight():
    print('STRAIGHT')
    pyautogui.keyDown('w')
    pyautogui.keyUp('a')
    pyautogui.keyUp('s')
    pyautogui.keyUp('d')

def left_or_right(direction):
    if direction == 1:
        right()
    elif direction == -1:
        left()
    elif direction == 0:
        straight()


def main():
    print('Starting Training on Expert Policy...')
    X,y = model.get_model('/home/lab/independentStudy/stk-code/cmake_build/example.txt')
    clf_expert = MLPRegressor(hidden_layer_sizes=(60,40,20))
    clf_expert.fit(X, y)
    print('Done Training on Expert Policy')

    print("Starting Training on Novice Policy...")
    X,y = model.get_model('/home/lab/independentStudy/stk-code/cmake_build/novice.txt')
    clf_novice = MLPRegressor(hidden_layer_sizes=(60,40,20))
    clf_novice.fit(X, y)

    print('Training Complete')

    s_testing = socket.socket()
    port = 8080
    s_testing.connect(('127.0.0.1', port))

    print('Connected to server')

    prev_flag = 1
    iterator = 1
    beta = 0.95

    print('Parameters Set, starting program...')
    while (True):
        screen = getImage()
        flag = s_testing.recv(1)
        flag = flag.decode()
        print("Flag received:", flag)
        features = s_testing.recv(2)
        lines = features.decode()
        features = s_testing.recv(int(lines))
        lines = features.decode()
        line = lines.split(",")
        flag = int(flag) # first flag is 0
        if flag == 2:
            return clf_novice
        if flag != prev_flag:
            print('Iteration completed. Updating weights for novice model')
            prev_flag = flag
            iterator+=1
            if prev_flag == 1:
                X,y = model.get_model('/home/lab/independentStudy/stk-code/cmake_build/novice.txt')
                open('/home/lab/independentStudy/stk-code/cmake_build/novice2.txt', 'w').close()
            else:
                X,y = model.get_model('/home/lab/independentStudy/stk-code/cmake_build/novice2.txt')
                open('/home/lab/independentStudy/stk-code/cmake_build/novice.txt', 'w').close()
            clf_novice.partial_fit(X,y) # update the model with a single iteration over the data
        d_expert = clf_expert.predict([[float(line[0]), float(line[1])]])
        d_novice = clf_novice.predict([[float(line[0]), float(line[1])]])
        print('Expert Prediction:', d_expert)
        print('Novice Prediction: ', d_novice)
        direction_to_go = np.random.choice([float(d_expert[0]), float(d_novice[0])], 1, p=[beta**iterator, 1-beta**iterator])
        print('With probability', beta**iterator, 'and ', 1-beta**iterator, 'i chose direction ', direction_to_go)
        #pos =  d_expert* (beta**iterator) + d_novice * (1-beta**iterator)
        #print random.choice(pos)
        s_testing.send(str(len(str(direction_to_go[0]))).encode())
        s_testing.send(str(direction_to_go[0]).encode())
        if prev_flag == 1:
            # assign to file
            f = open('/home/lab/independentStudy/stk-code/cmake_build/novice2.txt', 'a+')
            f.write(str(line[0]) + "," + str(line[1]) + "," + str(direction_to_go[0]) + '\n')
            f.close()
        else:
            f = open('/home/lab/independentStudy/stk-code/cmake_build/novice.txt', 'a+')
            f.write(str(line[0]) + "," + str(line[1]) + "," + str(direction_to_go[0]) + '\n')
            f.close()

main()
#pyautogui.keyDown('w')


#def process_img(original_image):
    #processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    #processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    #return processed_img


#last_time = time.time()

#while(True):
#    printscreen_pil = ImageGrab.grab(bbox=(70,40,900,700))
#    new_screen = process_img(np.array(printscreen_pil))
#    print('Loop took {} seconds'.format(time.time()-last_time))
#    last_time = time.time()
#    cv2.imshow('window', new_screen)
#    #cv2.imshow('window2', np.array(printscreen_pil))
#    if cv2.waitKey(25) & 0xFF == ord('q'):
#        cv2.destroyAllWindows()
 #       break
   # pyautogui.keyDown('w')
