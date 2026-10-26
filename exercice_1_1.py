from utils import Calculator, make_tools, make_registry, call_llm

tools = make_tools([Calculator])
registry = make_registry([Calculator])
print(tools)

message = {
    "content": "What is 15 times 8 ?", 
    "role": "user"
}

print(call_llm([message], tools=tools))