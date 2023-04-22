import speech_recognition as sr
import pyttsx3
import time
import asyncio

r = sr.Recognizer()

engine = pyttsx3.init()
engine.setProperty('voice', 'ru')

async def recognize_speech():
    with sr.Microphone() as source:
        print("Говорите...")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language="ru-RU").lower()
            print("Вы сказали: " + text)

            if "запусти таймер на" in text:
                duration = int(text.split()[-2])

                engine.say(f"Таймер запущен на {duration} секунд")
                engine.runAndWait()

                await asyncio.sleep(duration)

                engine.say(f"Таймер остановлен.")
                engine.runAndWait()


            elif "останови таймер" in text:
                engine.say("Таймер остановлен")
                engine.runAndWait()

                time.sleep(0)

            elif "сколько будет" in text:
                value1 = int(text.split()[2])
                value2 = int(text.split()[4])
                operation = text.split()[3]

                operations = {
                    'умножить': lambda a, b: a * b,
                    'х': lambda a, b: a * b,
                    'плюс': lambda a, b: a + b,
                    '+': lambda a, b: a + b,
                    'минус': lambda a, b: a - b,
                    '-': lambda a, b: a - b,
                    'делить': lambda a, b: a / b,
                    '/': lambda a, b: a / b,
                }

                result = operations[operation](value1, value2)

                engine.say(f"Будет {result}")
                engine.runAndWait()

            else:
                engine.say("Простите, я не понимаю, что вы сказали")
                engine.runAndWait()

        except:
            engine.runAndWait()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(recognize_speech())
