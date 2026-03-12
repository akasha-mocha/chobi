from scripts.core.engine.self_improving_dev_loop import run_self_improving_loop


def run_dev_cycle(task):

    print("Starting dev cycle")

    success = run_self_improving_loop(task)

    if success:
        print("Dev cycle completed")

    else:
        print("Dev cycle failed")