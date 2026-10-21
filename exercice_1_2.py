from utils import Calculator, make_tools, make_registry, call_llm, execute_tool

tools = make_tools([Calculator])
registry = make_registry([Calculator])

messages = [
    {
        "content": "What is 15 times 8 ?", 
        "role": "user"
    }

]


ans1 = call_llm(messages, tools=tools)

print(ans1)

messages.append(ans1["choices"][0]["message"])

messages.append({
    "role" : "tool", 
    "tool_call_id": ans1["choices"][0]["message"]["tool_calls"][0]["id"],
    "content": execute_tool(
        ans1["choices"][0]["message"]["tool_calls"][0], 
        registry
        )
    })

# messages.append({
#     "role" : "tool", 
#     "tool_call_id": ans1["choices"][0]["message"]["tool_calls"][0]["id"],
#     "content": "5"
#     })

print("messages\n", messages)

ans2 = call_llm(messages, tools=tools)

print("ans2\n", ans2)
