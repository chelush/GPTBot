import speech_recognition as sr
import pyttsx3
import time

r = sr.Recognizer()

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def recognize_speech():
    with sr.Microphone() as source:
        print("Говорите...")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language="ru-RU")
            print("Вы сказали: " + text)

            if "запусти таймер на" in text:
                duration = int(text.split()[-2])

                engine.say(f"Таймер запущен на {duration} секунд")
                engine.runAndWait()

                time.sleep(duration)

                engine.say("Таймер закончил свою работу")
                engine.runAndWait()

            elif "останови таймер" in text:
                engine.say("Таймер остановлен")
                engine.runAndWait()

                time.sleep(0)

            else:
                engine.say("Простите, я не понимаю, что вы сказали")
                engine.runAndWait()

        except:
            engine.say("Простите, я не могу распознать вашу речь")
            engine.runAndWait()


while True:
    recognize_speech()