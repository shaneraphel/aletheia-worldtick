import time

MEMORY: dict[str, list] = {}

def remember(text, session_id=None):
    if not session_id:
        raise ValueError("memory write requires a session id")
    MEMORY.setdefault(session_id, []).append({"text": text, "ts": time.time()})
