import os
import json
import requests
#from tenacity import retry, wait_random_exponential, stop_after_attempt

#from openai import OpenAI
import openai
from termcolor import colored


class KOpenAIPretty():
    def __init__(self):
        pass

    @staticmethod
    def pretty_print_conversation(messages):
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "function": "magenta",
        }

        for message in messages:
            if message["role"] == "system":
                print(colored(f"system: {message['content']}\n",          role_to_color[message["role"]]))
            elif message["role"] == "user":
                print(colored(f"user: {message['content']}\n",            role_to_color[message["role"]]))
            elif message["role"] == "assistant" and message.              get("function_call"):
                print(colored(f"assistant:                                {message['function_call']}\n", role_to_color[message["role"]]))
            elif message["role"] == "assistant" and not message.          get("function_call"):
                print(colored(f"assistant: {message['content']}\n",       role_to_color[message["role"]]))
            elif message["role"] == "function":
                print(colored(f"function ({message['name']}):             {message['content']}\n", role_to_color[message["role"]]))


class KOpenAIMessages():
    def __init__(self):
        pass

    @staticmethod
    def format(role, message):
        return {
            'role': role,
            'content': message
        }


class KOpenAIFunctions():
    # TODO: add useful functions
    def __init__(self, functions):
        self.functions = functions

    def __len__(self):
        return len(self.functions)

    def __str__(self):
        return ', '.join(self.functions)


class KOpenAI():
    def __init__(self, model: str = 'gpt-3.5-turbo', messages: list = None):
        """
        Wrapper around openai api ft. chat completions

        Parameters
        ----------
        model:
            Look-up supported models here: https://platform.openai.com/docs/models
            and pricing here: https://openai.com/pricing
        """
        self.set_api_url()
        self.set_auth_key()
        self.set_model(model)
        self.set_headers()

        # empty by default, can also be used to load chat histories
        self.set_messages(messages)
        self.last_response = None

    def set_api_url(self):
        self.api_url = 'https://api.openai.com/v1/chat/completions'

    def set_auth_key(self):
        openai.api_key = os.environ['OPENAI_API_KEY']

    def set_model(self, model):
        self.model = model

    def set_headers(self):
        """
        Sets authentication headers
        """
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + openai.api_key,
        }

    def set_messages(self, messages):
        self.messages = messages if messages is not None else []

    def set_system_prompt(self, message):
        if len(self.messages):
            raise ValueError("System prompt must be set before any chat messages")

        self.messages.append(KOpenAIMessages.format('system', message))

    def chat_completion_with_fns(self, functions=None, function_call=None):
        # fill json_data
        json_data = {
            "model": self.model,
            "messages": self.messages
        }
        if functions is not None:
            json_data.update({"functions": functions})
        if function_call is not None:
            json_data.update({"function_call": function_call})

        # request with openai api with (auth) header, json_data
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=json_data,
            )
            return response

        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return e

    def chat(self, message, role: str = 'user', functions=None, function_call=None):
        """
        Parameters
        ----------
        role: {system, user}
            Choose system to provide the initial instruction message,
            and user for further chats
        """
        self.messages.append(KOpenAIMessages.format(role, message))
        response = self.chat_completion_with_fns(functions=functions, function_call=function_call).json()
        self.last_response = response

        assistant_message = response['choices'][0]['message']
        self.messages.append(assistant_message)

        return assistant_message

    def pprint(self):
        KOpenAIPretty.pretty_print_conversation(self.messages)


