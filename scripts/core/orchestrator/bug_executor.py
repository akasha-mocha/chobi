from scripts.services.bug_service import create_bug


def process_test_result(task, test_result):

    if test_result["success"]:
        return

    print("Bug detected")

    create_bug(
        task["id"],
        "Test failed",
        test_result.get("stderr", "")
    )