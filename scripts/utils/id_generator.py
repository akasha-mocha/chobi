from datetime import datetime


def generate_id(prefix):

    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    return f"{prefix}-{ts}"