import speech_recognition as sr
import openai
from customtkinter import CTk, CTkLabel, CTkButton, CTkFont, set_appearance_mode, set_default_color_theme
from tkinter import *

import config
from subprocess import call

set_appearance_mode("dark")
set_default_color_theme("dark-blue")


class App(CTk):
    def __init__(self):
        super().__init__()

        self.r = sr.Recognizer()

        self.geometry("720x720")
        self.title("GPTBot")
        self.resizable(False, False)
        self.Font = CTkFont("Roboto", 27)

        self.client_label = CTkLabel(self, text="Вы сказали:", font=self.Font)
        self.client_label.pack()

        self.client_ask_text = StringVar()
        self.client_ask = CTkLabel(self, textvariable=self.client_ask_text, text_color='white', bg_color='gray',
                                   wraplength=700, width=700, font=self.Font, corner_radius=2)
        self.client_ask.pack(ipady=25)

        self.bot_label = CTkLabel(self, text="Ответ:", font=self.Font)
        self.bot_label.pack()

        self.bot_answer_text = StringVar()
        self.bot_answer = CTkLabel(self, textvariable=self.bot_answer_text, text_color='white', bg_color='gray',
                                   wraplength=700, width=700, font=self.Font, corner_radius=2)
        self.bot_answer.pack(ipady=75)

        self.say_button = CTkButton(self, text='Сказать', width=250, height=50, command=self.recognize_speech,
                                    font=self.Font)
        self.say_button.pack(pady=10)

    def askGPT(self, text):
        openai.api_key = config.TOKEN
        response = openai.Completion.create(engine="text-davinci-003", prompt=text, temperature=0.6,
                                            max_tokens=500,
                                            top_p=1,
                                            frequency_penalty=0,
                                            presence_penalty=1)
        return response.choices[0].text

    def recognize_speech(self):
        with sr.Microphone() as source:
            print("Говорите...")
            self.client_ask_text.set("Говорите...")
            self.update()
            audio = self.r.listen(source)

            text = self.r.recognize_google(audio, language="ru-RU").lower()
            print("Вы сказали: " + text)
            self.client_ask_text.set(text)
            self.bot_answer_text.set('Думаю...')
            self.update()

            response = self.askGPT(text).lstrip('\n')

            response = response[::-1]
            response = response[response.find(".") + 1:][::-1]

            self.bot_answer_text.set(response)
            self.update()
            print("Бот ответил: " + response)
            call(["python3", "speak.py", response])


if __name__ == '__main__':
    app = App()
    app.mainloop()
