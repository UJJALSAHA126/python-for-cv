from math import inf
import speech_recognition as sr
import pyttsx3
import wikipedia
import pywhatkit
import pyjokes

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print("Give me a command.")
            voice = listener.listen(source=source)
            command = listener.recognize_google(voice)
    except:
        pass
    return command


def talk(line: str, printAlso: bool = False):
    if printAlso:
        print(line)
    engine.say(line)
    engine.runAndWait()


def playOnYouTube(search: str):
    pywhatkit.playonyt(search)


def searchOnWikipedia(search: str):
    print(search)
    info = wikipedia.summary(search)
    print(info)


def processTheCommandInput(command: str):
    if "play on YouTube" in command:
        cm = command.replace("play on YouTube", "")
        talk("Openning YouTube")
        playOnYouTube(cm)

    elif "search about" in command:
        cm = command.replace("search about", "")
        talk("Searching")
        searchOnWikipedia(cm)

    elif "joke" in command:
        jk = pyjokes.get_joke()
        print(jk)
        talk(jk)


def main():
    talk("Initializing Your Voice Assistant. Please Wait",printAlso=True)
    # command = take_command()
    # processTheCommandInput(command=command)
    # searchOnWikipedia('Elon Musk')


if __name__ == '__main__':
    main()
