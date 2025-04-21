import pyautogui

class HandTracker():

    def __init__(self):
        
        
        #Right hand
        self.start_hand_r = None #Starting hand pos (x,y)
        self.prev_hand_r = None #Previous wrist pos (x,y)
        
        #Left hand
        self.start_hand_l = None #Starting hand pos (x,y)
        self.prev_hand_l = None #Previous wrist pos (x,y)
        
        #Cursor
        self.start_mouse = None #Starting cursor hand pos (x,y)
        
        #State
        self.enabled = False #Wheter tracking is active
        self.southpaw = False
        
        self.should_right_click = True
        self.right_clicking = False
        
        # Settings
        self.sensitivity = 250
        self.y_locked = True
        self.HAND_Y_THRESHOLD = .25 #Higher means the hand tracking will happen sooner
        
        #Mirrored directions
        self.mirrored = 1 #-1 if True, 1 if False
        
    def start_hand_tracking(self, start_pos_r, start_pos_l):
        print("\nStarting tracking...\n")
        self.enabled = True
        self.start_hand_r = start_pos_r
        self.start_hand_l = start_pos_l
        self.start_mouse = pyautogui.position()
        
    def stop_hand_tracking(self):
        if(self.enabled):
            print("\nStopping tracking...\n")
            self.enabled = False
            self.start_hand_r = None
            self.start_hand_l = None
            self.start_mouse = None
            
            if(self.right_clicking):
                self.right_clicking = False
                pyautogui.mouseUp(button='right')

    def process_hand(self, current_pos_r, current_pos_l):
        if(self.hands_are_in_place(current_pos_r[1],current_pos_l[1])):
         
            if not self.enabled:
                self.start_hand_tracking(current_pos_r,current_pos_l)
                return
            
            if(not self.right_clicking and self.should_right_click):
                pyautogui.mouseDown(button='right')
                self.right_clicking = True
            
            cursor_pos = pyautogui.position()   
            
            if(not self.southpaw):
                delta_x = current_pos_r[0] - self.start_hand_r[0]
                delta_y = current_pos_r[1] - self.start_hand_r[1]
            else:
                delta_x = current_pos_l[0] - self.start_hand_l[0]
                delta_y = current_pos_l[1] - self.start_hand_l[1]
            
            new_mouse_x = int(cursor_pos.x + self.mirrored * (delta_x * self.sensitivity)) #Current mouse position + deltaX from hand tells us which direction to move to
            
            if(self.y_locked):
                new_mouse_y = pyautogui.position().y
            else:
                new_mouse_y = int(cursor_pos.y + self.mirrored * (delta_y * self.sensitivity)) #Current mouse position + deltaY from hand tells us which direction to move to

            pyautogui.moveTo(new_mouse_x, new_mouse_y, duration=0, _pause=False)
            
        else:
            
            self.stop_hand_tracking()

    def hands_are_in_place(self, right_hand_y, left_hand_y):
        
        
        # print(f"Right: {right_hand_y} | Left {left_hand_y}")
        
        if(right_hand_y == "NaN" or left_hand_y == "NaN"):
            # print("\nNo hands detected...")
            return False
        
        if(right_hand_y <= self.HAND_Y_THRESHOLD and left_hand_y <= self.HAND_Y_THRESHOLD):
            return True #Both hands are above the threshold, block pose detection and enable hand panning
        else:
            return False #Either hand is not above the threshold, doesn't block detection