MAX_CONTEXT_CHARS = 12000


def trim(text):

    if len(text) <= MAX_CONTEXT_CHARS:

        return text

    return text[:MAX_CONTEXT_CHARS]


def optimize(context):

    optimized = {}

    for key, value in context.items():

        if isinstance(value, str):

            optimized[key] = trim(value)

        else:

            optimized[key] = value

    return optimized