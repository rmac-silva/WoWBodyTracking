from src.pose import Pose
import pyautogui
import time
class WalkManager():
    
    def __init__(self):
        #State
        self.walking = False #
        self.pressed_down = False
        
        #Vars
        self.walking_key = "w"
        self.last_time_walked = 0
        
        #Settings
        self.stopping_time = .5
        self.WALKING_Y_THRESHOLD = .93 #Higher means it's easier to walk

    def setup_poses(self,leftLegPose : Pose, rightLegPose : Pose, rested_pose : Pose): 
        self.poses["WalkLeft"] = leftLegPose
        self.poses["WalkRight"] = rightLegPose
        self.poses["Standing"] = rested_pose
        
    
        
    
    def process_walking(self, left_ankle_y, right_ankle_y):
        self.check_for_walking(left_ankle_y, right_ankle_y)

        if(self.walking and not self.pressed_down):
            print("Starting to walk...")
            pyautogui.keyDown(self.walking_key,_pause = False)
            self.pressed_down = True
        elif(not self.walking and self.pressed_down):
            print("Stopping...")
            self.pressed_down = False
            pyautogui.keyUp(self.walking_key,_pause = False)
    
    def check_for_walking(self, left_ankle_y, right_ankle_y):
        if(right_ankle_y <= self.WALKING_Y_THRESHOLD or left_ankle_y <= self.WALKING_Y_THRESHOLD):
            self.walking = True #Both hands are above the threshold, block pose detection and enable hand panning
            self.last_time_walked = time.time()
        else:
            time_idle = time.time() - self.last_time_walked
            
            if(time_idle >= self.stopping_time):
                self.walking = False
        
        
        
            
        