"""Open leftover dest: tools fire on a finalized user turn."""

inflight = {}


class tools:
    @staticmethod
    def dispatch(text):
        return {"text": text}

    @staticmethod
    def cancel(handle):
        return handle


def handle(event):
    if event.get("type") == "session.ready":
        return "ready"
    if event.get("type") == "transcript.user":
        handle = tools.dispatch(event.get("text") or "")
        inflight["tool"] = handle
        return "dispatched"
    if event.get("type") == "reply.done" and event.get("status") == "interrupted":
        tools.cancel(inflight.pop("tool", None))
        return "cancelled"
    return "ignored"
