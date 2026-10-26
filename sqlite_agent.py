from utils import Database, Calculator, make_tools, make_registry, call_llm, execute_tool, make_sql_tools
from typing import Optional
import sys

SYSTEM_PROMPT = """You are a SQL assistant with access to a SQLite database.

Tools:
- ListTables: list all tables
- DescribeTable: get table structure
- SQLQuery: execute any SQL query

Think step by step. Explore the schema first, then query.
Explain your reasoning before each tool call."""



MAX_ITERATIONS = 5

def agent_loop(question: str, tools: Optional[list] = None):
    tools_desc = make_tools(tools)
    registry = make_registry(tools)

    messages = [
        {
            "content": SYSTEM_PROMPT, 
            "role": "user"
        },
        {
            "content": question, 
            "role": "user"
        }
    ]

    for iteration in range(MAX_ITERATIONS):
        print(f"iteration {iteration}")
        answer = call_llm(messages, tools=tools_desc)

        if answer["choices"][0]["finish_reason"] == "stop":
            return answer["choices"][0]["message"]["content"]
    
        elif answer["choices"][0]["finish_reason"] == "tool_calls":
            messages.append(answer["choices"][0]["message"])
            tool_calls = answer["choices"][0]["message"]["tool_calls"]
            for tool_call in tool_calls:
                print("tool_call", tool_call, "res", execute_tool(tool_call, registry))
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

    db = Database("library.db") 

    sql_tools = make_sql_tools(db)

    questions = [
        "What are the books written after 1970?",
        "Who is the author of 'Dune' and when were they born?",
        "How many books are there per genre?",
        "What is the average rating per publisher?",
        "Which author has written the most books?",
    ]

    for question in questions:
        print(question)
        print(agent_loop(question, sql_tools))

