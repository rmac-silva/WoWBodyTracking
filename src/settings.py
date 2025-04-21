class Settings():
    
    def __init__(self):
        #Pose Settings
        self.pose_hold_time = 2 # How long the pose has to be held to trigger the keystroke
        self.pose_save_keybind = "." #Keybind for saving a pose

        #Mouse settings
        self.sensitivity = 450 #Mouse sens
        self.y_locked = True #Whether to consider the y-axis
        self.southpaw = False #Will prioritize the left hand for tracking movement
        self.HAND_Y_THRESHOLD = .25 #Higher means the hand tracking will happen sooner

        #Walking settings
        self.walking_key = "w"
        self.stopping_time = .5 #How long it takes for you to stop. Setting this too low will cause the program to constantly flip between walking and not walking
        self.WALKING_Y_THRESHOLD = .93 #Higher means it's easier to walk, you need to raise your feet less. Too high might mean it won't detect when you're standing still
        
        self.load_settings()
        
    def load_settings(self):
        file = "./settings.cfg"
        with open(file, 'r') as f:
            for line in f:
                line = line.strip()  # Remove leading/trailing whitespace
                if not line or line.startswith('#'):
                    continue  # Skip empty lines and comments
                args = line.split(":")
                setting_name = args[0].strip()
                setting_value = args[1].split("#")[0].strip()
                # Process the line here
                print(f"Line: {setting_name} : {setting_value}")
                setattr(self,setting_name,setting_value)

        self.pose_save_keybind = self.pose_save_keybind.replace("\"","").strip()
        self.walking_key = self.walking_key.replace("\"","").strip()
    