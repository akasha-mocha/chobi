from scripts.services.test_service import run_tests


def execute_tests():

    print("Running tests...")

    result = run_tests()

    if result["success"]:
        print("Tests passed")
    else:
        print("Tests failed")

    return result