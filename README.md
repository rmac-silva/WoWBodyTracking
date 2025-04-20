# WoW Motion Capture
This is a simple python script that allows players to:

- Walk in World of Warcraft by walking in real life
- Saving custom poses, assigning keybinds. When replicating those poses the keybinds get pressed
- A separate voice module where users can configure certain keywords associated with spoken words

# Common Issues
If you have overlap, either make the poses more distinct or make their thresholds lower. Ultimately you can try and ignore certain body parts, which will lead to smaller scores and hopefully more accurate pose estimation.

If poses are triggering while you're raising your hands, make the pose hold time bigger, even though it will introduce a delay it will prevent misfires (this happens often when raising your arms for mouse movement)

## Motion Capture
The WoW With Movement module requires a webcam that supports a USB 3.0 Connection [Blue USBs] needed to run MediaPipe's pose processing,

This application lacks UI completely, for a version with UI (and better developed) check out ["The Link"](https://store.steampowered.com/app/1285430/The_Link/).

### Instructions: {#instructions}
Please read to the end, or at least if you encounter issues glance over the [Settings](https://github.com/rmac-silva/WoWBodyTracking/edit/main/README.md#settings) section,

1. Either download the python code (requires python and associated libraries to run) or the release (executable, comes prepackaged with MediaPipe (hence the large download)
2. If you are running the release, you will have to download a voice recognition model from https://alphacephei.com/vosk/models and place it in a "model" folder next to the executable (check the github for the layout).
   You will also have to download a model if you want better voice recognition, as the current model is only 50mb in size and pretty bad.
4. Upon running, a settings file will be created to change some basic settings, these are glanced over in the settings section.

And by this point the program should be running! You should have a window with a webcam preview, and when stepping into the frame you should see a blue outline around your body.
If you raise your hands to the top of the screen they should turn red, meaning the hand tracking is working.

### Hand Movement
By default this is configured for WoW, so holding your hands on the top part of the screen will make the mouse pan and hold down right click.
To move the mouse, simply move your hand left or right, the farther from the starting point, the faster it will turn. Should be intuitive. You can swap the dominant hand in the settings.

### Walking
To walk in-game (again this is configured for WoW) if you raise either foot above the threshold you start walking (emulating pressing down on the 'w' key) and after .5s (configurable) of not raising your feet you stop walking.

### Saving a pose

1. Walk in frame, and make sure your body is fully visible
2. With the voice module enabled, simply say "Save Pose" to record your current pose as a .json file
3. Now open your saved_poses folder, and open the latest .json (usually the highest index) and configure the pose's behavior:
  - "name": "Mount Up", # The name of the pose, purely informational
  - "keycode": "8", #The key you want to press, ex: "q", "k", "9", "shift+9" 
  - "threshold": 0.15, #How close must you match your pose to trigger it, lower values make it harder. Higher values make it trigger incorrectly more often.
  - "key_press_interval" : 2, #The cooldown between key presses, if you hold down the pose it will press this button every 'key_press_interval' seconds
  - "ignored_body_parts": [], #The ignored body parts, [right_hand,right_arm,right_leg,left_hand,left_arm,left_leg] WARNING: This could lead to weird distance values since it has less body parts to check. I don't recommend using this

4. Relaunch the app and the pose will be loaded. I recommend testing it out on a notepad.

## Settings
### Pose Settings
- pose_hold_time : .5 # How long the pose has to be held to trigger the keystroke. Low values lead to a lot of misfires if you're raising your arms for hand tracking

### Mouse settings
- sensitivity : 450 #Mouse sensitivity
- y_locked : True #Whether to consider the y-axis or to lock it
- southpaw : False #Will prioritize the left hand for tracking movement
- HAND_Y_THRESHOLD : .25 #Higher means the hand tracking will happen sooner - This essentially means the top 25% of your webcam preview is where it will consider as valid positions for hand tracking.
- For example if you set it to .5, the top half of the screen will count. If you place it at .10, only the top 10% of your screen

### Walking settings
- walking_key : "w" #The key that will be used for walking
- stopping_time : .5 #How long it takes for you to stop, how often you need to raise your feet. Setting this too low will cause the program to constantly flip between walking and not walking. 
- WALKING_Y_THRESHOLD : .91 #Higher means it's easier to walk, you need to raise your feet less. Too high might mean it won't detect when you're standing still.
This threshold is the opposite of the hand one, if it's .91, it means if your foot is in the first 9% of the screen you are standing still, and if it's above the 9%th percentile of your screen, you will be walking

# WoW with Sound
This is essentially a side project, and a simple implementation of voice to keypress system. It interprets your input through your microphone and then presses the key you configured in the settings

Run it either with python (you will need the libraries) or through the release.

You will need to download a Vosk model (check WoW Motion Capture section) to interpret your speech.

After that, simply configure the sound_commands.cfg with the commands you pretend:
- shadowbolt | shadow bolt : 1 # This means that either the words "shadowbolt" or "shadow bolt" can trigger the command, useful for when the voice recognition can't understand whole words like "shadowbolt" 
- corruption : shift+1 # shift+1 enables hotkeys of multiple keypresses

# TODO
- Add a way to visualize the current confidence in the best matching pose
- Hotkeys for WoW Motion Capture
