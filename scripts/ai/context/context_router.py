def route_context(task, context):

    task_type = task.get("type")

    if task_type == "bug":

        return {

            "task": context["task"],
            "related_code": context.get("code")

        }

    if task_type == "feature":

        return {

            "task": context["task"],
            "architecture": context.get("architecture"),
            "spec": context.get("spec")

        }

    return context