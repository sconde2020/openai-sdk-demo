"""Tool schemas sent to the model — like method signatures in a Java interface.

The model reads these to decide when and how to call each tool.
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_biggest_cities",
            "description": "Returns the three biggest cities of a given country by population. Sorte the result by population in descending order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "description": "Country name in English (e.g. 'Brazil').",
                    }
                },
                "required": ["country"],        # like @NotNull in Jakarta
                "additionalProperties": False,  # like @JsonIgnoreProperties
            },
        },
    }
]
