from scripts.ai.context.context_filter import filter_context
from scripts.ai.context.context_ranker import rank_context
from scripts.ai.context.context_compressor import compress


def build_context(context):

    context = filter_context(context)

    ranked = rank_context([
        {"priority": 5, "data": context.get("task")},
        {"priority": 4, "data": context.get("architecture")},
        {"priority": 3, "data": context.get("code")},
        {"priority": 2, "data": context.get("memory")},
    ])

    final = {}

    for item in ranked:

        data = item["data"]

        if isinstance(data, str):

            final[str(len(final))] = compress(data)

    return final