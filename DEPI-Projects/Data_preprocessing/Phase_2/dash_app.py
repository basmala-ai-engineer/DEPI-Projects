# ============================================================
# FORD GOBIKE | ANALYTICS PLATFORM
# Supabase + Streamlit Dashboard
# ============================================================

import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import streamlit as st

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Ford GoBike | Analytics Platform",
    page_icon="🚲",
    layout="wide",
)


# ============================================================
# COLORS
# ============================================================

PRIMARY_BLUE = "#0B5A82"
PRIMARY_DARK = "#084866"
SOFT_BLUE = "#F4FAFE"
TEXT = "#243B53"
MUTED = "#718096"
WHITE = "#FFFFFF"
BORDER = "#E1EAF2"
BACKGROUND = "#F6FAFD"

st.markdown(
    f"""
    <style>
        /* ---------- Page ---------- */
        .stApp {{ background-color: {BACKGROUND}; }}
        header[data-testid="stHeader"] {{ background: transparent; }}
        .block-container {{ padding-top: 2rem; max-width: 1400px; }}

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {{ background-color: {PRIMARY_DARK}; }}
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {{
            color: {WHITE};
        }}
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
            color: {WHITE};
            font-size: 12px;
            font-weight: 600;
        }}
        section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
            color: #CFE8F5;
        }}

        /* ---------- Tabs (navigation) ---------- */
        div[data-baseweb="tab-list"] {{
            background-color: {WHITE};
            border: 1px solid {BORDER};
            border-radius: 10px;
            padding: 10px;
            gap: 8px;
        }}
        button[data-baseweb="tab"] {{
            background-color: {WHITE};
            border-radius: 8px;
            padding: 8px 18px;
            height: auto;
        }}
        button[data-baseweb="tab"] p {{
            color: {MUTED};
            font-weight: 600;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            background-color: {PRIMARY_BLUE};
        }}
        button[data-baseweb="tab"][aria-selected="true"] p {{
            color: {WHITE};
        }}
        div[data-baseweb="tab-highlight"],
        div[data-baseweb="tab-border"] {{ display: none; }}

        /* ---------- KPI cards ---------- */
        div[data-testid="stMetric"] {{
            background-color: {WHITE};
            border: 1px solid {BORDER};
            border-radius: 12px;
            padding: 16px 18px;
            box-shadow: 0 2px 8px rgba(15, 50, 70, 0.04);
        }}
        div[data-testid="stMetricLabel"] p {{
            color: {MUTED};
            font-size: 13px;
            font-weight: 600;
        }}
        div[data-testid="stMetricValue"] {{
            color: {PRIMARY_BLUE};
            font-weight: 700;
        }}

        /* ---------- Chart cards ---------- */
        div[data-testid="stPlotlyChart"] {{
            background-color: {WHITE};
            border: 1px solid {BORDER};
            border-radius: 12px;
            padding: 10px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SETTINGS (Streamlit Secrets or environment / .env)
# ============================================================

def get_setting(name):
    value = os.getenv(name)

    if value is None:
        try:
            value = st.secrets[name]
        except Exception:
            value = None

    return value


# ============================================================
# LOAD + PREPARE DATA (cached)
# ============================================================

def create_age_group(age):
    if pd.isna(age):
        return "Unknown"
    if 18 <= age <= 24:
        return "18-24"
    if 25 <= age <= 34:
        return "25-34"
    if 35 <= age <= 44:
        return "35-44"
    if 45 <= age <= 54:
        return "45-54"
    if 55 <= age <= 64:
        return "55-64"
    if age >= 65:
        return "65+"
    return "Unknown"


def get_peak_period(hour):
    if 7 <= hour <= 9:
        return "Morning Peak"
    if 16 <= hour <= 18:
        return "Evening Peak"
    if 10 <= hour <= 15:
        return "Midday"
    return "Off-Peak"


@st.cache_data(show_spinner="Loading data from Supabase...", ttl=3600)
def load_data():

    # ---------------- Database ----------------
    conn = psycopg2.connect(
        host=get_setting("DB_HOST"),
        port=get_setting("DB_PORT"),
        database=get_setting("DB_NAME"),
        user=get_setting("DB_USER"),
        password=get_setting("DB_PASSWORD"),
    )

    try:
        df = pd.read_sql_query(
            "SELECT * FROM vw_fordgobike_analysis;",
            conn,
        )
    finally:
        conn.close()

    # ---------------- Datetime ----------------
    df["start_time"] = pd.to_datetime(
        df["start_time"], errors="coerce", utc=True
    ).dt.tz_localize(None)

    df["end_time"] = pd.to_datetime(
        df["end_time"], errors="coerce", utc=True
    ).dt.tz_localize(None)

    # ---------------- February 2019 only ----------------
    min_date = pd.Timestamp("2019-02-01")
    max_date = pd.Timestamp("2019-02-28")

    df = df[
        (df["start_time"] >= min_date)
        & (df["start_time"] < max_date + pd.Timedelta(days=1))
    ].copy()

    # ---------------- Numeric cleaning ----------------
    numeric_columns = [
        "duration_sec",
        "duration_min",
        "duration_hour",
        "member_age",
        "start_station_latitude",
        "start_station_longitude",
        "end_station_latitude",
        "end_station_longitude",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    # ---------------- Age ----------------
    df.loc[
        (df["member_age"] < 18) | (df["member_age"] > 100),
        "member_age",
    ] = np.nan

    df["age_group"] = df["member_age"].apply(create_age_group)

    # ---------------- Gender ----------------
    df["member_gender"] = (
        df["member_gender"].fillna("Other").astype(str).str.strip()
    )
    df["member_gender"] = df["member_gender"].replace(
        {"": "Other", "nan": "Other", "None": "Other"}
    )

    # ---------------- User type ----------------
    df["user_type"] = (
        df["user_type"].fillna("Unknown").astype(str).str.strip()
    )

    # ---------------- Time features ----------------
    df["hour"] = df["start_time"].dt.hour
    df["day_name"] = df["start_time"].dt.day_name()
    df["trip_date"] = df["start_time"].dt.date
    df["peak_period"] = df["hour"].apply(get_peak_period)

    # ---------------- Duration ----------------
    if "duration_min" not in df.columns:
        df["duration_min"] = df["duration_sec"] / 60

    if "duration_hour" not in df.columns:
        df["duration_hour"] = df["duration_sec"] / 3600

    return df


try:
    df = load_data()
except Exception:
    st.error(
        "Could not connect to the database. "
        "Please check the DB_* values in the app Secrets."
    )
    st.stop()


# ============================================================
# HELPERS
# ============================================================

AGE_ORDER = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+", "Unknown"]

WEEKDAY_ORDER = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

PEAK_ORDER = ["Morning Peak", "Midday", "Evening Peak", "Off-Peak"]


def style_fig(fig):
    fig.update_layout(
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(family="Arial", color=TEXT),
        margin=dict(l=45, r=25, t=30, b=45),
        hoverlabel=dict(bgcolor=WHITE, font_color=TEXT),
        legend=dict(bgcolor="rgba(255,255,255,0)"),
    )
    fig.update_xaxes(showgrid=False, linecolor=BORDER)
    fig.update_yaxes(gridcolor="#EDF2F7", zeroline=False)
    return fig


def bar_chart(data, x, y, x_title, y_title, orientation="v"):
    fig = px.bar(data, x=x, y=y, orientation=orientation)
    fig.update_layout(xaxis_title=x_title, yaxis_title=y_title)
    fig.update_traces(marker_color=PRIMARY_BLUE)
    return style_fig(fig)


def show(fig):
    st.plotly_chart(fig, use_container_width=True)


def filter_data(data, user_type, gender, age_group, start_date, end_date):
    filtered = data

    if user_type != "All":
        filtered = filtered[filtered["user_type"] == user_type]

    if gender != "All":
        filtered = filtered[filtered["member_gender"] == gender]

    if age_group != "All":
        filtered = filtered[filtered["age_group"] == age_group]

    if start_date:
        filtered = filtered[filtered["start_time"].dt.date >= start_date]

    if end_date:
        filtered = filtered[filtered["start_time"].dt.date <= end_date]

    return filtered


def build_map(map_data):
    center_lat = map_data["start_station_latitude"].mean()
    center_lon = map_data["start_station_longitude"].mean()

    hover = "<b>%{text}</b><br>Trips: %{customdata[0]}<extra></extra>"

    try:
        fig = go.Figure(
            go.Scattermap(
                lat=map_data["start_station_latitude"],
                lon=map_data["start_station_longitude"],
                mode="markers",
                marker=dict(size=10, color=PRIMARY_BLUE),
                text=map_data["start_station_name"],
                customdata=map_data[["trips"]],
                hovertemplate=hover,
            )
        )
        fig.update_layout(
            map=dict(
                style="open-street-map",
                center=dict(lat=center_lat, lon=center_lon),
                zoom=11,
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor=WHITE,
            height=600,
        )

    except AttributeError:
        fig = go.Figure(
            go.Scattermapbox(
                lat=map_data["start_station_latitude"],
                lon=map_data["start_station_longitude"],
                mode="markers",
                marker=dict(size=10, color=PRIMARY_BLUE),
                text=map_data["start_station_name"],
                customdata=map_data[["trips"]],
                hovertemplate=hover,
            )
        )
        fig.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=center_lat, lon=center_lon),
                zoom=11,
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor=WHITE,
            height=600,
        )

    return fig


def card_title(title):
    st.markdown(
        f"<div style='font-size:15px; font-weight:700; color:{TEXT}; "
        f"margin: 6px 0 8px 0;'>{title}</div>",
        unsafe_allow_html=True,
    )


def insight_card(title, text):
    st.markdown(
        f"""
        <div style="background-color:{SOFT_BLUE};
                    border-left:4px solid {PRIMARY_BLUE};
                    border-radius:8px; padding:15px; margin-bottom:10px;">
            <div style="font-size:14px; font-weight:700;
                        color:{PRIMARY_BLUE}; margin-bottom:7px;">{title}</div>
            <div style="font-size:13px; line-height:1.6;
                        color:{TEXT};">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown("## 🚲 Ford GoBike")
st.sidebar.caption("Analytics Platform")
st.sidebar.markdown("---")
st.sidebar.markdown("**FILTERS**")

user_type = st.sidebar.selectbox(
    "User Type",
    ["All"] + sorted(df["user_type"].dropna().unique()),
)

gender = st.sidebar.selectbox(
    "Gender",
    ["All"] + sorted(df["member_gender"].dropna().unique()),
)

age_group = st.sidebar.selectbox(
    "Age Group",
    ["All"] + [a for a in AGE_ORDER if a in df["age_group"].unique()],
)

DATE_MIN = pd.Timestamp("2019-02-01").date()
DATE_MAX = pd.Timestamp("2019-02-28").date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(DATE_MIN, DATE_MAX),
    min_value=DATE_MIN,
    max_value=DATE_MAX,
)

