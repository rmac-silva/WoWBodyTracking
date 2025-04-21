import os
from src.pose import PoseManager
from src.speech_module import SpeechModule
from src.media_pipe import MediaPipe
from src.hand_tracker import HandTracker
from src.walk_manager import WalkManager
from src.settings import Settings

os.makedirs("saved_poses", exist_ok=True)

def load_saved_settings():
    #Pose settings
    mp.pose_hold_time = float(s.pose_hold_time)
    mp.save_pose_keybind = str(s.pose_save_keybind)
    #Mouse settings
    hand_tracker.sensitivity = float(s.sensitivity)
    hand_tracker.y_locked = s.y_locked
    hand_tracker.southpaw = s.southpaw
    hand_tracker.HAND_Y_THRESHOLD = float(s.HAND_Y_THRESHOLD)
    
    #Walking settings
    walk_manager.walking_key = s.walking_key
    walk_manager.stopping_time = float(s.stopping_time)
    walk_manager.WALKING_Y_THRESHOLD = float(s.WALKING_Y_THRESHOLD)

def create_sample_settings():
    config_text = """
#Pose Settings
pose_hold_time : .5 # How long the pose has to be held to trigger the keystroke. Low values lead to a lot of misfires
pose_save_keybind : "." #Keybind to save a pose instead of using voice commands

#Mouse settings
sensitivity : 450 #Mouse sens
y_locked : True #Whether to consider the y-axis
southpaw : False #Will prioritize the left hand for tracking movement
HAND_Y_THRESHOLD : .25 #Higher means the hand tracking will happen sooner

#Walking settings
walking_key : "w"
stopping_time : .5 #How long it takes for you to stop. Setting this too low will cause the program to constantly flip between walking and not walking
WALKING_Y_THRESHOLD : .91 #Higher means it's easier to walk, you need to raise your feet less. Too high might mean it won't detect when you're standing still
    """
    
    with open("settings.cfg", "x") as file:
        file.write(config_text.strip())
    
try:
    s = Settings()
except:
    create_sample_settings()
    s = Settings()
finally:
    pose_manager = PoseManager()
    speech_recognizer = SpeechModule()
    hand_tracker = HandTracker()
    walk_manager = WalkManager()
    mp = MediaPipe(pose_manager,speech_recognizer,hand_tracker,walk_manager)
    load_saved_settings()
    mp.run()
    input("Press any key to close...")
    


