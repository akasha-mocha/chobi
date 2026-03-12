import os
import yaml
import json
from pathlib import Path

from scripts.ai.ai_interface import call_ai


PROMPT_ROOT = ".antigravity/prompts"


class WorkflowEngine:

    def __init__(self, project_root="."):
        self.project_root = Path(project_root)

    def run_workflow(self, workflow_path):

        workflow_path = Path(workflow_path)

        with open(workflow_path, "r", encoding="utf-8") as f:
            workflow = yaml.safe_load(f)

        print(f"Running workflow: {workflow['name']}")

        steps = workflow.get("steps", [])

        context = {}

        for step in steps:

            print(f"Step: {step.get('name') or step.get('id')}")

            if "prompt" in step:
                self._run_prompt_step(step, context)

            elif "script" in step:
                self._run_script_step(step, context)

            else:
                raise Exception("Unknown step type")

    # --------------------------------------------------

    def _run_prompt_step(self, step, context):

        prompt_path = self._resolve_prompt(step["prompt"])

        prompt = self._load_prompt(prompt_path)

        inputs = self._load_inputs(step.get("input", []))

        full_prompt = self._compose_prompt(prompt, inputs)

        response = call_ai(full_prompt)

        output = step.get("output")

        if output:
            self._write_output(output, response)

    # --------------------------------------------------

    def _run_script_step(self, step, context):

        script_path = step["script"]

        print(f"Running script: {script_path}")

        namespace = {}

        with open(script_path, "r", encoding="utf-8") as f:
            code = f.read()

        exec(code, namespace)

    # --------------------------------------------------

    def _resolve_prompt(self, prompt_path):

        if prompt_path.startswith(".antigravity"):
            return prompt_path

        return os.path.join(PROMPT_ROOT, prompt_path)

    # --------------------------------------------------

    def _load_prompt(self, path):

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    # --------------------------------------------------

    def _load_inputs(self, inputs):

        collected = {}

        for path in inputs:

            if os.path.exists(path):

                with open(path, "r", encoding="utf-8") as f:

                    if path.endswith(".json"):
                        collected[path] = json.load(f)
                    else:
                        collected[path] = f.read()

        return collected

    # --------------------------------------------------

    def _compose_prompt(self, prompt, inputs):

        block = ""

        for name, value in inputs.items():

            block += f"\n\nINPUT FILE: {name}\n"

            if isinstance(value, dict) or isinstance(value, list):
                block += json.dumps(value, indent=2)
            else:
                block += str(value)

        return prompt + "\n\n" + block

    # --------------------------------------------------

    def _write_output(self, output_path, data):

        output_path = Path(output_path)

        if output_path.suffix == "":
            output_path.mkdir(parents=True, exist_ok=True)
            return

        output_path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(data, dict) or isinstance(data, list):

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

        else:

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(str(data))

        print(f"Output written: {output_path}")