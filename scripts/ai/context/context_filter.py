def filter_context(context):

    filtered = {}

    for key, value in context.items():

        if not value:
            continue

        if isinstance(value, str) and len(value) < 5:
            continue

        filtered[key] = value

    return filtered