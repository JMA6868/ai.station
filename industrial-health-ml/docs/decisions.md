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


## Decision 002: Timestamp Continuity

Status: Accepted

### Context
Industrial sensor measurements must preserve
their original temporal relationships.

### Decision
Validate adjacent timestamp intervals using a
configurable expected sampling interval.

Reject windows that contain invalid sensor
measurements or discontinuous timestamps.

Use a small numerical tolerance to account
for floating-point representation errors.

### Rationale
Combining measurements across sampling gaps
can produce misleading statistical features.

### Limitations
- Timestamp validation assumes a fixed sampling rate.
- Sampling jitter is handled using a fixed tolerance.
- Full timestamp quality reporting is not yet implemented.
- Sensor measurement units are not yet standardized.

### Future Work
- Support configurable sampling tolerance.
- Add data quality reports.
- Evaluate timestamp integrity in real datasets.
