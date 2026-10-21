from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from utils import Calculator, make_tools, make_registry, call_llm, execute_tool

@dataclass
class WordCounter:
    """ Count the total number of words in a text. """
    text: str

    def __call__(self) -> int:
        return len(self.text.split())


tools = make_tools([Calculator, WordCounter])
registry = make_registry([Calculator, WordCounter])

messages = [{"role" : "user", "content" : "How many words are in 'Hello world, this is a test'?"}]

response = call_llm(messages=messages, tools=tools)
print("\n")
print(response)

messages.append(response['choices'][0]['message'])

tool_response = execute_tool(response['choices'][0]['message']['tool_calls'][0], registry)
messages.append({"role" : "tool", "tool_call_id" : response['choices'][0]['message']['tool_calls'][0]['id'], "content": tool_response})

final_reponse = call_llm(messages=messages, tools=tools)
print("\n")
print(final_reponse)