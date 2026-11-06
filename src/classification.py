# Simple RMS threshold classifier

def predict_fault(rms, threshold):
    """Return 1 for fault and 0 for normal."""
    if rms > threshold:
        return 1
    return 0