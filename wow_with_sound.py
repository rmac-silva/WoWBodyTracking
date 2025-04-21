from src.speech_module import SpeechModule,SpeechManager

def load_commands():
    
    file = "./sound_commands.cfg"
    
    commands = []
    
    with open(file, 'r') as f:
        f.readline() #Skip first
        for line in f:
            line = line.strip()  # Remove leading/trailing whitespace
            if not line or line.startswith('#'):
                continue  # Skip empty lines and comments
            
            args = line.split(":")
            
            command_words = args[0].strip().split("|")
            
            for word in command_words:
                key = str(args[1].split("#")[0].strip())
                
                commands.append( (word,key) )
                
            
    return commands
        
def create_sample_commands():
    config_text = """
# Voice command | command1 | command2 : Keypress # Combinations still not yet possible
quit program : exit #Reserved, do not delete, unless you don't walk to quit
walk : forward_walk #Reserved, do not delete, unless you don't want to walk
stop : stop_walk #Reserved, do not delete, unless you don't want to stop walking
shadowbolt | shadow bolt : 1
    """
    
    with open("sound_commands.cfg", "x") as file:
        file.write(config_text.strip())
try:
    commands = load_commands()
except:
    create_sample_commands()
    commands = load_commands()
finally:
    print(f"\nLoaded commands:\n{commands}")
    sm = SpeechModule()
    speech_manager = SpeechManager(commands,sm)
    print("\nStarting Speech Interpreter...\n")
    speech_manager.run()
