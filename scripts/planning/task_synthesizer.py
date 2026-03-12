from scripts.services.task_service import create_task


def synthesize_tasks(feature_list):

    tasks = []

    for feature in feature_list:

        task = create_task(
            feature["title"],
            feature["description"]
        )

        tasks.append(task)

    return tasks