from typing import List
import mediapipe as mp #Mediapipe
import cv2 #webcam preview library
import pyautogui
import time

#Typing
from mediapipe.framework.formats import landmark_pb2

#Classes
from src.pose import PoseManager
from src.speech_module import SpeechModule
from src.hand_tracker import HandTracker
from src.walk_manager import WalkManager
import src.utils as utils 



class MediaPipe():
    
    def __init__(self, p_manager : PoseManager, sm : SpeechModule , ht : HandTracker, wm : WalkManager):
        self.pose_count = len(p_manager.pose_list)+1 #Index for saving poses
        
        #Detection objects
        self.mp_pose = mp.solutions.pose
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.webcam_capture = cv2.VideoCapture(0)
        
        #State
        self.paused = False
        self.running = True
        
        #Pose Manager
        self.pose_manager = p_manager
        self.previous_pose = None
        
        #Pose Manager - Time Variables
        self.time_in_pose = 0
        self.last_call_time = 0
        
        #Pose Manager - Settings
        self.pose_hold_time = 2
        
        #Speech module
        self.speech_module = sm
        
        #Hands
        self.hands = None
        self.hand_tracker = ht
        
        #Walking
        self.walking_manager = wm
        
        #Variable objects
        self.result : landmark_pb2 = ""
        
        self.setup_hands()
    
    #region - Setup
    
    def setup_hands(self):
        self.index = 0
        
        hand_joints = {
            self.mp_pose.PoseLandmark.LEFT_WRIST,
            self.mp_pose.PoseLandmark.LEFT_THUMB,
            self.mp_pose.PoseLandmark.LEFT_INDEX,
            self.mp_pose.PoseLandmark.LEFT_PINKY,
            self.mp_pose.PoseLandmark.RIGHT_WRIST,
            self.mp_pose.PoseLandmark.RIGHT_THUMB,
            self.mp_pose.PoseLandmark.RIGHT_INDEX,
            self.mp_pose.PoseLandmark.RIGHT_PINKY,
        }
        
        self.body_connections = [
            (a, b) for a, b in self.mp_pose.POSE_CONNECTIONS
            if a not in hand_joints and b not in hand_joints
        ]
        self.hand_connections = [
            (a, b) for a, b in self.mp_pose.POSE_CONNECTIONS
            if a in hand_joints and b in hand_joints
        ]
        
        self.screen_w, self.screen_h = pyautogui.size()
        print(f"Screen size:{self.screen_w}x{self.screen_h}")
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
    

    #endregion
    
    #region - Main
    def run(self):
        self.speech_module.start()
        
        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while self.webcam_capture.isOpened(): #While not paused
                
                ret, frame = self.webcam_capture.read()
                if not ret:
                    break

                frame = cv2.flip(frame,1)
                
                self.process_input()
                self.process_speech()
                
                if(not self.paused):
                    image = self.process_tracking(pose, frame)

                # Show the output
                cv2.imshow('Pose Detector', image)
                  
                if(not self.running):
                    break
                
        #Not running
        self.webcam_capture.release()
        cv2.destroyAllWindows()

    def process_tracking(self, pose, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
                    
                    
        # Perform pose detection
        self.result = pose.process(image)
        joint_positions = self.pose_joints()
        #Hand recognition (Mouse movement)
        self.process_hands(image)
        self.process_feet()
        #Joint positions need to be obtained before converting the image to BGR
        
        # Draw the pose annotation on the image
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    
        

        if self.result.pose_landmarks:
            
            if(not self.hand_tracker.enabled):
                best_pose = self.pose_manager.find_best_matching_pose(joint_positions)
                
                if(best_pose == self.previous_pose):
                    self.time_in_pose += time.time() - self.last_call_time
                else:
                    self.time_in_pose = 0
                    
                if(best_pose is not None and self.time_in_pose >= self.pose_hold_time):
                    best_pose.emulate_key()
                    
                self.previous_pose = best_pose
                self.last_call_time = time.time()
            else:
                self.time_in_pose = 0
                self.last_call_time = time.time()
                    
            self.draw_overlay(image)
            
        return image

    def draw_overlay(self, image):

        if(self.hand_tracker.enabled):
            self.mp_drawing.draw_landmarks(
                image, 
                self.result.pose_landmarks, 
                self.body_connections,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(252, 152, 3), thickness=2) #BGR
            )
            
            self.mp_drawing.draw_landmarks(
                image, 
                self.result.pose_landmarks, 
                self.hand_connections,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(3, 3, 253), thickness=2) #BGR
            )
        else:
            self.mp_drawing.draw_landmarks(
                image, 
                self.result.pose_landmarks, 
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(252, 152, 3), thickness=2) #BGR
            )
        
        return image
    #endregion
    
    #region - Input processing
    def process_hands(self,image):
        
        hand_tracking_results = self.hands.process(image)

        if hand_tracking_results.multi_hand_landmarks and hand_tracking_results.multi_handedness:
            
            l_hand_pos = ("NaN","NaN")
            r_hand_pos = ("NaN","NaN")
            
            for hand_landmarks, handedness in zip(hand_tracking_results.multi_hand_landmarks, hand_tracking_results.multi_handedness):
                label = handedness.classification[0].label  # 'Right' or 'Left'
                
                if label == 'Left': 
                    r_hand_pos = (hand_landmarks.landmark[0].x,hand_landmarks.landmark[0].y)
                
                if label == 'Right':
                    l_hand_pos = (hand_landmarks.landmark[0].x,hand_landmarks.landmark[0].y)

            self.hand_tracker.process_hand(r_hand_pos,l_hand_pos)
                
    def process_feet(self):
        joint_positions : List[landmark_pb2.NormalizedLandmark] = self.pose_joints()
        if(joint_positions is not None):
            right_ankle = joint_positions[28]
            left_ankle = joint_positions[27]
            self.index += 1
            if self.index % 20 == 0:
                print(f"L:{left_ankle.y} | R:{right_ankle.y}")
                
            self.walking_manager.process_walking(left_ankle.y,right_ankle.y)
        else:
            self.walking_manager.walking = False
    
    def process_input(self):
        input = cv2.waitKey(10) & 0xFF
        
        if input == ord('s') and self.result.pose_landmarks:
            self.save_new_pose()
            
        if input == ord('h') and self.result.pose_landmarks:
            self.speech_module.toggle()

        elif input == 27:  # ESC to exit
            print("Stopping")
            self.running = False
            
    def process_speech(self):
        if(self.speech_module.enabled):
            text = self.speech_module.get_speech()
            
            if(text != ""):
                self.interpret_command(text)
                
    def interpret_command(self,text : str):
        print(f"Running command:{text}")
        
        match(text):
            
            case "pause" | "pause program":
                self.paused = True
            case "resume" | "unpause":
                self.paused = False
            case "save pose" | "save command" | "safe pose":
                self.save_new_pose()
            case "exit" | "quit" | "stop":
                self.running = False
            case "stop listening" | "quiet" | "silence":
                self.speech_module.enabled = False
            case _:
                print("Invalid command")
    
    #endregion
    
    #region - Getters & Setters
    def save_new_pose(self):
        new_pose = utils.save_pose_to_json(self.pose_joints(), self.pose_count)
        self.pose_manager.create_pose_from_json_object(new_pose)
        self.pose_count += 1
        
    def pose_joints(self):
        if(self.result is None):
            return None
        elif(self.result.pose_landmarks is None):
            return None
        else:
            return self.result.pose_landmarks.landmark