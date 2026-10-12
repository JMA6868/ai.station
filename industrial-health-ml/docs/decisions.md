# IndustrialSense AI — Technical Decisions

## Decision 001: Invalid Sensor Readings

Status: Accepted

### Context
Industrial sensor data may contain missing,
non-numeric, or out-of-range measurements.

### Decision
Represent invalid readings as None.

Do not remove invalid readings and concatenate
the surrounding valid measurements.

Skip sliding windows containing invalid readings.

### Rationale
Removing invalid readings can destroy the original
sample positions and create artificial continuity.

### Limitations
The current pipeline does not yet validate
timestamps or sampling intervals.

### Future Work
Implement timestamp validation and data
quality reporting.
