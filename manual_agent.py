from google.genai import types
from config import MAX_TOOL_LOOPS, MODEL_NAME, client
from tools.declarations import GEMINI_TOOLS
from tools.registry import TOOL_FUNCTIONS
from logger import log
from prompts import SYSTEM_INSTRUCTION

def run_agent(
    user_input: str,
    contents: list,
    memory_context: str = ""
) -> tuple[str, list]:

    if memory_context:
        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=memory_context)
                ]
            )
        )

    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=user_input)
            ],
        )
    )

    log(
        "user_message",
        {
            "text": user_input
        }
    )

    # ... add user message etc.

    for loop_count in range(MAX_TOOL_LOOPS):

        log(
            "agent_loop",
            {
                "loop": loop_count + 1
            }
        )

        log("gemini_request_start")

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=types.GenerateContentConfig(
                    tools=GEMINI_TOOLS,
                    system_instruction=SYSTEM_INSTRUCTION,
                ),
            )

        except Exception as e:
            log(
                "gemini_error",
                {
                    "type": type(e).__name__,
                    "message": str(e),
                }
            )

            return f"Gemini API error: {e}", contents

        # Your existing function-call handling
        if response.function_calls:
            # execute tools
            # append results

            continue

        # No more tool calls = final answer
        contents.append(
            response.candidates[0].content
        )

        log(
            "agent_response",
            {
                "text": response.text
            }
        )

        return response.text, contents

    # We only reach here if all loops were used
    log(
        "max_tool_loops_reached",
        {
            "limit": MAX_TOOL_LOOPS
        }
    )

    return (
        "The agent reached the maximum number of tool steps.",
        contents
    )