if isinstance(date_range, (list, tuple)):
    if len(date_range) == 2:
        start_date, end_date = date_range
    elif len(date_range) == 1:
        start_date = end_date = date_range[0]
    else:
        start_date, end_date = DATE_MIN, DATE_MAX
else:
    start_date = end_date = date_range


# ============================================================
# HEADER
# ============================================================

st.markdown(
    f"""
    <div style="margin-bottom: 8px;">
        <span style="font-size:28px; font-weight:800; color:{PRIMARY_BLUE};">
            Ford GoBike
        </span>
        <span style="font-size:28px; font-weight:500; color:{TEXT};">
            Analytics Platform
        </span>
        <div style="font-size:13px; color:{MUTED};">February 2019</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FILTERED DATA
# ============================================================

filtered = filter_data(
    df, user_type, gender, age_group, start_date, end_date
)

if filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()


# ============================================================
# TABS
# ============================================================

tab_overview, tab_time, tab_user, tab_duration, tab_stations = st.tabs(
    [
        "Overview",
        "Time Analysis",
        "User Analysis",
        "Duration Analysis",
        "Stations",
    ]
)


# ============================================================
# PAGE 1 - OVERVIEW
# ============================================================

with tab_overview:

    total_trips = len(filtered)
    avg_duration = filtered["duration_min"].mean()
    active_bikes = filtered["bike_id"].nunique()
    avg_age = filtered["member_age"].mean()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Trips", f"{total_trips:,}")
    k2.metric("Average Duration", f"{avg_duration:.1f} min")
    k3.metric("Active Bikes", f"{active_bikes:,}")
    k4.metric("Average Age", f"{avg_age:.1f}")

    col_a, col_b = st.columns([2, 1])

    with col_a:
        card_title("Daily Trips")

        daily = (
            filtered.groupby("trip_date").size().reset_index(name="trips")
        )
        daily["trip_date"] = pd.to_datetime(daily["trip_date"])
        daily = daily.sort_values("trip_date")

        fig_daily = px.line(daily, x="trip_date", y="trips", markers=True)
        fig_daily.update_traces(
            line=dict(color=PRIMARY_BLUE, width=3),
            marker=dict(size=6),
        )
        fig_daily.update_layout(xaxis_title="Date", yaxis_title="Trips")
        show(style_fig(fig_daily))

    with col_b:
        card_title("User Type Distribution")

        user_counts = filtered["user_type"].value_counts().reset_index()
        user_counts.columns = ["user_type", "count"]

        fig_user_type = px.pie(
            user_counts, names="user_type", values="count", hole=0.55
        )
        fig_user_type.update_traces(textinfo="percent+label")
        show(style_fig(fig_user_type))

    card_title("Key Insights")

    most_common_user = filtered["user_type"].value_counts().idxmax()
    busiest_hour = filtered["hour"].value_counts().idxmax()
    most_common_gender = filtered["member_gender"].value_counts().idxmax()

    top_station_series = (
        filtered["start_station_name"].dropna().value_counts()
    )
    top_station = (
        top_station_series.index[0] if not top_station_series.empty else "N/A"
    )

    insight_card(
        "Most common user type",
        f"{most_common_user} accounts for the largest share of trips "
        f"in the selected data.",
    )
    insight_card(
        "Peak hour",
        f"The highest trip activity occurs around {busiest_hour}:00.",
    )
    insight_card(
        "Gender distribution",
        f"{most_common_gender} is the most represented gender "
        f"category in the selected data.",
    )
    insight_card(
        "Top start station",
        f"{top_station} has the highest number of recorded trip starts.",
    )


# ============================================================
# PAGE 2 - TIME ANALYSIS
# ============================================================

with tab_time:

    col_a, col_b = st.columns(2)

    with col_a:
        card_title("Trips by Hour")
        hourly = (
            filtered.groupby("hour")
            .size()
            .reset_index(name="trips")
            .sort_values("hour")
        )
        show(bar_chart(hourly, "hour", "trips", "Hour of Day", "Trips"))

    with col_b:
        card_title("Trips by Weekday")
        weekday = (
            filtered.groupby("day_name")
            .size()
            .reindex(WEEKDAY_ORDER)
            .fillna(0)
            .rename_axis("day_name")
            .reset_index(name="trips")
        )
        show(bar_chart(weekday, "day_name", "trips", "Day", "Trips"))

    card_title("Peak Period Distribution")
    peak = (
        filtered.groupby("peak_period")
        .size()
        .reindex(PEAK_ORDER)
        .fillna(0)
        .rename_axis("peak_period")
        .reset_index(name="trips")
    )
    show(bar_chart(peak, "peak_period", "trips", "Period", "Trips"))


# ============================================================
# PAGE 3 - USER ANALYSIS
# ============================================================

with tab_user:

    col_a, col_b = st.columns(2)

    with col_a:
        card_title("Gender Distribution")
        gender_data = filtered["member_gender"].value_counts().reset_index()
        gender_data.columns = ["gender", "count"]
        show(bar_chart(gender_data, "gender", "count", "Gender", "Trips"))

    with col_b:
        card_title("Age Group Distribution")
        age_data = (
            filtered.groupby("age_group")
            .size()
            .reindex(AGE_ORDER)
            .fillna(0)
            .rename_axis("age_group")
            .reset_index(name="count")
        )
        show(bar_chart(age_data, "age_group", "count", "Age Group", "Trips"))

    card_title("User Composition")
    composition = (
        filtered.groupby(["user_type", "member_gender"])
        .size()
        .reset_index(name="count")
    )
    fig_composition = px.bar(
        composition,
        x="user_type",
        y="count",
        color="member_gender",
        barmode="group",
    )
    fig_composition.update_layout(xaxis_title="User Type", yaxis_title="Trips")
    show(style_fig(fig_composition))


# ============================================================
# PAGE 4 - DURATION ANALYSIS
# ============================================================

with tab_duration:

    col_a, col_b = st.columns(2)

    with col_a:
        card_title("Average Duration by User Type")
        duration_user = (
            filtered.groupby("user_type")["duration_min"].mean().reset_index()
        )
        show(
            bar_chart(
                duration_user,
                "user_type",
                "duration_min",
                "User Type",
                "Average Duration (min)",
            )
        )

    with col_b:
        card_title("Average Duration by Gender")
        duration_gender = (
            filtered.groupby("member_gender")["duration_min"]
            .mean()
            .reset_index()
        )
        show(
            bar_chart(
                duration_gender,
                "member_gender",
                "duration_min",
                "Gender",
                "Average Duration (min)",
            )
        )

    col_c, col_d = st.columns(2)

    with col_c:
        card_title("Average Duration by Age Group")
        duration_age = (
            filtered.groupby("age_group")["duration_min"]
            .mean()
            .reindex(AGE_ORDER)
            .dropna()
            .rename_axis("age_group")
            .reset_index()
        )
        show(
            bar_chart(
                duration_age,
                "age_group",
                "duration_min",
                "Age Group",
                "Average Duration (min)",
            )
        )

    with col_d:
        card_title("Trip Duration Distribution")
        histogram_data = filtered[filtered["duration_min"].between(0, 120)]
        fig_histogram = px.histogram(
            histogram_data, x="duration_min", nbins=40
        )
        fig_histogram.update_layout(
            xaxis_title="Duration (minutes)", yaxis_title="Trips"
        )
        fig_histogram.update_traces(marker_color=PRIMARY_BLUE)
        show(style_fig(fig_histogram))


# ============================================================
# PAGE 5 - STATIONS
# ============================================================

with tab_stations:

    col_a, col_b = st.columns(2)

    with col_a:
        card_title("Top Start Stations")
        start_stations = (
            filtered["start_station_name"]
            .dropna()
            .value_counts()
            .head(10)
            .sort_values()
            .reset_index()
        )
        start_stations.columns = ["station", "count"]
        show(
            bar_chart(
                start_stations,
                "count",
                "station",
                "Trips",
                "Start Station",
                orientation="h",
            )
        )

    with col_b:
        card_title("Top End Stations")
        end_stations = (
            filtered["end_station_name"]
            .dropna()
            .value_counts()
            .head(10)
            .sort_values()
            .reset_index()
        )
        end_stations.columns = ["station", "count"]
        show(
            bar_chart(
                end_stations,
                "count",
                "station",
                "Trips",
                "End Station",
                orientation="h",
            )
        )

    card_title("Station Activity Map")

    map_data = filtered[
        [
            "start_station_name",
            "start_station_latitude",
            "start_station_longitude",
        ]
    ].dropna()

    map_data = (
        map_data.groupby(
            [
                "start_station_name",
                "start_station_latitude",
                "start_station_longitude",
            ]
        )
        .size()
        .reset_index(name="trips")
    )

    if map_data.empty:
        st.info("No station location data available.")
    else:
        show(build_map(map_data))