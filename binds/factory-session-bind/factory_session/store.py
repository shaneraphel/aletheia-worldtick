TASKS: dict[str, list] = {}

def enqueue(job, worker_id=None):
    if not worker_id:
        raise ValueError("factory job requires a worker id")
    TASKS.setdefault(worker_id, []).append(job)
