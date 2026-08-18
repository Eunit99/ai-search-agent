import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

search_tool_definition = {
    "type": "function",
    "function": {
        "name": "search_web",
        "description": (
            "Call this tool whenever you need up-to-date information, news, "
            "current events, or web data that occurred after your knowledge cutoff date."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The optimized search query string to look up on Google."
                },
                "location": {
                    "type": "string",
                    "description": "Geographical location filter for search targeting. Defaults to 'United States'.",
                    "default": "United States"
                }
            },
            "required": ["query"]
        }
    }
}


def ask_agent(user_prompt: str):
    """
    Sends a query to the LLM along with the available search tool definition.
    The LLM determines autonomously whether it needs to execute a Google search.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a factual, precise AI search agent with live web access via SearchApi. "
                "Use the search_web tool when you need current or time-sensitive information. "
                "Answer directly only for timeless facts, historical events, or technical concepts."
            )
        },
        {"role": "user", "content": user_prompt}
    ]

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=[search_tool_definition],
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        print("Agent decision: 'I need to use SearchApi to look up live information on the web.'")
        return {"status": "tool_call_required", "data": tool_calls, "message_history": messages}
    else:
        print("Agent decision: 'I can answer this question from my existing knowledge.'")
        return {"status": "completed", "data": response_message.content}
