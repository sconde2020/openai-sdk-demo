"""Central configuration — all tuneable parameters in one place.

Java equivalent: an @ConfigurationProperties class or application.properties file.
"""

# OpenAI model used for all calls (agent loop + data fetch).
MODEL = "gpt-4o-mini"

# Number of cities to return per query.
TOP_N = 3

# System prompt for the agent loop (runner.py).
AGENT_SYSTEM_PROMPT = (
    "You are a helpful assistant. When asked about the biggest cities of a country, "
    "always call the get_biggest_cities tool. Present the result as a numbered list."
)

# System prompt for the data-fetch call (handlers.py).
# The {top_n} placeholder is filled at runtime — like String.format() in Java.
DATA_SYSTEM_PROMPT = (
    "You are a geography expert. "
    "When given a country name, respond ONLY with a JSON object. "
    "The object must have a single key 'cities' whose value is a list "
    "of the {top_n} most populous cities for that country, ordered largest first. "
    'Example format: {{"cities": ["Tokyo", "Yokohama", "Osaka"]}}'
)
