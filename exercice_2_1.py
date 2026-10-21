from utils import Calculator, make_tools, make_registry, call_llm, execute_tool
import sys

MAX_ITERATIONS = 5

def agent_loop(question: str, system_prompt: str = "" ):
    tools = make_tools([Calculator])
    registry = make_registry([Calculator])

    messages = [
        {
            "content": system_prompt + question, 
            "role": "user"
        }
    ]


    for iteration in range(MAX_ITERATIONS):
        answer = call_llm(messages, tools=tools)

        if answer["choices"][0]["finish_reason"] == "stop":
            return answer["choices"][0]["message"]["content"]
    
        elif answer["choices"][0]["finish_reason"] == "tool_calls":
            messages.append(answer["choices"][0]["message"])
            tool_calls = answer["choices"][0]["message"]["tool_calls"]
            for tool_call in tool_calls:
                messages.append({
                    "role" : "tool", 
                    "tool_call_id": tool_call["id"],
                    "content": execute_tool(
                        tool_call, 
                        registry
                        )
                    })
        else:
            print("ALERTE !\n", answer)
    
    return "Max iterations reached"

if __name__ == "__main__":
    if sys.argv[1]:
        print(agent_loop(str(sys.argv[1])))