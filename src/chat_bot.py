import os

from src.initializer import llm
from src.tools import extract_info, search_papers, tools

mapping_tool_function = {"search_papers": search_papers, "extract_info": extract_info}


def execute_tool(tool_name, tool_args):

    result = mapping_tool_function[tool_name](**tool_args)

    if result is None:
        result = "The operation completed but didn't return any results."

    elif isinstance(result, list):
        result = ", ".join(result)

    elif isinstance(result, dict):
        # Convert dictionaries to formatted JSON strings
        result = json.dumps(result, indent=2)

    else:
        # For any other type, convert using str()
        result = str(result)
    return result


def process_query(query):

    messages = [{"role": "user", "content": query}]

    response = llm.messages.create(
        max_tokens=2024,
        model="claude-sonnet-4-5-20250929",
        tools=tools,
        messages=messages,
    )

    process_query = True
    while process_query:
        assistant_content = []

        for content in response.content:
            if content.type == "text":

                print(content.text)
                assistant_content.append(content)

                if len(response.content) == 1:
                    process_query = False

            elif content.type == "tool_use":

                assistant_content.append(content)
                messages.append({"role": "assistant", "content": assistant_content})

                tool_id = content.id
                tool_args = content.input
                tool_name = content.name
                print(f"Calling tool {tool_name} with args {tool_args}")

                result = execute_tool(tool_name, tool_args)
                messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_id,
                                "content": result,
                            }
                        ],
                    }
                )
                response = llm.messages.create(
                    max_tokens=2024,
                    model="claude-sonnet-4-5-20250929",
                    tools=tools,
                    messages=messages,
                )

                if len(response.content) == 1 and response.content[0].type == "text":
                    print(response.content[0].text)
                    process_query = False


def chat_loop():
    print("Type your queries or 'quit' to exit.")
    while True:
        try:
            query = input("\nQuery: ").strip()
            if query.lower() == "quit":
                break

            process_query(query)
            print("\n")
        except Exception as e:
            print(f"\nError: {str(e)}")
