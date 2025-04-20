import threading
import speech_recognition as sr
from speech_recognition import Recognizer
import pyautogui
import sys
import time
import json

class SpeechModule(threading.Thread):
    
    def __init__(self):
        super().__init__()
        self.daemon = True  # Subservient
        
        self.recognizer = Recognizer()
        self.microphone = sr.Microphone()
        
        self.enabled = True
        
        #Speech
        self.interpreted_text = ""
        self.previous_speech = ""
        
        self._lock = threading.Lock()
        self._stop = False
        
    def run(self):
        with self.microphone as source:
            print("Calibrating microphone...")
            self.recognizer.adjust_for_ambient_noise(source)

            while True:
                if(self.enabled):
                    try:
                        audio = self.recognizer.listen(source)
                        text = self.recognizer.recognize_vosk(audio)
                        
                        with self._lock:
                            self.interpreted_text = text

                        if "stop speech" in text.lower():
                            self.enabled = False

                    except sr.UnknownValueError:
                        print("Could not understand audio.")
                    except sr.RequestError as e:
                        print(f"Windows Speech Recognition error: {e}")
                    except KeyboardInterrupt:
                        print("Interrupted by user.")
                        break
                else:
                    time.sleep(1)
                    
    def toggle(self):
        self.enabled = not self.enabled
        
        if(self.enabled):
            print("Listening...")
        else:
            print("Stopping speech module...")
        
    def stop(self):
        self._stop = True
        
    def get_speech(self):
        if(self.interpreted_text == self.previous_speech):
            return ""
        else:
            self.previous_speech = self.interpreted_text
            try:
                parsed = json.loads(self.interpreted_text)
                return parsed["text"]
            except:
                print("[ERROR] Failed to parse voice command, you can either disable it in settings.cfg or download a model from https://alphacephei.com/vosk/models.\n If you download a model, place it in a folder called 'model' next to the executable.", file=sys.stderr)
                self.enabled = False
class SpeechManager():

    def __init__(self, commands, sm : SpeechModule):
        self.speech_module = sm
        self.commands = commands
        
        self.running = True
        
    def run(self):
        self.speech_module.enabled
        self.speech_module.start()
        
        print("\nPlease wait for the voice module to load...")
        print("Please wait for the voice module to load...\n")
        
        while(True):
            if(self.speech_module.enabled):
                text = self.speech_module.get_speech()

                if(text != ""):
                    self.interpret_command(text)
                    
                if(not self.running):
                    break
                    
    def interpret_command(self,text):
        print(f"Processing command: {text}")
        for entry in self.commands:
            if(text == entry[0]): #Text matches command
                try:
                    if(entry[1] == "exit"):
                        self.running = False
                    elif(entry[1] == "walk"):
                        pyautogui.keyDown("w",_pause = False)
                    elif(entry[1] == "stop"):
                        pyautogui.keyUp("w",_pause = False)
                    else:
                        keys = entry[1].split("+")
                        if(len(keys) == 1):
                            pyautogui.press(keys[0])
                        elif(len(keys) == 2):
                            pyautogui.hotkey(keys[0],keys[1])
                        elif(len(keys) == 3):
                            pyautogui.hotkey(keys[0],keys[1],keys[2])
                        else:
                            print(f"Invalid number of keybinds: {keys}")
                            
                        
                        
                except:
                    print(f"Invalid key in: {entry}")