def get_ready_tasks(tasks):

    ready = []

    for task in tasks:

        deps = task.get("dependencies", [])

        if not deps:

            ready.append(task)

    return ready