# Immediate "risk" triggers
RISK_SLEEP_THRESHOLD = 5.0      # Sleep below this value = risk
RISK_STRESS_THRESHOLD = 8       # Stress below this value = risk
RISK_ANXIETY_THRESHOLD = 8      # Anxiety below this value = risk

# Warning limits: values between stable and risk

WARNING_SLEEP_MIN = 5.0         # Warning sleep lower bound
WARNING_SLEEP_MAX = 6.5         # Warning sleep upper bound

WARNING_STRESS_MIN = 6          # Warning stress lower bound
WARNING_STRESS_MAX = 7          # Warning stress upper bound

WARNING_ANXIETY_MIN = 6         # Warning anxiety lower bound
WARNING_ANXIETY_MAX = 7         # Warning anxiety upper bound

# History file path

HISTORY_FILE_PATH = "data/nefilim_history.json"
DEFAULT_STORAGE_PATH = HISTORY_FILE_PATH  

DEFAULT_LOG_PATH = "data/nefilim.log"

# Fields required to build a valid NEFILIM record
REQUIRED_FIELDS = [
    "sleep_hours",
    "mood",
    "anxiety",
    "energy",
    "focus",
    "notes",
]

# Valid ranges for the data sent to the detector
METRIC_RANGES = {
    "sleep_hours": (0, 24),
    "mood": (0, 10),
    "anxiety": (0, 10),
    "energy": (0, 10),
    "focus": (0, 10),
}