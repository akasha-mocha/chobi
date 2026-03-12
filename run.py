import sys

def run_dev():
    from scripts.core.orchestrator.ai_runner import run_ai_dev
    run_ai_dev()

def run_dashboard():
    from dashboard.server import start_dashboard
    start_dashboard()

def run_tests():
    from scripts.services.test_service import run_tests
    result = run_tests()
    print(result)

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("python run.py dev")
        print("python run.py dashboard")
        print("python run.py test")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "dev":
        run_dev()

    elif cmd == "dashboard":
        run_dashboard()

    elif cmd == "test":
        run_tests()

    else:
        print("Unknown command")