"""Single-call structured output — no tool loop, no dispatch layer.

Instead of a tool schema + agent loop, we define the expected JSON shape
with a Pydantic model and let the SDK enforce it.
Java analogy: like annotating a return type with @ResponseBody + a DTO class,
the framework handles serialization for you.
"""

from openai import OpenAI
from pydantic import BaseModel  # data class with built-in validation — like a Java record

MODEL = "gpt-4o-mini"
TOP_N = 3


class CitiesResult(BaseModel):
    """Expected JSON shape returned by the model.

    Java equivalent:
        public record CitiesResult(List<String> cities) {}
    """
    cities: list[str]  # list[str] == List<String> in Java


def run(country: str, client: OpenAI | None = None) -> str:
    """Ask the model for the top N cities and return them as a numbered list.

    Java equivalent: public String run(String country, OpenAI client)
    """
    if client is None:
        client = OpenAI()

    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a geography expert."},
            {
                "role": "user",
                "content": (
                    f"List the {TOP_N} most populous cities in {country}, "
                    "in descending order by population."
                ),
            },
        ],
        # response_format enforces the JSON shape — the SDK validates the response
        # against CitiesResult and raises if the model deviates.
        response_format=CitiesResult,
    )

    # .parsed is already a CitiesResult object — no json.loads() needed.
    # Java equivalent: objectMapper.readValue(body, CitiesResult.class)
    result: CitiesResult = response.choices[0].message.parsed

    # enumerate() yields (index, value) pairs — like a Java for-each with a counter.
    return "\n".join(f"{i + 1}. {city}" for i, city in enumerate(result.cities))