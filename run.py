import json
from agent import ask_agent, openai_client
from search_helper import search_web


def run_agent_loop(user_prompt: str):
    """
    The orchestrator runtime loop. Prompts the agent, detects tool requests,
    executes the SearchApi call, updates conversation history, and generates
    the final web-informed answer.
    """
    print(f"\nUser: {user_prompt}")

    result = ask_agent(user_prompt)

    if result["status"] == "completed":
        print(f"\nFinal answer:\n{result['data']}\n")
        return

    if result["status"] == "tool_call_required":
        tool_calls = result["data"]
        messages = result["message_history"]

        assistant_msg = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                } for tc in tool_calls
            ]
        }
        messages.append(assistant_msg)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"Invoking tool: {function_name}() with arguments {function_args}")

            if function_name == "search_web":
                search_query = function_args.get("query")
                search_location = function_args.get("location", "United States")
                raw_search_results = search_web(query=search_query, location=search_location)

                tool_response_msg = {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": raw_search_results
                }
                messages.append(tool_response_msg)
            else:
                print(f"Warning: model requested unknown tool: {function_name}")
                return

        print("Synthesizing live search data into a comprehensive answer...")
        final_response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        print(f"\nFinal answer:\n{final_response.choices[0].message.content}\n")


if __name__ == "__main__":
    run_agent_loop("What were the top 3 tech stock market trends in Q1 of 2026?")
    run_agent_loop("Explain the fundamental difference between a SQL and NoSQL database in two sentences.")
