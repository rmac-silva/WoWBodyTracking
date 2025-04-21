import os
import json 
import math
import pyautogui
import src.utils as utils
import time

from typing import List
from mediapipe.framework.formats import landmark_pb2


debug = False

class PoseData:

    def __init__(self, id: int, x: float, y: float, z: float, visibility: float):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.visibility = visibility

class Pose:

    def __init__(self, pose_data: List[PoseData], name : str, keycode : str, threshold : float = 0.15, key_press_interval=1, ignored_parts : List[str] = []):
        self.name = name
        self.keycode = keycode.lower()
        self.pose_data = pose_data  # List of PoseData objects
        self.threshold = threshold
        self.key_press_interval = key_press_interval
        self.ignored_parts = ignored_parts
        self.ignored_parts.append("head")
        
        #Time variables
        self.last_key_press_time = 0
        
        self.ignored_indexes = []
        self.compute_ignored_indexes()
        
    def compute_ignored_indexes(self):
        for p in self.ignored_parts:
            self.ignored_indexes.extend(utils.BODY_PART_LANDMARKS[p])
    
    def compare_pose(self,current_landmarks : List[landmark_pb2.NormalizedLandmark]):
        if(current_landmarks is None or self.pose_data is None):
            return 1 #Max distance
        
        
        counted_positions = 0
        index = 0
        # Sum of Euclidean distances between corresponding landmarks
        total_distance = 0.0
        for saved, current in zip(self.pose_data, current_landmarks):
            if(index not in self.ignored_indexes):
                dx = saved.x - current.x
                dy = saved.y - current.y
                dz = saved.z - current.z
                dist = math.sqrt(dx*dx + dy*dy + dz*dz)
                total_distance += dist
                
                counted_positions += 1

            index += 1
        
        # Return average distance
        # sif(self.name == "T Pose"):print(f"Score: {total_distance / len(filtered_landmarks)}")
        return total_distance / counted_positions
    
    def emulate_key(self):
        try:
            current_time = time.time()
            time_delta = current_time - self.last_key_press_time
            if(time_delta >= self.key_press_interval):
                
                keys = self.keycode.split("+")
                if(len(keys) == 1):
                    print(f"Pressing {keys[0]}")
                    pyautogui.press(keys[0],presses=1,_pause=False)
                elif(len(keys) == 2):
                    print(f"Pressing {keys[0]}+{keys[1]}")
                    pyautogui.hotkey(keys[0],keys[1])
                elif(len(keys) == 3):
                    pyautogui.hotkey(keys[0],keys[1],keys[2])
                    print(f"Pressing {keys[0]}+{keys[1]}+{keys[2]}")
                else:
                    print(f"Invalid number of keybinds: {keys} max is 3 shift+ctrl+1")
                
                self.last_key_press_time = time.time()
        except ValueError:
            if(debug):print(f"Error emulating key {self.keycode} for pose {self.name}")
            pass

    
class PoseManager:

    def __init__(self):
        self.pose_list: List[Pose] = []
        
        #Dedicated pose for mouse look
        self.mouse_enabled_pose = None
        
        #LeftLeg Raised for walking
        self.left_leg_raised_pose = None
        #RightLeg Raised for walking
        self.right_leg_raised_pose = None
        #Rested pose for walking
        self.rested_pose = None
        self.load_poses()

    def load_poses(self):
        pose_path = "./saved_poses"
        
        if os.path.exists(pose_path) and os.path.isdir(pose_path):
            files = os.listdir(pose_path)
            
            for file in files:
                if file.endswith(".json"):
                    print(f"Creating pose {file}")
                    file_path = os.path.join(pose_path, file)
                    self.create_pose_from_json(file_path)
        else:
            print(f"Directory not found: {pose_path}")

    def create_pose_from_json(self, file_path: str):
        """Loads a Pose object from a JSON file."""
        with open(file_path, 'r') as f:
            pose_data_json = json.load(f)

        pose_name = str(pose_data_json["name"])
        pose_keycode = str(pose_data_json["keycode"])
        pose_threshold = float(pose_data_json["threshold"])
        key_press_interval = float(pose_data_json["key_press_interval"])
        ignored_body_parts = pose_data_json["ignored_body_parts"]
        pose_data = [] #List of pose data
        
        # Create PoseData objects for each landmark entry in the JSON
        for landmark in pose_data_json["data"]:
            pose_data.append(PoseData(
                id=landmark['id'],
                x=landmark['x'],
                y=landmark['y'],
                z=landmark['z'],
                visibility=landmark['visibility']
            ))
            
        
        pose = Pose(pose_data, pose_name, pose_keycode, pose_threshold, key_press_interval, ignored_body_parts)#Create a new pose

        self.pose_list.append(pose)  # Add the Pose object to possible poses
        
    def create_pose_from_json_object(self, json_object):
        pose_data = [] #List of pose data
        
        # Create PoseData objects for each landmark entry in the JSON
        for landmark in json_object["data"]:
            pose_data.append(PoseData(
                id=landmark['id'],
                x=landmark['x'],
                y=landmark['y'],
                z=landmark['z'],
                visibility=landmark['visibility']
            ))
        
        pose = Pose(pose_data,json_object["name"],str(json_object["keycode"]))#Create a new pose
        self.pose_list.append(pose)  # Add the Pose object to possible poses
        
    def find_best_matching_pose(self, current_landmarks : List[landmark_pb2.NormalizedLandmark]):
        """Compares current pose landmarks to a saved pose JSON and returns a similarity score (lower is better)."""
    
        best_diff = 2
        best_pose : Pose = None
        score = 0
        
        for pose in self.pose_list:
            score = pose.compare_pose(current_landmarks)
            diff = score - pose.threshold #0.1 - .2 threshold = -.1 || Success!
            if(diff < best_diff and score <= pose.threshold):
                best_diff = diff
                best_pose = pose

        return best_pose
    
    def compare_single_pose(self,pose : Pose, landmarks :  List[landmark_pb2.NormalizedLandmark]):
        score = pose.compare_pose(landmarks)
        return score
                    
