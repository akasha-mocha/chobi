import yaml


def load_spec(path="docs/spec.yaml"):

    with open(path, "r", encoding="utf-8") as f:

        return yaml.safe_load(f)


def get_modules():

    spec = load_spec()

    return spec.get("modules", [])