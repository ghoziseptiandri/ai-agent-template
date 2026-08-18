# Simple AI Agent with Gemini + Python - #MakeItPublic Part 1

**Disclaimer: This project was built as a hands-on learning exercise. The code and structure evolved through experimentation, debugging, and conversations with ChatGPT.**

This is a simple AI agent project I built while learning how AI agents
actually work.

I started from a very basic Gemini chat in Python, then slowly added
tools, memory, logging, testing, and a proper agent loop. I wanted to
understand the structure instead of just copying a big framework that
already does everything for me.

So this repository is also a **starter template** for my future AI agent
projects.

> This is a learning project, not a production-ready agent yet.

## What It Can Do

At the current stage, the agent can:

-   Chat with Gemini
-   Decide when to call Python tools
-   Use a calculator tool
-   Use a current-time tool
-   Call multiple tools in one request
-   Chain tool calls across multiple agent steps
-   Keep conversation history
-   Save long-term memory
-   Update existing memory
-   Delete memory
-   Handle tool errors without immediately crashing
-   Limit the number of agent/tool loops
-   Write structured logs
-   Run automated tests with `pytest`

## What I Learned Building This

The project currently covers:

1.  Python & Virtual Environments
2.  `.env` & API Keys
3.  Gemini API & Chat
4.  Function / Tool Calling
5.  Manual Function Calling
6.  Tool Registry
7.  Project Structure
8.  `main.py` vs Agent Logic
9.  Conversation History
10. Persistent Memory
11. Memory as an Agent Tool
12. System Instructions
13. Error Handling
14. Logging & Observability
15. Automated Testing
16. Multiple & Chained Tool Calls
17. Maximum Tool-Loop Limit
18. Prompt Organization
19. Configuration Management

## Project Structure

The project is intentionally still quite simple:

``` text
ai-agent-google/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
│
├── config.py
├── logger.py
├── long_term_memory.py
├── main.py
├── manual_agent.py
├── memory.py
├── prompts.py
│
├── tools/
│   ├── __init__.py
│   ├── calculator.py
│   ├── declarations.py
│   ├── registry.py
│   └── time_tool.py
│
└── tests/
    ├── test_calculator.py
    ├── test_memory.py
    └── test_registry.py
```

A simple way I think about the files:

-   `main.py` --- starts the application
-   `manual_agent.py` --- runs the agent loop
-   `config.py` --- configuration such as the model and loop limit
-   `prompts.py` --- instructions for how the agent should behave
-   `tools/` --- things the agent is allowed to do
-   `memory.py` --- conversation memory
-   `long_term_memory.py` --- persistent facts
-   `logger.py` --- structured agent logs
-   `tests/` --- automated tests

## Requirements

I built this with:

-   Python 3.13
-   Google Gen AI Python SDK
-   Gemini API
-   `python-dotenv`
-   `pytest`

You also need a Gemini API key.

## Setup

### 1. Clone the repository

``` bash
git clone YOUR_REPOSITORY_URL
cd ai-agent-google
```

### 2. Create a virtual environment

On macOS/Linux:

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

You should now see something like:

``` text
(.venv) ...
```

You do **not** need to `cd` into `.venv`.

The point of activating it is to tell the terminal to use the Python
interpreter and packages installed specifically for this project.

### 3. Install dependencies

``` bash
python -m pip install -r requirements.txt
```

### 4. Create your `.env` and Setup the Model

Copy the example:

``` bash
cp .env.example .env
```

Then open `.env` and put your real Gemini API key there:

``` text
GEMINI_API_KEY=your_real_api_key_here
```

Do not put the real API key inside `.env.example`.

Also, never commit `.env` to Git.

Then, open `config.py` and choose the model you want to use:

```python
MODEL_NAME = "your-model-name"
```

### 5. Run the agent

``` bash
python main.py
```

Then you can start chatting with it from the terminal.

## Example: Normal Chat

``` text
You: What is the capital of Japan?

Agent: The capital of Japan is Tokyo.
```

For a normal question, Gemini can answer directly without using a tool.

## Example: Tool Calling

``` text
You: What is 29 multiplied by 3?
```

The flow is roughly:

``` text
User
  ↓
Gemini
  ↓
Gemini decides it needs calculate()
  ↓
Python runs the calculator
  ↓
87
  ↓
Result goes back to Gemini
  ↓
Final answer
```

This was one of the most important things for me to understand.

The AI is not actually executing my Python function itself.

Gemini decides **which tool it wants to use and with what arguments**.
My Python program executes the real function and sends the result back.

## Multiple Tool Calls

The agent can also handle more than one tool request.

For example:

``` text
Calculate 25 × 4 and also calculate 18 + 7.
```

The agent can request:

``` text
calculate(25, 4, "multiply")
→ 100

calculate(18, 7, "add")
→ 25
```

Instead of only reading the first function call, the code loops through
all requested function calls.

## Chained Tool Calls

A more interesting case is:

``` text
Multiply 12 by 5, then add 7 to the result.
```

That can require multiple agent steps:

``` text
12 × 5
  ↓
60
  ↓
60 + 7
  ↓
67
```

This is why the agent has a loop.

Gemini can call a tool, receive the result, think about what it needs
next, call another tool, and eventually return the final answer.

