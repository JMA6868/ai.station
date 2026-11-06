"""Verified metadata for additional CWRU 12 kHz DE faults.

Recording IDs and experimental conditions are mapped from
the official CWRU 12 kHz Drive End fault data table.

Physical-bearing and defect-instance IDs remain unknown.
"""

CWRU_ADDITIONAL_FAULT_METADATA = {}

GROUPS = {
    0.021: {
        "inner_race": (209, 210, 211, 212),
        "ball": (222, 223, 224, 225),
        "outer_race_6": (234, 235, 236, 237),
        "outer_race_3": (246, 247, 248, 249),
        "outer_race_12": (258, 259, 260, 261),
    },
    0.028: {
        "inner_race": (3001, 3002, 3003, 3004),
        "ball": (3005, 3006, 3007, 3008),
    },
}

for diameter, conditions in GROUPS.items():
    for condition, recording_ids in conditions.items():
        for load_hp, recording_id in enumerate(recording_ids):
            if recording_id in CWRU_ADDITIONAL_FAULT_METADATA:
                raise ValueError(f"Duplicate recording: {recording_id}")

            CWRU_ADDITIONAL_FAULT_METADATA[recording_id] = {
                "label": 1,
                "condition": condition,
                "load_hp": load_hp,
                "fault_diameter_in": diameter,
                "source_rate_hz": 12000,
                "bearing_id": None,
                "defect_instance_id": None,
            }
