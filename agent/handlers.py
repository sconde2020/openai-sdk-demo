"""Business logic layer — like a @Service in Spring Boot.

runner.py decides WHEN to call a tool; this module does the actual data fetch
via a second OpenAI call, returning structured JSON (no static list, no extra library).
"""

import json
from openai import OpenAI

from agent.config import MODEL, TOP_N, DATA_SYSTEM_PROMPT


def get_biggest_cities(country: str) -> str:
    """Return JSON with the top N cities for *country*, or an error JSON on failure.

    Java equivalent: public String getBiggestCities(String country)
    """
    client = OpenAI()  # reads OPENAI_API_KEY from env — like new OpenAI(System.getenv(...))

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                # .format() fills the {top_n} placeholder — like String.format() in Java.
                {"role": "system", "content": DATA_SYSTEM_PROMPT.format(top_n=TOP_N)},
                {"role": "user", "content": f"Country: {country}"},  # f-string == String.format()
            ],
            response_format={"type": "json_object"},  # forces valid JSON output
            temperature=0,  # deterministic — no creativity needed
        )

        data = json.loads(response.choices[0].message.content)  # like ObjectMapper.readValue()
        return json.dumps({"country": country, "cities": data["cities"]})

    except KeyError:
        # Model returned JSON without the "cities" key.
        return json.dumps({"error": f"Unexpected JSON format for '{country}'."})
    except json.JSONDecodeError as exc:
        return json.dumps({"error": f"Could not parse model response: {exc}"})
    except Exception as exc:
        # Catches network errors, auth errors, rate limits, etc.
        return json.dumps({"error": f"OpenAI call failed: {exc}"})


# Map<String, Function<Map<String,Object>, String>> in Java terms.
TOOL_HANDLERS: dict[str, callable] = {
    "get_biggest_cities": lambda args: get_biggest_cities(args["country"]),  # lambda == Java lambda
}
