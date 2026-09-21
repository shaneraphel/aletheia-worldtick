import numpy as np

def accept(candidate, reference):
    candidate = np.asarray(candidate)
    if np.issubdtype(np.asarray(candidate).dtype, np.integer) or np.issubdtype(
        np.asarray(reference).dtype, np.integer
    ):
        accepted = bool(np.array_equal(candidate, reference))
    else:
        accepted = bool(np.allclose(candidate, reference, rtol=1e-3, atol=1e-3))
    return accepted
