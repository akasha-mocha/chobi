listeners = []


def subscribe(fn):

    listeners.append(fn)


def publish(event):

    for l in listeners:
        try:
            l(event)
        except Exception:
            pass