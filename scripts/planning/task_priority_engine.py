def prioritize(tasks):

    def score(task):

        priority = task.get("priority", 1)

        if task["status"] == "open":
            priority += 5

        return priority

    return sorted(tasks, key=score, reverse=True)