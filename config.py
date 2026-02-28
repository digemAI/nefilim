# risk thresholds, values that immediately trigger a "risk" state

RISK_SLEEP_THRESHOLD = 5.0      # sleep hours below this value trigger risk
RISK_STRESS_THRESHOLD = 8       # stress at or above this value triggers risk
RISK_ANXIETY_THRESHOLD = 8      # anxiety at or above this value triggers risk

# warning thresholds, intermediate ranges that trigger a "warning" state

WARNING_SLEEP_MIN = 5.0         # lower bound for warning sleep range
WARNING_SLEEP_MAX = 6.5         # upper bound for warning sleep range

WARNING_STRESS_MIN = 6          # lower bound for warning stress range
WARNING_STRESS_MAX = 7          # upper bound for warning stress range

WARNING_ANXIETY_MIN = 6         # lower bound for warning anxiety range
WARNING_ANXIETY_MAX = 7         # upper bound for warning anxiety range


# storage configuration, path where check-in history is persisted

HISTORY_FILE_PATH = "data/nefilim_history.json"