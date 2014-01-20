# -*- coding: UTF-8 -*-
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import Leap, sys


TURN_TRESHOLD = 50
DRIFT_TRESHOLD = 150

keys = {'forward':'w', 
        'left':'a', 
        'right':'d', 
        'brake':'s', 
        'nitro':'n',
        'drift':'v',
        'fire':' ',
        }

class SampleListener(Leap.Listener):
    def __press_key(self, key):
        if not self.__key_pressed_flags[key]:
            self.keyboard.press_key(keys[key])
            self.__key_pressed_flags[key] = True

    def __release_key(self, key):
        if self.__key_pressed_flags[key]:
            self.keyboard.release_key(keys[key])
            self.__key_pressed_flags[key] = False

    def on_init(self, controller):
        self.__left_hand_id = 0
        self.__right_hand_id = 0
        self.__frame_count = 0

        self.__key_pressed_flags = {
            'forward':False, 
            'left':False, 
            'right':False, 
            'brake':False, 
            'nitro':False,
            'drift':False,
            'fire':False,
        }

        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()
        x_dim, y_dim = self.mouse.screen_size()
        self.mouse.click(x_dim/2, y_dim/2, 1)
        
        print "Initialized"


    def on_connect(self, controller):
        print "Connected"


    def on_disconnect(self, controller):
        print "Disconnected"


    def on_exit(self, controller):
        print "Exited"


    def on_frame(self, controller):
        f = controller.frame()
        left_hand = f.hand(self.__left_hand_id)
        right_hand = f.hand(self.__right_hand_id)
        

        if (not left_hand.is_valid ) or (right_hand.is_valid ):
            left_hand = f.hands.leftmost
            right_hand = f.hands.rightmost

            self.__left_hand_id = left_hand.id
            self.__right_hand_id = right_hand.id

            print "new hands identified", self.__left_hand_id, self.__right_hand_id

        left_handPos = left_hand.palm_position
        right_handPos = right_hand.palm_position
        avgZ = (left_handPos[2] + right_handPos[2]) / 2

        print "left_hand position: ", left_handPos
        print "right_hand position: ", right_handPos        
        print "avgZ: ", avgZ


### Nitro and brake
        if avgZ < -50:
            print "nitro"
            self.__press_key('nitro')
        else:
            self.__release_key('nitro')

        
        if avgZ > 90:
            print "hamulec"
            self.__press_key('brake')
        else:
            self.__release_key('brake')


### driving forward       
        if avgZ <= 10:   
            print "prosto" 
            self.__press_key('forward')
        else:
            self.__release_key('forward')


### turning and drifting
        if left_handPos[1] - right_handPos[1] > TURN_TRESHOLD:
            print "skret w prawo"
            self.__press_key('right')
        else:
            self.__release_key('right')


        if right_handPos[1] - left_handPos[1] > TURN_TRESHOLD:
            print "skret w lewo"
            self.__press_key('left')
        else:
            self.__release_key('left')


        if abs(right_handPos[1] - left_handPos[1]) > DRIFT_TRESHOLD:
            print "drift"
            self.__press_key('drift')
        else:
            self.__release_key('drift')

            
### using gifts
        right_fingers = right_hand.fingers
        if len(right_fingers) == 5:
            print "FIRE!!!"
            self.__press_key('fire')
        else:
            self.__release_key('fire')



    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"


def main():
    listener = SampleListener()
    controller = Leap.Controller()

    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    controller.add_listener(listener)

    print "Press Enter to quit..."
    sys.stdin.readline()

    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