## Maximum Tool Loop

Because the agent uses a loop, I also added a maximum number of tool
rounds.

For example:

``` python
MAX_TOOL_LOOPS = 10
```

Without this, a bad tool interaction could theoretically continue:

``` text
Gemini → Tool → Gemini → Tool → Gemini → Tool → ...
```

The limit gives the agent a simple safety guard.

## Memory

I separated memory into two ideas.

### Conversation Memory

Conversation history lets the agent remember what happened earlier in
the current conversation.

Conceptually:

``` text
Message 1
   ↓
conversation history
   ↓
Message 2
```

### Long-Term Memory

Long-term memory stores useful facts separately so they can survive
after the program is restarted.

The agent has memory tools for:

``` text
CREATE → save_memory
READ   → load memory
UPDATE → update_memory
DELETE → delete_memory
```

For example:

``` text
You: Remember my favorite number is 42.
→ save_memory

You: Actually, my favorite number is 7.
→ update_memory

You: Forget my favorite number.
→ delete_memory
```

The local JSON memory files are ignored by Git because they are runtime
data, not part of the template.

## Tool Registry

Instead of writing a long chain of `if/elif` statements, tools are
registered in one place.

Conceptually:

``` python
TOOL_FUNCTIONS = {
    "calculate": calculate,
    "get_current_time": get_current_time,
    "save_memory": save_memory,
    "update_memory": update_memory,
    "delete_memory": delete_memory,
}
```

Then when Gemini requests a tool, the agent can look it up dynamically.

This also makes adding another tool much easier later.

## System Prompt

The agent instructions live separately in `prompts.py`.

I like this separation because:

``` text
prompts.py
→ how the agent should behave

tools/
→ what the agent can do

manual_agent.py
→ how the agent loop works

config.py
→ technical settings

main.py
→ starts everything
```

It keeps `manual_agent.py` from becoming one huge file.

## Logging

The agent writes structured logs so I can see what actually happened.

For example:

``` text
user_message
↓
gemini_request_start
↓
tool_requested
↓
tool_result
↓
gemini_request_start
↓
agent_response
```

A real log can look like:

``` json
{"event": "tool_requested", "data": {"tool": "calculate", "arguments": {"a": 25, "b": 4, "operation": "multiply"}}}
{"event": "tool_result", "data": {"tool": "calculate", "result": 100}}
```

This was useful because when the agent did not behave as expected, I
could see whether the problem happened before Gemini responded, during a
tool call, or after the tool result.

The generated log files are ignored by Git.

## Testing

The project uses `pytest`.

Activate the virtual environment first:

``` bash
source .venv/bin/activate
```

Then run:

``` bash
python -m pytest
```

I prefer `python -m pytest` because it makes it clear which Python
interpreter is running pytest.

At the time I turned this project into a template, I had tests for:

-   Calculator operations
-   Division by zero
-   Tool registration
-   Saving memory
-   Updating memory
-   Deleting memory
-   Duplicate memory
-   Missing memory keys

One useful lesson from this was that tests are not just something to add
for professional-looking code. One of the tests actually caught that my
calculator raised `ZeroDivisionError` while I expected my tool to raise
a cleaner `ValueError`.

## `.gitignore`

Local secrets, environments, caches, logs, and runtime memory should not
be committed.

Example:

``` gitignore
# Environment variables / secrets
.env

# Python virtual environment
.venv/

# Python cache files
__pycache__/
*.pyc

# Pytest cache
.pytest_cache/

# Application logs
agent.log
agent.jsonl

# Local agent memory / runtime data
memory.json
long_term_memory.json

# macOS system files
.DS_Store
```

## `.env.example`

The repository should include `.env.example`:

``` text
GEMINI_API_KEY=your_api_key_here
```

But the real `.env` stays local.

## Things I Intentionally Did Not Use Yet

This project does not try to hide everything behind an agent framework.

That is intentional.

For learning, I wanted to see the manual flow:

``` text
User
 ↓
Model
 ↓
Function request
 ↓
Python tool
 ↓
Function result
 ↓
Model
 ↓
Answer
```

Once I understand that properly, using a higher-level framework later should make much more sense.


I am intentionally building these one by one instead of adding everything at once.

## A Few Notes

This repository is mainly for learning and experimentation.

Gemini model availability, API limits, SDK behavior, and pricing can
change, so you may need to update the model or SDK configuration
depending on when you use this template.

Also, API usage is separate from a ChatGPT subscription or other AI
subscriptions. Each provider has its own API access, limits, and
billing.

## Why I Made This

At first I could make an AI answer a question, but I did not really
understand what made something an **agent** instead of just a chatbot.

Building it manually helped me understand the difference:

``` text
Chatbot:
User → AI → Answer

Agent:
User → AI → Decide → Tool → Result → AI → Answer
```

Then memory, multiple tools, chained calls, logging, tests, and safety
limits started to make much more sense.

This template is basically my checkpoint before moving into the next
part of learning AI agents.

## References

I used these resources while learning and building this project:

- Google Gemini API documentation
- Google Gen AI Python SDK
- Gemini Function Calling documentation
- Python Virtual Environments documentation
- python-dotenv documentation
- pytest documentation