import streamlit as st
import pandas as pd
import io
import json

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Data Schema Validator",
    page_icon="💊",
    layout="wide"
)

st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    [data-testid="stMetricValue"] { font-size: 1.6rem; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# BUILT-IN SCHEMAS  (all 9 masters from DB schema)
# =========================================================

BUILTIN_SCHEMAS = {

    # ── 1. Brand Master ──────────────────────────────────
    "Brand Master": {
        "columns": {
            "name":            {"type": "varchar",   "max_length": 20,  "nullable": False, "unique": False, "case_insensitive_unique": True},
            "short-name":      {"type": "varchar",   "max_length": 10,  "nullable": False,  "unique": True, "case_insensitive_unique": True},
            "remark":          {"type": "varchar",   "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "logo-image":      {"type": "varchar",   "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "is-active":       {"type": "int",                          "nullable": False, "unique": False, "case_insensitive_unique": False},
            "inactive-reason": {"type": "varchar",   "max_length": 45,  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "is-validated":    {"type": "int",                          "nullable": False,  "unique": False, "case_insensitive_unique": False},
            "created-by":      {"type": "varchar",   "max_length": 255, "nullable": False, "unique": False, "case_insensitive_unique": False},
            "updated-by":      {"type": "varchar",   "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "created-at":      {"type": "timestamp",                    "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "updated-at":      {"type": "timestamp",                    "nullable": True,  "unique": False, "case_insensitive_unique": False},
        }
    },

    # ── 2. Companies ─────────────────────────────────────
    "Companies": {
        "columns": {
            "name":            {"type": "varchar",   "max_length": 128, "nullable": False, "unique": False, "case_insensitive_unique": False},
            "type":            {"type": "enum",      "allowed_values": ["manufacturer", "marketer", "both"],
                                                     "nullable": False, "unique": False, "case_insensitive_unique": False},
            "grade":           {"type": "varchar",   "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "category":        {"type": "varchar",   "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "certifications":  {"type": "varchar",   "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "short-name":      {"type": "varchar",   "max_length": 12,  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "remark":          {"type": "varchar",   "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "address-1":       {"type": "varchar",   "max_length": 25,  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "address-2":       {"type": "varchar",   "max_length": 25,  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "address-3":       {"type": "varchar",   "max_length": 25,  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "city-id":         {"type": "int",                          "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "state-id":        {"type": "int",                          "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "pincode":         {"type": "int",                          "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "inactive-reason": {"type": "varchar",   "max_length": 45,  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "is-validated":    {"type": "int",                          "nullable": False,  "unique": False, "case_insensitive_unique": False},
            "is-active":       {"type": "int",                          "nullable": False, "unique": False, "case_insensitive_unique": False},
            "created-at":      {"type": "timestamp",                    "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "created-by":      {"type": "varchar",   "max_length": 255, "nullable": False, "unique": False, "case_insensitive_unique": False},
            "updated-at":      {"type": "timestamp",                    "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "updated-by":      {"type": "varchar",   "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
        }
    },

    # ── 3. Product Master ────────────────────────────────
    "Product Master": {
        "columns": {
            "name":                    {"type": "varchar", "max_length": 255, "nullable": False, "unique": True, "case_insensitive_unique": True},
            "product-category-id":     {"type": "int",                        "nullable": False,  "unique": False, "case_insensitive_unique": False},
            "short-name":              {"type": "varchar", "max_length": 50,  "nullable": False,  "unique": True, "case_insensitive_unique": True},
            "remark":                  {"type": "varchar", "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "is-validated":            {"type": "int",                        "nullable": False,  "unique": False, "case_insensitive_unique": False},
            "is-active":               {"type": "int",                        "nullable": False, "unique": False, "case_insensitive_unique": False},
            "inactive-reason":         {"type": "varchar", "max_length": 45,  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "created-by":              {"type": "varchar", "max_length": 255, "nullable": False, "unique": False, "case_insensitive_unique": False},
            "updated-by":              {"type": "varchar", "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "created-at":              {"type": "timestamp",                  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "updated-at":              {"type": "timestamp",                  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "product-sub-category-id": {"type": "int",                        "nullable": True,  "unique": False, "case_insensitive_unique": False},
        }
    },

    # ── 4. Product Sub-Category ──────────────────────────
    "Product Sub-Category": {
        "columns": {
            "name":                {"type": "varchar", "max_length": 255, "nullable": False, "unique": False, "case_insensitive_unique": False},
            "product-category-id": {"type": "int",                        "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "short-name":          {"type": "varchar", "max_length": 50,  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "remark":              {"type": "varchar", "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "is-validated":        {"type": "int",                        "nullable": False,  "unique": False, "case_insensitive_unique": False},
            "is-active":           {"type": "int",                        "nullable": False, "unique": False, "case_insensitive_unique": False},
            "inactive-reason":     {"type": "varchar", "max_length": 45,  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "created-by":          {"type": "varchar", "max_length": 255, "nullable": False, "unique": False, "case_insensitive_unique": False},
            "updated-by":          {"type": "varchar", "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "created-at":          {"type": "timestamp",                  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "updated-at":          {"type": "timestamp",                  "nullable": True,  "unique": False, "case_insensitive_unique": False},
        }
    },

    # ── 5. Use Master ────────────────────────────────────
    "Use Master": {
        "columns": {
            "name":               {"type": "varchar", "max_length": 255,  "nullable": False, "unique": True, "case_insensitive_unique": True},
            "short-description":  {"type": "varchar", "max_length": 255,  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "long-description":   {"type": "varchar", "max_length": 1000, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "course-duration":    {"type": "varchar", "max_length": 255,  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "remark":             {"type": "varchar", "max_length": 255,  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "is-validated":       {"type": "int",                         "nullable": False,  "unique": False, "case_insensitive_unique": False},
            "is-active":          {"type": "int",                         "nullable": False, "unique": False, "case_insensitive_unique": False},
            "inactive-reason":    {"type": "varchar", "max_length": 45,   "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "created-by":         {"type": "varchar", "max_length": 255,  "nullable": False, "unique": False, "case_insensitive_unique": False},
            "created-at":         {"type": "timestamp",                   "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "updated-by":         {"type": "varchar", "max_length": 255,  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "updated-at":         {"type": "timestamp",                   "nullable": True,  "unique": False, "case_insensitive_unique": False},
        }
    },

    # ── 6. Drug Use Mapping ──────────────────────────────
    "Drug Use Mapping": {
        "columns": {
            "drug-id":        {"type": "int",                         "nullable": False, "unique": False, "case_insensitive_unique": False},
            "use-master-id":  {"type": "int",                         "nullable": False, "unique": False, "case_insensitive_unique": False},
            "ranking":        {"type": "varchar", "max_length": 45,   "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "is-active":      {"type": "int",                         "nullable": False, "unique": False, "case_insensitive_unique": False},
            "created-by":     {"type": "varchar", "max_length": 255,  "nullable": False, "unique": False, "case_insensitive_unique": False},
            "updated-by":     {"type": "varchar", "max_length": 255,  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "created-at":     {"type": "timestamp",                   "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "updated-at":     {"type": "timestamp",                   "nullable": True,  "unique": False, "case_insensitive_unique": False},
        }
    },

    # ── 7. Drug Variant Mapping ──────────────────────────
    "Drug Variant Mapping": {
        "columns": {
            "drug-id":           {"type": "int",                        "nullable": False, "unique": False, "case_insensitive_unique": False},
            "variant-master-id": {"type": "int",                        "nullable": False, "unique": False, "case_insensitive_unique": False},
            "custom-value":      {"type": "varchar", "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "is-active":         {"type": "int",                        "nullable": False, "unique": False, "case_insensitive_unique": False},
            "created-by":        {"type": "varchar", "max_length": 255, "nullable": False, "unique": False, "case_insensitive_unique": False},
            "updated-by":        {"type": "varchar", "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "created-at":        {"type": "timestamp",                  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "updated-at":        {"type": "timestamp",                  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "updated-at":        {"type": "timestamp",                  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "ranking":           {"type":"int",                         "nullable":True,   "unique":False,  "case_insensitive_unique": False},
        }
    },

    # ── 8. Variant Master ────────────────────────────────
    "Variant Master": {
        "columns": {
            "name":            {"type": "varchar", "max_length": 255, "nullable": False, "unique": True, "case_insensitive_unique": True},
            "type":            {"type": "enum",    "allowed_values": ["master", "custom"],
                                                   "nullable": False, "unique": False, "case_insensitive_unique": False},
            "inactive-reason": {"type": "varchar", "max_length": 45,  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "remark":          {"type": "varchar", "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "is-validated":    {"type": "int",                        "nullable": False,  "unique": False, "case_insensitive_unique": False},
            "is-active":       {"type": "int",                        "nullable": False, "unique": False, "case_insensitive_unique": False},
            "created-by":      {"type": "varchar", "max_length": 255, "nullable": False, "unique": False, "case_insensitive_unique": False},
            "updated-by":      {"type": "varchar", "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "created-at":      {"type": "timestamp",                  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "updated-at":      {"type": "timestamp",                  "nullable": True,  "unique": False, "case_insensitive_unique": False},
        }
    },

    # ── 9. Variant Values Master ─────────────────────────
    "Variant Values Master": {
        "columns": {
            "name":              {"type": "varchar", "max_length": 255, "nullable": False, "unique": False, "case_insensitive_unique": False},
            "variant-master-id": {"type": "int",                        "nullable": False, "unique": False, "case_insensitive_unique": False},
            "short-name":        {"type": "varchar", "max_length": 50,  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "is-active":         {"type": "int",                        "nullable": False, "unique": False, "case_insensitive_unique": False},
            "created-by":        {"type": "varchar", "max_length": 255, "nullable": False, "unique": False, "case_insensitive_unique": False},
            "updated-by":        {"type": "varchar", "max_length": 255, "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "created-at":        {"type": "timestamp",                  "nullable": True,  "unique": False, "case_insensitive_unique": False},
            "updated-at":        {"type": "timestamp",                  "nullable": True,  "unique": False, "case_insensitive_unique": False},
        }
    },

}

# =========================================================
# SCHEMA PERSISTENCE
# =========================================================

SCHEMA_FILE = "saved_schemas.json"

def load_saved_schemas():
    try:
        with open(SCHEMA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_schemas_to_file(schemas):
    try:
        with open(SCHEMA_FILE, "w") as f:
            json.dump(schemas, f, indent=2)
        return True
    except Exception:
        return False

def get_all_schemas():
    return {**BUILTIN_SCHEMAS, **load_saved_schemas()}

# =========================================================
# VALIDATION HELPERS
# =========================================================

def check_varchar(series, max_length):
    type_ok   = series.apply(lambda x: pd.isna(x) or isinstance(x, str))
    length_ok = series.apply(lambda x: pd.isna(x) or len(str(x)) <= max_length)
    return type_ok, length_ok

def check_int(series):
    return series.apply(lambda x: pd.isna(x) or str(x).strip().lstrip('-').isdigit())

def check_timestamp(series):
    return pd.to_datetime(series, errors='coerce').notna() | series.isna()

def check_boolean(series):
    allowed = {'0', '1', 'yes', 'no', 'true', 'false'}
    return series.apply(lambda x: pd.isna(x) or str(x).strip().lower() in allowed)

def check_enum(series, allowed_values):
    allowed_lower = [str(v).strip().lower() for v in allowed_values]
    return series.apply(lambda x: pd.isna(x) or str(x).strip().lower() in allowed_lower)

def check_fk(series, reference_values):
    ref_lower = [str(v).strip().lower() for v in reference_values]
    return series.apply(lambda x: pd.isna(x) or str(x).strip().lower() in ref_lower)

def check_non_nullable(series):
    return series.notna() & (series.astype(str).str.strip() != '')

def check_unique_ci(series):
    return ~series.astype(str).str.strip().str.lower().duplicated(keep=False)

def check_unique_cs(series):
    return ~series.duplicated(keep=False)

# =========================================================
# CORE VALIDATION ENGINE
# =========================================================

def run_validation(df, schema_def, upload_mode="create"):
    errors = []
    columns = schema_def.get("columns", {})

    # ── ID column rules based on upload mode ──────────────
    if "id" in df.columns:
        if upload_mode == "update":
            # id must be present, non-null, integer, and unique
            id_series = df["id"]
            # Not null
            null_mask = id_series.isna() | (id_series.astype(str).str.strip() == "")
            for idx in df[null_mask].index:
                errors.append({"Column": "id", "Issue": "NULL_OR_BLANK",
                    "Row": idx + 2, "Value": str(df.at[idx, "id"]),
                    "Details": "id is required and cannot be empty in Update mode"})
            # Must be integer
            valid_int = id_series.apply(lambda x: pd.isna(x) or str(x).strip().lstrip('-').isdigit())
            for idx in df[~valid_int].index:
                errors.append({"Column": "id", "Issue": "INVALID_DATA_TYPE",
                    "Row": idx + 2, "Value": str(df.at[idx, "id"])[:60],
                    "Details": "id must be an integer in Update mode"})
            # Must be unique
            dup_mask = id_series.duplicated(keep=False)
            for idx in df[dup_mask & ~null_mask].index:
                errors.append({"Column": "id", "Issue": "DUPLICATE_VALUE",
                    "Row": idx + 2, "Value": str(df.at[idx, "id"])[:60],
                    "Details": "Duplicate id found — each row must have a unique id in Update mode"})
        # In create mode: id column present is fine, skip all id checks (auto-generated by DB)
    else:
        if upload_mode == "update":
            errors.append({"Column": "id", "Issue": "COLUMN_NOT_FOUND",
                "Row": "-", "Value": "-",
                "Details": "id column is mandatory for Update mode — add it with the existing record IDs"})

    for col_name, rules in columns.items():

        # id is handled separately above based on upload_mode
        if col_name == "id":
            continue

        if col_name not in df.columns:
            errors.append({"Column": col_name, "Issue": "COLUMN_NOT_FOUND",
                "Row": "-", "Value": "-", "Details": "Column missing from uploaded file"})
            continue

        series   = df[col_name]
        col_type = rules.get("type", "varchar")

        if col_type == "varchar":
            max_len = rules.get("max_length", 255)
            type_ok, length_ok = check_varchar(series, max_len)
            for idx in df[~type_ok].index:
                errors.append({"Column": col_name, "Issue": "INVALID_DATA_TYPE",
                    "Row": idx + 2, "Value": str(df.at[idx, col_name])[:60],
                    "Details": "Expected text/string value"})
            for idx in df[~length_ok].index:
                val = str(df.at[idx, col_name])
                errors.append({"Column": col_name, "Issue": "VARCHAR_LENGTH_EXCEEDED",
                    "Row": idx + 2, "Value": val[:60],
                    "Details": f"Max {max_len} chars | Actual: {len(val)} chars"})

        elif col_type == "int":
            valid = check_int(series)
            for idx in df[~valid].index:
                errors.append({"Column": col_name, "Issue": "INVALID_DATA_TYPE",
                    "Row": idx + 2, "Value": str(df.at[idx, col_name])[:60],
                    "Details": "Expected integer value"})

        elif col_type == "timestamp":
            valid = check_timestamp(series)
            for idx in df[~valid].index:
                errors.append({"Column": col_name, "Issue": "INVALID_DATA_TYPE",
                    "Row": idx + 2, "Value": str(df.at[idx, col_name])[:60],
                    "Details": "Expected date/timestamp value"})

        elif col_type == "boolean":
            valid = check_boolean(series)
            for idx in df[~valid].index:
                errors.append({"Column": col_name, "Issue": "INVALID_BOOLEAN",
                    "Row": idx + 2, "Value": str(df.at[idx, col_name])[:60],
                    "Details": "Allowed: 0, 1, yes, no, true, false"})

        elif col_type == "enum":
            allowed = rules.get("allowed_values", [])
            valid   = check_enum(series, allowed)
            for idx in df[~valid].index:
                errors.append({"Column": col_name, "Issue": "INVALID_ENUM_VALUE",
                    "Row": idx + 2, "Value": str(df.at[idx, col_name])[:60],
                    "Details": f"Allowed values: {', '.join(str(v) for v in allowed)}"})

        elif col_type == "foreign_key":
            ref_vals = rules.get("reference_values", [])
            if ref_vals:
                valid = check_fk(series, ref_vals)
                for idx in df[~valid].index:
                    errors.append({"Column": col_name, "Issue": "INVALID_FOREIGN_KEY",
                        "Row": idx + 2, "Value": str(df.at[idx, col_name])[:60],
                        "Details": f"Value not found in reference list ({len(ref_vals)} entries)"})

        if not rules.get("nullable", True):
            valid = check_non_nullable(series)
            for idx in df[~valid].index:
                errors.append({"Column": col_name, "Issue": "NULL_OR_BLANK",
                    "Row": idx + 2, "Value": str(df.at[idx, col_name]),
                    "Details": "This column cannot be empty"})

        if rules.get("unique", False):
            valid = check_unique_cs(series)
            for idx in df[~valid].index:
                errors.append({"Column": col_name, "Issue": "DUPLICATE_VALUE",
                    "Row": idx + 2, "Value": str(df.at[idx, col_name])[:60],
                    "Details": "Duplicate value (case-sensitive)"})

        if rules.get("case_insensitive_unique", False):
            valid = check_unique_ci(series)
            for idx in df[~valid].index:
                errors.append({"Column": col_name, "Issue": "CASE_INSENSITIVE_DUPLICATE",
                    "Row": idx + 2, "Value": str(df.at[idx, col_name])[:60],
                    "Details": 'Duplicate when ignoring case (e.g. "ORG" vs "org")'})

    return pd.DataFrame(errors) if errors else pd.DataFrame(
        columns=["Column", "Issue", "Row", "Value", "Details"])

# =========================================================
# ISSUE ICONS
# =========================================================

ISSUE_ICON = {
    "COLUMN_NOT_FOUND":           "🔴",
    "INVALID_DATA_TYPE":          "🟠",
    "VARCHAR_LENGTH_EXCEEDED":    "🟡",
    "NULL_OR_BLANK":              "🔴",
    "DUPLICATE_VALUE":            "🟠",
    "CASE_INSENSITIVE_DUPLICATE": "🟡",
    "INVALID_ENUM_VALUE":         "🟠",
    "INVALID_FOREIGN_KEY":        "🟠",
    "INVALID_BOOLEAN":            "🟡",
}

# Master grouping for sidebar display
MASTER_GROUPS = {
    "💊 Drug & Product": ["Product Master", "Product Sub-Category", "Use Master",
                          "Drug Use Mapping", "Drug Variant Mapping"],
    "🏭 Company & Brand": ["Brand Master", "Companies"],
    "🔬 Variant": ["Variant Master", "Variant Values Master"],
}

# =========================================================
# TABS
# =========================================================

tab_validate, tab_manage = st.tabs(["🔍  Validate CSV", "⚙️  Schema Manager"])

# ─────────────────────────────────────────────────────────
# TAB 1 — VALIDATE
# ─────────────────────────────────────────────────────────

with tab_validate:
    st.title("💊 Pharma Data Validator")
    st.caption("Upload a bulk-upload CSV and validate it against your master schema before processing.")

    all_schemas = get_all_schemas()

    if not all_schemas:
        st.warning("No schemas defined yet. Go to the Schema Manager tab to create one.")
        st.stop()

    # ── Upload Mode Toggle ────────────────────────────────
    st.markdown("#### Upload Mode")
    mode_col1, mode_col2 = st.columns([2, 5])
    with mode_col1:
        upload_mode = st.radio(
            "Upload mode",
            options=["➕ Create New", "✏️ Update Existing"],
            horizontal=True,
            label_visibility="collapsed"
        )
    upload_mode_key = "create" if upload_mode == "➕ Create New" else "update"

    with mode_col2:
        if upload_mode_key == "create":
            st.info("**Create mode** — `id` column not required. New records will get IDs assigned by the database.")
        else:
            st.warning("**Update mode** — `id` column is **mandatory**, must be a non-null unique integer matching an existing record.")

    st.divider()

    left, right = st.columns([1, 2])

    with left:
        st.subheader("1 · Select master")

        # Group selector
        group_options = list(MASTER_GROUPS.keys()) + ["📂 All Masters"]
        selected_group = st.radio("Filter by group", group_options, index=len(group_options) - 1,
                                  label_visibility="collapsed")

        if selected_group == "📂 All Masters":
            schema_options = list(all_schemas.keys())
        else:
            group_masters = MASTER_GROUPS.get(selected_group, [])
            schema_options = [s for s in group_masters if s in all_schemas]
            # Also include any user-saved schemas
            schema_options += [s for s in all_schemas if s not in BUILTIN_SCHEMAS and s not in schema_options]

        schema_name = st.selectbox("Master", options=schema_options, label_visibility="collapsed")
        schema_def  = all_schemas[schema_name]
        columns_def = schema_def.get("columns", {})

        with st.expander("📋 View expected columns"):
            preview_rows = []
            for cname, crules in columns_def.items():
                t     = crules.get("type", "varchar")
                extra = ""
                if t == "varchar":
                    extra = f"max {crules.get('max_length', 255)} chars"
                elif t == "enum":
                    vals  = crules.get("allowed_values", [])
                    extra = ", ".join(str(v) for v in vals[:5])
                    if len(vals) > 5:
                        extra += f" +{len(vals)-5} more"
                elif t == "foreign_key":
                    extra = f"{len(crules.get('reference_values', []))} reference values"
                elif t == "boolean":
                    extra = "0/1/yes/no/true/false"
                preview_rows.append({
                    "Column":   cname,
                    "Type":     t,
                    "Extra":    extra,
                    "Nullable": "✅ Yes" if crules.get("nullable", True) else "❌ No",
                    "Unique":   "✅" if crules.get("unique") or crules.get("case_insensitive_unique") else "—",
                })
            st.dataframe(pd.DataFrame(preview_rows), hide_index=True, use_container_width=True)

    with right:
        st.subheader("2 · Upload your CSV file")
        uploaded = st.file_uploader("Drop your CSV here", type=["csv"], label_visibility="collapsed")

    st.divider()

    if uploaded:
        try:
            df = pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"Could not read file: {e}")
            st.stop()

        st.subheader(f"3 · Results  {'(Create Mode)' if upload_mode_key == 'create' else '(Update Mode)'}")
        with st.spinner("Running validation..."):
            errors_df = run_validation(df, schema_def, upload_mode=upload_mode_key)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total rows",      len(df))
        m2.metric("Errors found",    len(errors_df))
        m3.metric("Columns checked", len(columns_def))
        m4.metric("Status", "✅  PASSED" if len(errors_df) == 0 else "❌  FAILED")

        st.divider()

        if len(errors_df) == 0:
            st.success("🎉 No errors found! Your file is ready for bulk upload.")
        else:
            st.error(f"Found **{len(errors_df)} error(s)**. Please fix them before uploading.")

            st.subheader("Issue summary")
            summary = errors_df["Issue"].value_counts().reset_index()
            summary.columns = ["Issue", "Count"]
            summary.insert(0, " ", summary["Issue"].map(lambda x: ISSUE_ICON.get(x, "⚪")))
            st.dataframe(summary, hide_index=True, use_container_width=True)

            st.subheader("Detailed error list")
            fc1, fc2 = st.columns(2)
            with fc1:
                f_issue = st.multiselect("Filter by issue type",
                    options=errors_df["Issue"].unique().tolist(),
                    default=errors_df["Issue"].unique().tolist())
            with fc2:
                f_col = st.multiselect("Filter by column",
                    options=errors_df["Column"].unique().tolist(),
                    default=errors_df["Column"].unique().tolist())

            filtered = errors_df[
                errors_df["Issue"].isin(f_issue) &
                errors_df["Column"].isin(f_col)
            ]
            st.dataframe(filtered, hide_index=True, use_container_width=True, height=380)

            buf = io.StringIO()
            filtered.to_csv(buf, index=False)
            st.download_button(
                "⬇️ Download error report (CSV)",
                data=buf.getvalue(),
                file_name=f"{schema_name.replace(' ', '_')}_errors.csv",
                mime="text/csv"
            )
    else:
        st.info("👆 Upload a CSV file above to start validation.")

# ─────────────────────────────────────────────────────────
# TAB 2 — SCHEMA MANAGER
# ─────────────────────────────────────────────────────────

with tab_manage:
    st.title("Schema Manager")
    st.caption("Create, view, import, and export schemas — no code editing required.")

    saved_schemas = load_saved_schemas()

    mgr_l, mgr_r = st.columns([1, 1])

    with mgr_l:
        st.subheader("All schemas")
        all_s = get_all_schemas()

        if all_s:
            for sname, sdef in all_s.items():
                is_builtin = sname in BUILTIN_SCHEMAS
                label      = f"{'🔒 ' if is_builtin else ''}{sname}  —  {len(sdef.get('columns', {}))} columns"
                with st.expander(label):
                    for cname, crules in sdef.get("columns", {}).items():
                        t      = crules.get("type", "varchar")
                        req    = "required" if not crules.get("nullable", True) else "nullable"
                        detail = ""
                        if t == "varchar":
                            detail = f", max {crules.get('max_length', 255)}"
                        elif t == "enum":
                            vals   = crules.get("allowed_values", [])
                            detail = f": {', '.join(str(v) for v in vals)}"
                        elif t == "foreign_key":
                            detail = f", {len(crules.get('reference_values', []))} ref values"
                        st.markdown(f"- **{cname}** `{t}`{detail} · {req}")

                    if not is_builtin:
                        if st.button(f"🗑️ Delete '{sname}'", key=f"del_{sname}"):
                            del saved_schemas[sname]
                            save_schemas_to_file(saved_schemas)
                            st.success(f"Deleted '{sname}'")
                            st.rerun()
        else:
            st.info("No schemas yet.")

        st.divider()
        st.markdown("**Export all schemas**")
        st.caption("Download a JSON backup or share schemas with another instance.")
        export_blob = json.dumps(
            {n: {"schema_name": n, "columns": d.get("columns", {})}
             for n, d in all_s.items()},
            indent=2
        )
        st.download_button("⬇️ Export all schemas (JSON)", data=export_blob,
            file_name="schemas_export.json", mime="application/json")

    with mgr_r:
        create_tab, import_tab = st.tabs(["➕ Create new", "📥 Import JSON"])

        with create_tab:
            new_name = st.text_input("Master name", placeholder="e.g. Schedule Master")

            if "nc" not in st.session_state:
                st.session_state.nc = []

            with st.container(border=True):
                st.markdown("**Add a column**")
                a1, a2 = st.columns(2)
                with a1:
                    cin_name = st.text_input("Column name", placeholder="e.g. schedule-type", key="cin_name")
                with a2:
                    cin_type = st.selectbox("Type", key="cin_type",
                        options=["varchar", "int", "timestamp", "boolean", "enum", "foreign_key"])

                cin_max_len  = None
                cin_allowed  = []
                cin_ref_vals = []

                if cin_type == "varchar":
                    cin_max_len = st.number_input("Max length (characters)",
                        min_value=1, max_value=65535, value=255, key="cin_max")
                elif cin_type == "enum":
                    raw_enum    = st.text_input("Allowed values — comma separated",
                        placeholder="H, G, X, SOS", key="cin_enum")
                    cin_allowed = [v.strip() for v in raw_enum.split(",") if v.strip()]
                    if cin_allowed:
                        st.caption(f"Detected: {cin_allowed}")
                elif cin_type == "foreign_key":
                    raw_fk       = st.text_area("Reference values — one per line",
                        placeholder="REF001\nREF002", key="cin_fk", height=80)
                    cin_ref_vals = [v.strip() for v in raw_fk.splitlines() if v.strip()]
                    if cin_ref_vals:
                        st.caption(f"{len(cin_ref_vals)} reference values loaded")

                b1, b2, b3 = st.columns(3)
                with b1: cin_nullable  = st.checkbox("Nullable",  value=True,  key="cin_null")
                with b2: cin_unique    = st.checkbox("Unique",    value=False, key="cin_uniq")
                with b3: cin_ci_unique = st.checkbox("CI Unique", value=False, key="cin_ci",
                    help="Case-insensitive uniqueness check")

                if st.button("➕ Add column", use_container_width=True, key="btn_add_col"):
                    if not cin_name.strip():
                        st.warning("Enter a column name.")
                    else:
                        rule = {
                            "type":                    cin_type,
                            "nullable":                cin_nullable,
                            "unique":                  cin_unique,
                            "case_insensitive_unique": cin_ci_unique,
                        }
                        if cin_type == "varchar":
                            rule["max_length"]       = int(cin_max_len)
                        elif cin_type == "enum":
                            rule["allowed_values"]   = cin_allowed
                        elif cin_type == "foreign_key":
                            rule["reference_values"] = cin_ref_vals

                        st.session_state.nc.append({"name": cin_name.strip(), "rules": rule})
                        st.success(f"Column '{cin_name.strip()}' added.")

            if st.session_state.nc:
                st.markdown(f"**Columns in new schema ({len(st.session_state.nc)})**")
                for i, col in enumerate(st.session_state.nc):
                    r1, r2 = st.columns([5, 1])
                    with r1:
                        t      = col['rules']['type']
                        detail = ""
                        if t == "varchar":
                            detail = f", max {col['rules'].get('max_length', 255)}"
                        elif t == "enum":
                            detail = f": {', '.join(str(v) for v in col['rules'].get('allowed_values', []))}"
                        elif t == "foreign_key":
                            detail = f", {len(col['rules'].get('reference_values', []))} refs"
                        st.markdown(f"`{col['name']}` — **{t}**{detail}")
                    with r2:
                        if st.button("✕", key=f"rm_{i}"):
                            st.session_state.nc.pop(i)
                            st.rerun()

                st.divider()
                if st.button("💾 Save schema", type="primary", use_container_width=True):
                    if not new_name.strip():
                        st.warning("Enter a master name first.")
                    else:
                        new_def = {"columns": {col["name"]: col["rules"] for col in st.session_state.nc}}
                        saved_schemas[new_name.strip()] = new_def
                        if save_schemas_to_file(saved_schemas):
                            st.success(f"✅ Schema '{new_name}' saved! It's now available in the Validate tab.")
                            st.session_state.nc = []
                            st.rerun()
                        else:
                            st.error("Save failed — check file write permissions.")

        with import_tab:
            st.markdown("Paste a JSON schema (exported from this tool, or hand-crafted).")
            st.code('''{
  "schema_name": "Schedule Master",
  "columns": {
    "name": {
      "type": "varchar",
      "max_length": 100,
      "nullable": false,
      "unique": false,
      "case_insensitive_unique": false
    },
    "schedule-type": {
      "type": "enum",
      "allowed_values": ["H", "G", "X", "SOS"],
      "nullable": false,
      "unique": false,
      "case_insensitive_unique": false
    }
  }
}''', language="json")

            json_paste = st.text_area("Paste JSON here", height=180, key="json_import")

            if st.button("📥 Import schema", use_container_width=True):
                try:
                    parsed      = json.loads(json_paste)
                    import_name = parsed.get("schema_name", "").strip()
                    import_cols = parsed.get("columns", {})
                    if not import_name:
                        st.error("JSON must include a 'schema_name' field.")
                    elif not import_cols:
                        st.error("JSON must include a 'columns' field with at least one column.")
                    else:
                        saved_schemas[import_name] = {"columns": import_cols}
                        if save_schemas_to_file(saved_schemas):
                            st.success(f"✅ Imported '{import_name}' successfully!")
                            st.rerun()
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON: {e}")
