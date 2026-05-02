"""Orchestration layer — like a @Controller in Spring Boot.

Owns the conversation state (messages list) and drives the agent loop:
send → check tool calls → dispatch → repeat until the model says "stop".
"""

import json
from openai import OpenAI

from agent.tools import TOOLS
from agent.handlers import TOOL_HANDLERS
from agent.config import MODEL, AGENT_SYSTEM_PROMPT


def run(user_query: str, client: OpenAI | None = None) -> str:
    """Run the agent for one query and return the final text answer.

    Java equivalent: public String run(String userQuery, OpenAI client)
    OpenAI | None  == Optional<OpenAI> — a new client is created when None is passed.
    """
    if client is None:
        client = OpenAI()

    # List<Map<String,String>> — the full conversation history sent on every request.
    messages = [
        {"role": "system", "content": AGENT_SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ]

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        choice = response.choices[0]  # like List.get(0)

        if choice.finish_reason == "stop":
            return choice.message.content  # model is done — return the text

        # Model requested tool calls — process each one.
        messages.append(choice.message)  # must be added before the tool results

        for tc in choice.message.tool_calls:
            args = json.loads(tc.function.arguments)  # like ObjectMapper.readValue()
            handler = TOOL_HANDLERS.get(tc.function.name)  # .get() returns None if missing
            result = handler(args) if handler else json.dumps({"error": "unknown tool"})  # ternary

            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

        # Loop back — model reads the tool results and produces the next response.
