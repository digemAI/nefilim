# Valid ranges for the validation stage
METRIC_RANGES = {
    "sleep_hours": (0, 24),
    "mood": (0, 10),
    "anxiety": (0, 10),
    "energy": (0, 10),
    "focus": (0, 10),
}

# Fields required to build a valid NEFILIM record
REQUIRED_FIELDS = [
    "sleep_hours",
    "mood",
    "anxiety",
    "energy",
    "focus",
    "notes",
]

# Risk triggers for the current state
RISK_ANXIETY_THRESHOLD = 8
RISK_FOCUS_THRESHOLD = 3
RISK_SLEEP_THRESHOLD = 4.0
RISK_ENERGY_THRESHOLD = 3
RISK_MOOD_THRESHOLD = 2

# Warning limits for the current state
WARNING_SLEEP_THRESHOLD = 6.0
WARNING_ANXIETY_THRESHOLD = 6
WARNING_ENERGY_THRESHOLD = 4
WARNING_FOCUS_THRESHOLD = 4
WARNING_MOOD_THRESHOLD = 4

# V2 settings for history and trend analysis
RECENT_HISTORY_LIMIT = 7
TREND_WINDOW = 3
WARNING_STREAK_LIMIT = 3
RISK_STREAK_LIMIT = 2
HIGH_WARNING_RATIO = 0.6
HIGH_RISK_RATIO = 0.34
WORSENING_DELTA = 1.0
IMPROVING_DELTA = 1.0

# Storage and logging paths
HISTORY_FILE_PATH = "data/nefilim_history.json"
DEFAULT_STORAGE_PATH = HISTORY_FILE_PATH
DEFAULT_LOG_PATH = "data/nefilim.log"