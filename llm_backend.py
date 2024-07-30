import os
from anthropic import AsyncAnthropic
from typing import Dict, List
import uuid
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="[%(pathname)s:%(lineno)d | (%(funcName)s)] %(message)s")


class Client:
    _AVAILABLE_CLIENTS = {"claude", "chatgpt"}

    def __init__(self, client_name: str = ""):
        if client_name.lower() not in Client._AVAILABLE_CLIENTS:
            raise ValueError(
                f"input {client_name} not part of valid arguments: {Client._AVAILABLE_CLIENTS}")

        API_KEY_ENV = "ANTHROPIC_TOKEN"
        api_key = os.getenv(API_KEY_ENV)

        self.model_name = "claude-3-5-sonnet-20240620"
        self.max_tokens = 1000
        self.temperature = 0

        self.client_anthropic = AsyncAnthropic(api_key=api_key)
        self.threads: Dict[str, List[Dict[str, str]]] = dict()

    async def send_in_thread(self, message: str, thread_id: str = "") -> str:
        if thread_id != "" and thread_id not in self.threads:
            raise ValueError(f"thread id: {thread_id} not found in threads")

        if message == "":
            raise ValueError("message is empty")

        thread_uuid = thread_id
        if thread_id != "":
            self.threads[thread_uuid].append(
                {"role": "user", "content": str(message)})
        else:
            thread_uuid = uuid.uuid4()
            self.threads[thread_uuid] = [
                {"role": "user", "content": str(message)}]

        api_response_message = await self.client_anthropic.messages.create(
            model=self.model_name,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=self.threads[thread_uuid],
        )

        # always expect one response in return
        if len(api_response_message.content) != 1:
            raise ValueError(f"unexpected return: {api_response_message}")

        response_str: str = api_response_message.content[0].text
        self.threads[thread_uuid].append(
            {"role": "assistant", "content": response_str})

        return response_str
