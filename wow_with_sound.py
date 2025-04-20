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

commands = load_commands()
print(f"\nLoaded commands:\n{commands}")
sm = SpeechModule()
speech_manager = SpeechManager(commands,sm)
print("\nStarting Speech Interpreter...\n")
speech_manager.run()
