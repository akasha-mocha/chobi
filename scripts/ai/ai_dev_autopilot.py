import yaml
import subprocess
import traceback
from pathlib import Path

from scripts.core.workflow.workflow_engine import WorkflowEngine
from scripts.core.dev_state_manager import DevStateManager


class AIDevAutopilot:

    def __init__(self, config_path=".antigravity/autopilot/dev_loop.yaml"):

        self.config_path = Path(config_path)

        if not self.config_path.exists():
            raise FileNotFoundError(f"Autopilot config not found: {config_path}")

        self.engine = WorkflowEngine()
        self.state = DevStateManager()

        self.config = self._load_config()

        self.tests_passed = False

    # --------------------------------
    # load yaml
    # --------------------------------

    def _load_config(self):

        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    # --------------------------------
    # run autopilot
    # --------------------------------

    def run(self):

        print("\n==============================")
        print("AI DEV AUTOPILOT START")
        print("==============================\n")

        cycle = self.state.next_cycle()

        print(f"DEV CYCLE: {cycle}\n")

        steps = self.config.get("steps", [])

        for step in steps:

            if step.get("loop"):

                self._run_loop(step)

            else:

                self._execute_step(step)

        print("\n==============================")
        print("AI DEV AUTOPILOT FINISHED")
        print("==============================\n")

    # --------------------------------
    # loop execution
    # --------------------------------

    def _run_loop(self, step):

        max_cycles = step.get("max_cycles", 10)

        print(f"\nEntering dev loop (max {max_cycles})")

        for i in range(max_cycles):

            print(f"\n===== DEV LOOP {i+1} =====")

            for s in step.get("steps", []):

                self._execute_step(s)

                if self.tests_passed:

                    print("\n✔ Tests passed. Development complete.")
                    return

        print("\nMax dev cycles reached.")

    # --------------------------------
    # step execution
    # --------------------------------

    def _execute_step(self, step):

        name = step.get("name", "unknown")

        print(f"\n--- STEP: {name} ---")

        try:

            if "workflow" in step:

                self._run_workflow(step["workflow"])

            elif "script" in step:

                self._run_script(step["script"], name)

            elif "steps" in step:

                for s in step["steps"]:
                    self._execute_step(s)

        except Exception as e:

            print(f"STEP FAILED: {name}")
            print(e)
            traceback.print_exc()

    # --------------------------------
    # workflow
    # --------------------------------

    def _run_workflow(self, workflow_path):

        path = Path(workflow_path)

        if not path.exists():
            raise FileNotFoundError(f"Workflow not found: {workflow_path}")

        print(f"Running workflow: {workflow_path}")

        self.engine.run_workflow(workflow_path)

    # --------------------------------
    # script
    # --------------------------------

    def _run_script(self, script_path, step_name):

        path = Path(script_path)

        if not path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")

        print(f"Running script: {script_path}")

        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True
        )

        print(result.stdout)

        if result.returncode != 0:

            print("SCRIPT ERROR:")
            print(result.stderr)

            raise RuntimeError("Script execution failed")

        # test success detection

        if step_name == "run_tests":

            if "FAILED" not in result.stdout and "ERROR" not in result.stdout:

                self.tests_passed = True

    # --------------------------------
    # entry
    # --------------------------------


def main():

    autopilot = AIDevAutopilot()

    autopilot.run()


if __name__ == "__main__":
    main()