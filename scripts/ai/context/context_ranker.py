import heapq


def rank_context(items):

    ranked = []

    for item in items:

        score = item.get("priority", 1)

        heapq.heappush(ranked, (-score, item))

    results = []

    while ranked:

        results.append(heapq.heappop(ranked)[1])

    return results