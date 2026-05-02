"""Central configuration — all tuneable parameters in one place.

Java equivalent: an @ConfigurationProperties class or application.properties file.
"""

# OpenAI model used for all calls.
MODEL = "gpt-4o-mini"

# Number of cities to return per query.
TOP_N = 3

# Instructions given to the model before the user message.
SYSTEM_PROMPT = "You are a geography expert."

# Template for the user message. {country} and {top_n} are filled in at runtime.
# f-strings resolve at call time — like String.format() in Java.
USER_PROMPT_TEMPLATE = (
    "List the {top_n} most populous cities in {country}, "
    "in descending order by population."
)
