"""
config.py
---------
Central configuration for the Carousell S3 -> S3 medallion pipeline.
Update BUCKET and the *_PREFIX values to match your environment.
All paths are S3 URIs so the same code runs on Databricks (with the
S3 bucket mounted / IAM instance profile attached) or via spark-submit
with the hadoop-aws + aws-java-sdk-bundle packages on the cluster.
"""

# ---------------------------------------------------------------------------
# S3 layout
# ---------------------------------------------------------------------------
BUCKET = "destiny-regishealthcare-target"

# RAW_PREFIX     = f"{BUCKET}/raw/orders"          # original source CSVs land here (MySQL/SQLServer/API dumps)
RAW_PREFIX = f"{BUCKET}/raw"
BRONZE_PREFIX  = f"s3://{BUCKET}/Raw data bronze"       # raw data copied 1:1 into Delta, ingestion metadata added
SILVER_PREFIX  = f"{BUCKET}/clean_silver"       # cleaned, standardized, deduplicated, FK-validated
QUARANTINE_PREFIX = f"{BUCKET}/quarantine"  # rows that fail validation, kept for DQ reporting
GOLD_PREFIX    = f"{BUCKET}/gold"         # star-schema dims + facts, ready for Power BI
DQ_METRICS_PATH = f"{BUCKET}/dq_metrics"  # one row per pipeline run per table with pass/fail counts


# ---------------------------------------------------------------------------
# Table -> raw file name mapping (source system CSVs, see project brief)
# ---------------------------------------------------------------------------
RAW_FILES = {

    "admissions": "admissions.csv",

    "appointments": "appointments.csv",

    "billing": "billing.csv",

    "discharges": "discharges.csv",

    "employees": "employees.csv",

    "facilities": "facilities.csv",

    "incidents": "incidents.csv",

    "medications": "medications.csv",

    "resident_feedback": "resident_feedback.csv",

    "residents": "residents.csv",

}
# ---------------------------------------------------------------------------
# # Reference / lookup constants used across cleaning scripts
# # ---------------------------------------------------------------------------
# VALID_ORDER_STATUSES = ["Completed", "Pending", "Cancelled", "Refunded", "Processing", "Shipped"]
# VALID_COUNTRY_CODES = ["SG", "MY", "ID", "HK", "TW", "AU", "PH"]
# VALID_CURRENCIES = ["SGD", "MYR", "IDR", "HKD", "TWD", "AUD", "PHP"]

# ORDER_STATUS_MAP = {
#     "complet": "Completed", "completed": "Completed",
#     "cancelld": "Cancelled", "cancelled": "Cancelled",
#     "in_progress": "Processing", "processing": "Processing",
#     "shipped??": "Shipped", "shipped": "Shipped",
#     "pending": "Pending", "refunded": "Refunded",
# }

# VALID_PAYMENT_STATUSES = ["Success", "Pending", "Failed", "Refunded", "Chargeback"]
# PAYMENT_STATUS_MAP = {
#     "succes": "Success", "success": "Success",
#     "faild": "Failed", "failed": "Failed",
#     "in_review": "Pending", "pending": "Pending",
#     "refunded": "Refunded", "chargeback": "Chargeback",
# }

# VALID_SHIPPING_STATUSES = ["Delivered", "In Transit", "Pending Pickup", "Returned", "Lost", "Cancelled"]
# SHIPPING_STATUS_MAP = {
#     "deliverd": "Delivered", "delivered": "Delivered",
#     "in-transit!!": "In Transit", "in transit": "In Transit",
#     "shipped??": "In Transit",
#     "unknown": "Pending Pickup",
#     "cancelled": "Cancelled", "returned": "Returned", "lost": "Lost",
# }

# NULL_TOKENS = ["", "NULL", "null", "N/A", "n/a", "NA", "UNKNOWN", "unknown", None]

# # Broken/synthetic FK ids are injected in the 900000-999999 range in this dataset;
# # treat anything in that range (or not present in the parent dim) as broken.
# BROKEN_FK_RANGE = (900000, 999999)