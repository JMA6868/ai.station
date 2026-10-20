# IndustrialSense AI - CWRU Recording Metadata

# Approximate RPM values documented by the CWRU Data Center.
APPROX_RPM_BY_LOAD = {
    0: 1797,
    1: 1772,
    2: 1750,
    3: 1730,
}

# Current eight recordings used in Step 26.
# These values describe the published experimental conditions,
# not verified unique physical bearing identities.

CWRU_RECORDING_METADATA = {
    97:  {"label": 0, "condition": "normal", "load_hp": 0, "fault_diameter_in": None},
    98:  {"label": 0, "condition": "normal", "load_hp": 1, "fault_diameter_in": None},
    99:  {"label": 0, "condition": "normal", "load_hp": 2, "fault_diameter_in": None},
    100: {"label": 0, "condition": "normal", "load_hp": 3, "fault_diameter_in": None},
    105: {"label": 1, "condition": "inner_race", "load_hp": 0, "fault_diameter_in": 0.007},
    106: {"label": 1, "condition": "inner_race", "load_hp": 1, "fault_diameter_in": 0.007},
    107: {"label": 1, "condition": "inner_race", "load_hp": 2, "fault_diameter_in": 0.007},
    108: {"label": 1, "condition": "inner_race", "load_hp": 3, "fault_diameter_in": 0.007},
    118: {"label": 1, "condition": "ball", "load_hp": 0, "fault_diameter_in": 0.007},
    119: {"label": 1, "condition": "ball", "load_hp": 1, "fault_diameter_in": 0.007},
    120: {"label": 1, "condition": "ball", "load_hp": 2, "fault_diameter_in": 0.007},
    121: {"label": 1, "condition": "ball", "load_hp": 3, "fault_diameter_in": 0.007},
    130: {"label": 1, "condition": "outer_race_6", "load_hp": 0, "fault_diameter_in": 0.007},
    131: {"label": 1, "condition": "outer_race_6", "load_hp": 1, "fault_diameter_in": 0.007},
    132: {"label": 1, "condition": "outer_race_6", "load_hp": 2, "fault_diameter_in": 0.007},
    133: {"label": 1, "condition": "outer_race_6", "load_hp": 3, "fault_diameter_in": 0.007},
}

CWRU_METADATA_SOURCE = (
    "https://engineering.case.edu/bearingdatacenter/"
)