import speech_recognition as sr
import pyttsx3 as py
import openai
import config
from typing import NoReturn


class Speaker:
    """
    This class helps to play voice contents in this program
    """
    def __init__(self):
        # pyttsx3 code from official documentation to set voice/speaker
        # https://pyttsx3.readthedocs.io/en/latest/engine.html#the-engine-factory

        self.ttx = py.init()
        self.voices = self.ttx.getProperty('voices')
        self.ttx.setProperty("voice", self.voices[1].id)

    def speak(self, text: str) -> None:
        """
        This method plays the given text as a voice. This method blocks the program until
        the voice has been played.
        :param text: the parameter which will be given as argument to say method of the pyttsx3 object:
        :return:
        """
        self.ttx.say(text=text)
        self.ttx.runAndWait()


class Microphone:
    """
    This class is created to get voice content from user and handle it
    """
    def __init__(self):
        # Here we create recognizer of the speech recognize library
        self.r = sr.Recognizer()

    def voice_text(self) -> str | None:
        """
        This method returns the voice user speaks from outside
        :return:
        """
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
    """
    This class created to handle AI and get responses from it
    """
    def __init__(self):
        # Setting main parameters like client and messages which we will save in each request
        # https://platform.openai.com/docs/introduction
        self.client = openai.OpenAI(
            api_key=config.openai_key,
        )
        self.messages = []

    def request(self, text: str) -> str:
        """
        This method sends requests to the AI and returns the response
        request renders as a user
        :param text:
        :return:
        """
        message = {"role": "user", "content": text}
        self.messages.append(message)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            stream=False
        )

        return response.choices[0].message.content


class App:
    """
    The main class which handle the application at all
    """
    def __init__(self):
        """
        Initialize the application and create objects of classes Speaker, Ai, Microphone
        """
        self.speaker = Speaker()
        self.ai = Ai()
        self.microphone = Microphone()

    def run(self) -> NoReturn:
        """
        Run the application.
        :return:
        """
        while True:
            text = self.microphone.voice_text()
            if not text:
                """
                if there is any error with user's microphone or internet connection, this function returns None
                and then we ask user to enter text with input
                """

                text = input("Say something to chat-gpt: ")

            response = self.ai.request(text=text)

            print(f"Gpt response: {response}")
            self.speaker.speak(text=text)


if __name__ == '__main__':
    App().run()
