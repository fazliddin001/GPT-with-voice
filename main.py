import speech_recognition as sr
import pyttsx3 as py
import openai
import config


class Speaker:
    def __init__(self):
        self.ttx = py.init()
        self.voices = self.ttx.getProperty('voices')
        self.ttx.setProperty("voice", self.voices[1].id)

    def speak(self, text: str):
        self.ttx.say(text=text)
        self.ttx.runAndWait()


class Microphone:
    def __init__(self):
        self.r = sr.Recognizer()

    def voice_text(self):
        with sr.microphone as source:
            self.r.adjust_for_ambient_noise(source, 1.2)
            audio = self.r.listen(source)
            try:
                response = self.r.recognize_google(audio, language='ru-RU')
                return response
            except Exception as exc:
                print(exc)
                return None


class Ai:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=config.openai_key,
        )
        self.messages = []

    def request(self, text: str):
        message = {"role": "user", "content": text}
        self.messages.append(message)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            stream=False
        )

        return response.choices[0].message.content


class App:
    def __init__(self):
        self.speaker = Speaker()
        self.ai = Ai()
        self.microphone = Microphone()

    def run(self):

        while True:
            try:
                text = self.microphone.voice_text()
            except:
                text = input("Say something to chat-gpt: ")

            response = self.ai.request(text=text)

            print(f"Gpt response: {response}")
            self.speaker.speak(text=text)


if __name__ == '__main__':
    App().run()
