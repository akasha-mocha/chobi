def detect_bug(test_result):

    stderr = test_result.get("stderr", "")

    if "ImportError" in stderr:
        return {"type": "import_error"}

    if "AssertionError" in stderr:
        return {"type": "test_failure"}

    return {
        "type": "unknown",
        "log": stderr
    }