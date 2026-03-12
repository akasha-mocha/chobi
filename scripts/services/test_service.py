import subprocess
import os


def run_tests():
    """
    pytest を実行
    """

    try:
        result = subprocess.run(
            ["pytest", "tests"],
            capture_output=True,
            text=True
        )

        success = result.returncode == 0

        return {
            "success": success,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def run_single_test(test_name):
    try:
        result = subprocess.run(
            ["pytest", test_name],
            capture_output=True,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }