"""Single-call structured output — no tool loop, no dispatch layer.

The expected JSON shape is enforced by a Pydantic model.
Java analogy: like a @ResponseBody DTO — the framework handles serialization.
"""

from openai import OpenAI
from pydantic import BaseModel  # data class with built-in validation — like a Java record

from agent.config import MODEL, TOP_N, SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


class CitiesResult(BaseModel):
    """Expected JSON shape returned by the model.

    Java equivalent: public record CitiesResult(List<String> cities) {}
    """
    cities: list[str]  # list[str] == List<String> in Java


def run(country: str, client: OpenAI | None = None) -> str:
    """Ask the model for the top N cities and return them as a numbered list.

    Java equivalent: public String run(String country, OpenAI client)
    """
    if client is None:
        client = OpenAI()  # reads OPENAI_API_KEY from env

    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                # .format() fills the placeholders — like String.format() in Java.
                "content": USER_PROMPT_TEMPLATE.format(country=country, top_n=TOP_N),
            },
        ],
        # response_format enforces the JSON shape and raises if the model deviates.
        response_format=CitiesResult,
    )

    # .parsed is already a CitiesResult object — no json.loads() needed.
    result: CitiesResult = response.choices[0].message.parsed

    # enumerate() yields (index, value) pairs — like a for-each with a counter in Java.
    return "\n".join(f"{i + 1}. {city}" for i, city in enumerate(result.cities))
