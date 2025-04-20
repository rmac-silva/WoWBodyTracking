
from typing import List
from mediapipe.framework.formats import landmark_pb2
import json
from mediapipe.python.solutions.pose import PoseLandmark

excluded_landmarks = [
    PoseLandmark.LEFT_EYE, 
    PoseLandmark.RIGHT_EYE, 
    PoseLandmark.LEFT_EYE_INNER, 
    PoseLandmark.RIGHT_EYE_INNER, 
    PoseLandmark.LEFT_EAR,
    PoseLandmark.RIGHT_EAR,
    PoseLandmark.LEFT_EYE_OUTER,
    PoseLandmark.RIGHT_EYE_OUTER,
    PoseLandmark.NOSE,
    PoseLandmark.MOUTH_LEFT,
    PoseLandmark.MOUTH_RIGHT ]

BODY_PART_LANDMARKS = {
    "right_arm": [
        PoseLandmark.RIGHT_SHOULDER.value,
        PoseLandmark.RIGHT_ELBOW.value,
        PoseLandmark.RIGHT_WRIST.value,
        PoseLandmark.RIGHT_THUMB.value,
        PoseLandmark.RIGHT_INDEX.value,
        PoseLandmark.RIGHT_PINKY.value
    ],
    "left_arm": [
        PoseLandmark.LEFT_SHOULDER.value,
        PoseLandmark.LEFT_ELBOW.value,
        PoseLandmark.LEFT_WRIST.value,
        PoseLandmark.LEFT_THUMB.value,
        PoseLandmark.LEFT_INDEX.value,
        PoseLandmark.LEFT_PINKY.value
    ],
    "right_hand": [
        PoseLandmark.RIGHT_WRIST.value,
        PoseLandmark.RIGHT_THUMB.value,
        PoseLandmark.RIGHT_INDEX.value,
        PoseLandmark.RIGHT_PINKY.value
    ],
    "left_hand": [
        PoseLandmark.LEFT_WRIST.value,
        PoseLandmark.LEFT_THUMB.value,
        PoseLandmark.LEFT_INDEX.value,
        PoseLandmark.LEFT_PINKY.value
    ],
    "head": [
        PoseLandmark.NOSE.value,
        PoseLandmark.LEFT_EYE_INNER.value,
        PoseLandmark.LEFT_EYE.value,
        PoseLandmark.LEFT_EYE_OUTER.value,
        PoseLandmark.RIGHT_EYE_INNER.value,
        PoseLandmark.RIGHT_EYE.value,
        PoseLandmark.RIGHT_EYE_OUTER.value,
        PoseLandmark.LEFT_EAR.value,
        PoseLandmark.RIGHT_EAR.value,
        PoseLandmark.MOUTH_LEFT.value,
        PoseLandmark.MOUTH_RIGHT.value
    ],
    "right_leg": [
        PoseLandmark.RIGHT_HIP.value,
        PoseLandmark.RIGHT_KNEE.value,
        PoseLandmark.RIGHT_ANKLE.value,
        PoseLandmark.RIGHT_HEEL.value,
        PoseLandmark.RIGHT_FOOT_INDEX.value
    ],
    "left_leg": [
        PoseLandmark.LEFT_HIP.value,
        PoseLandmark.LEFT_KNEE.value,
        PoseLandmark.LEFT_ANKLE.value,
        PoseLandmark.LEFT_HEEL.value,
        PoseLandmark.LEFT_FOOT_INDEX.value
    ]
}

def save_pose_to_json(landmarks : List[landmark_pb2.NormalizedLandmark], index : int):
    
    filename = f"saved_poses/pose_{index}.json"
    pose_obj = {
        "name" : f"NaN {index}",
        "keycode" : "NaN",
        "threshold" : 0.15,
        "ignored_body_parts" : [],
        "data" : []
    }
    
    data = [{
        'id': idx,
        'x': lm.x,
        'y': lm.y,
        'z': lm.z,
        'visibility': lm.visibility
    } for idx, lm in enumerate(landmarks)]

    pose_obj["data"] = data
    
    with open(filename, 'w') as f:
        json.dump(pose_obj, f, indent=2)
    
    return pose_obj
        
