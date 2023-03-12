import numpy as np
import speech_recognition as sr
from gtts import gTTS
import os
import datetime
import transformers


#build the AI
class chatbot():
    def __init__(self, name):
        print("___starting up", name,"___")
        self.name = name


    #speech to text (1st NLP func)
    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:

            print("listening...")
            audio = recognizer.listen(mic)
            self.text="ERROR"
        try:
            self.text = recognizer.recognize_google(audio)
            print("me-->", self.text)
        except:
            print("ERROR")


    #text to speech
    @staticmethod
    def text_to_speech(text):
        print("ai -->", text)
        speaker =  gTTS(text=text, lang="en", slow=False)
        speaker.save("res.mp3")
        statbuf = os.stat("res.mp3")
        mbytes = statbuf.st_size / 1024
        duration = mbytes / 200
        os.system("start res.mp3")
        os.system("close res.mp3")
        os.remove("res.mp3")

    # wake word config
    def wake_up(self, text):
        return True if self.name in text.lower() else False

    @staticmethod
    def action_time():
        datetime.datetime.now().time().strftime('%H:%M')






#run the AI
if __name__ == "__main__":
    ai = chatbot(name="suji")
    nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    ex = True
    while ex:
        ai.speech_to_text()
        if ai.wake_up(ai.text) is True:
            res = "hello I am zuzie the AI , what can i do for you?"
        #time
        elif "time" in ai.text:
            res = ai.action_time()
        #response
        elif any(i in ai.text for i in ["thank", "thanks"]):
            res = np.random.choice(["you are welcome!","anytime","cool!","I am here if you need me","peace out!"])

        #conversational
        else:
            if ai.text=="ERROR":
                res="sorry, come again?"
            else:
                chat = nlp(transformers.Conversation(ai.text), pad_token_id=50256)
                res = str(chat)
                res = res[res.find("bot >> ")+6:].strip()

        ai.text_to_speech(res)
    print("____closing down zuzie____")