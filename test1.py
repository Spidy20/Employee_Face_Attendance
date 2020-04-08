import pyttsx3
#Intialize pyttx engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#Set voice 1 for ladies voice, 0 for Gents.
engine.setProperty('voice', voices[1].id)
def speak(audio):
    #Speak the lines which you written
    engine.say(audio)
    engine.runAndWait()
#Fucntion call
speak("Follow Machine learning hub")