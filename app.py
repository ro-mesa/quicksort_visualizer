import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from algorithms.quick_sort import quick_sort, quick_sort_with_steps

# ============================================================
# PAGE CONFIG & CLEAN EDITORIAL PALETTE (PLUM / CORAL / ALABASTER)
# ============================================================

st.set_page_config(
    page_title="Quick Sort Studio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700;800&display=swap');

    /* Hide Streamlit Default Header, Sidebar, Toolbar & Footer */
    header[data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"],
    #MainMenu,
    footer {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }

    /* Clean Off-White Canvas */
    html, body, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        background-color: #F6F7FB !important;
        background-image: none !important;
        color: #1E2438 !important;
        font-family: 'Inter', sans-serif !important;
    }

    .block-container {
        padding-top: 1.4rem !important;
        padding-bottom: 3rem !important;
        max-width: 1320px;
    }

    h1, h2, h3, h4, p, span, label, div {
        font-family: 'Inter', sans-serif;
    }

    /* Hamburger Trigger Button */
    .st-key-toggle_qs_menu_btn button {
        width: 44px !important;
        min-width: 44px !important;
        height: 44px !important;
        min-height: 44px !important;
        padding: 0 !important;
        border-radius: 12px !important;
        background: #2B3044 !important;
        border: none !important;
        color: #FFFFFF !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(43, 48, 68, 0.18) !important;
        transition: all 0.18s ease !important;
    }
    .st-key-toggle_qs_menu_btn button:hover {
        background: #E94E65 !important;
        transform: translateY(-1px) !important;
    }
    .st-key-toggle_qs_menu_btn button * {
        color: #FFFFFF !important;
    }

    /* Floating Configuration Drawer (Clean Light Mode Fix) */
    .st-key-qs_floating_menu {
        position: fixed !important;
        top: 76px !important;
        left: 32px !important;
        width: 340px !important;
        max-width: 92vw !important;
        max-height: 84vh !important;
        overflow-y: auto !important;
        z-index: 9999 !important;
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-top: 4px solid #E94E65 !important;
        border-radius: 16px !important;
        padding: 18px 20px !important;
        box-shadow: 0 24px 48px rgba(30, 36, 56, 0.18) !important;
        animation: menuDrop 0.18s ease-out forwards;
    }
    .st-key-qs_floating_menu label,
    .st-key-qs_floating_menu p,
    .st-key-qs_floating_menu span {
        color: #334155 !important;
        font-weight: 600 !important;
    }
    .st-key-qs_floating_menu div[data-baseweb="input"] > div,
    .st-key-qs_floating_menu div[data-baseweb="select"] > div {
        background-color: #F8FAFC !important;
        color: #1E2438 !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
    }
    .st-key-qs_floating_menu div[data-baseweb="input"] input,
    .st-key-qs_floating_menu div[data-baseweb="select"] span {
        color: #1E2438 !important;
        -webkit-text-fill-color: #1E2438 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
    }

    @keyframes menuDrop {
        from { opacity: 0; transform: translateY(-6px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Minimal Top Header */
    .studio-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        padding: 0.25rem 0.25rem 0.75rem 0.25rem;
    }

    .active-chip {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.78rem;
        font-weight: 600;
        color: #5E2750 !important;
        background: #F3E8FF;
        padding: 6px 14px;
        border-radius: 999px;
    }

    /* Main Visualizer Card Header (Plum -> Coral Gradient) */
    .viz-card-top {
        background: linear-gradient(90deg, #5E2750 0%, #9E3B67 55%, #E94E65 100%);
        color: #FFFFFF !important;
        border-radius: 16px 16px 0 0;
        padding: 0.9rem 1.35rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
    }

    .legend-row {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
        font-size: 0.8rem;
        font-weight: 600;
        color: #FFFFFF !important;
    }

    .swatch {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 6px;
        border: 1.5px solid rgba(255, 255, 255, 0.85);
    }

    /* Unified Single-Row Telemetry Strip */
    .metrics-bar {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        background: #FFFFFF;
        border: 1px solid #E6E9F2;
        border-radius: 14px;
        padding: 0.9rem 0.5rem;
        margin: 1rem 0 1.4rem 0;
        box-shadow: 0 4px 16px rgba(30, 36, 56, 0.04);
    }

    .metric-cell {
        text-align: center;
        border-right: 1px solid #EEF1F6;
        padding: 0 0.75rem;
    }
    .metric-cell:last-child {
        border-right: none;
    }

    .metric-title {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748B !important;
    }

    .metric-val {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.45rem;
        font-weight: 800;
        margin-top: 2px;
    }

    /* Buttons */
    .stButton > button[kind="secondary"] {
        background: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        color: #1E2438 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.84rem !important;
        padding: 0.45rem 0.9rem !important;
        transition: all 0.16s ease !important;
    }
    .stButton > button[kind="secondary"]:hover {
        border-color: #E94E65 !important;
        color: #E94E65 !important;
        background: #FFF5F7 !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #5E2750, #E94E65) !important;
        border: none !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 0.45rem 1rem !important;
        box-shadow: 0 4px 14px rgba(233, 78, 101, 0.22) !important;
    }
    .stButton > button[kind="primary"] * {
        color: #FFFFFF !important;
    }

    /* Clean Content Cards */
    .clean-card {
        background: #FFFFFF;
        border: 1px solid #E6E9F2;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 6px 20px rgba(30, 36, 56, 0.04);
        margin-bottom: 1rem;
    }

    .clean-card-head {
        padding: 0.85rem 1.25rem;
        color: #FFFFFF !important;
        font-weight: 700;
        font-size: 0.96rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .clean-card-head span {
        color: #FFFFFF !important;
    }

    .clean-card-body {
        padding: 1.2rem 1.35rem;
        color: #334155 !important;
        font-size: 0.92rem;
        line-height: 1.68;
    }

    .pill-tag {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.75rem;
        font-weight: 700;
        background: rgba(255, 255, 255, 0.22);
        color: #FFFFFF !important;
        padding: 3px 10px;
        border-radius: 999px;
    }

    /* Tabs */
    [data-testid="stTabs"] [role="tab"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        color: #64748B !important;
        padding-bottom: 0.65rem !important;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        color: #E94E65 !important;
        border-bottom-color: #E94E65 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

PLOT_LAYOUT = {
    "template": "plotly_white",
    "paper_bgcolor": "#FFFFFF",
    "plot_bgcolor": "#FFFFFF",
    "font": {"color": "#1E2438", "family": "JetBrains Mono, monospace"},
    "margin": dict(l=24, r=24, t=28, b=24),
}


def build_sort_chart(values, pivot_index, comparing, action):
    """Build a clean, airy bar chart with pointer tags (PIVOT, i, lt, gt) embedded directly under each bar."""
    n = len(values)
    pivot_val = values[pivot_index] if (pivot_index is not None and 0 <= pivot_index < n) else None

    lt_idx = None
    gt_idx = None
    if action != "complete" and pivot_val is not None:
        less_indices = [idx for idx, v in enumerate(values) if v < pivot_val]
        greater_indices = [idx for idx, v in enumerate(values) if v > pivot_val]
        lt_idx = (max(less_indices) + 1) if less_indices else 0
        gt_idx = (min(greater_indices) - 1) if greater_indices else (n - 1)

    colors = []
    x_labels = []
    for idx, val in enumerate(values):
        tags = []
        if action == "complete":
            colors.append("#10B981")
        elif pivot_index is not None and idx == pivot_index:
            colors.append("#5E2750")
            tags.append("PIVOT")
        elif comparing is not None and idx == comparing:
            colors.append("#E94E65")
            tags.append("i")
        else:
            colors.append("#CBD5E1")

        if action != "complete" and pivot_val is not None:
            if lt_idx is not None and idx == min(lt_idx, n - 1):
                tags.append("lt")
            if gt_idx is not None and idx == max(gt_idx, 0):
                tags.append("gt")

        tag_line = f"<br><b>{' · '.join(tags)}</b>" if tags else "<br> "
        x_labels.append(f"[{idx}]{tag_line}")

    fig = go.Figure(
        data=[
            go.Bar(
                x=x_labels,
                y=values,
                text=[f"{v:g}" for v in values],
                textposition="outside",
                textfont=dict(family="JetBrains Mono, monospace", size=14, color="#1E2438"),
                width=0.52,
                marker=dict(
                    color=colors,
                    line=dict(color="rgba(30,36,56,0.08)", width=1),
                ),
            )
        ]
    )
    max_val = max(values) if values else 10
    fig.update_layout(
        **PLOT_LAYOUT,
        height=340,
        showlegend=False,
        xaxis_title="",
        yaxis_title="",
        yaxis=dict(
            range=[0, max_val * 1.2],
            gridcolor="#F1F5F9",
            zeroline=False,
            showticklabels=True,
            tickfont=dict(color="#94A3B8", size=11),
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(family="JetBrains Mono, monospace", size=12, color="#334155"),
        ),
    )
    return fig


def trigger_sort_run(records, direction):
    sorted_result, final_stats, execution_steps = quick_sort_with_steps(
        records,
        key="value",
        ascending=(direction == "Ascending"),
    )
    st.session_state["qs_steps"] = execution_steps
    st.session_state["qs_sorted_result"] = sorted_result
    st.session_state["qs_final_stats"] = final_stats
    st.session_state["qs_step_index"] = 0
    st.session_state["qs_history_slider"] = 0


# ============================================================
# SESSION DEFAULTS & INPUT PARSING
# ============================================================

if "qs_custom_input" not in st.session_state:
    st.session_state["qs_custom_input"] = "40, 20, 60, 10, 30, 50, 70"

if "qs_direction" not in st.session_state:
    st.session_state["qs_direction"] = "Ascending"

if "qs_menu_open" not in st.session_state:
    st.session_state["qs_menu_open"] = False

if "show_code_panel" not in st.session_state:
    st.session_state["show_code_panel"] = False

records = []
input_error_msg = None
try:
    numbers = [float(x.strip()) for x in st.session_state["qs_custom_input"].split(",") if x.strip()]
    if not numbers:
        raise ValueError("Enter at least one number.")
    if len(numbers) > 50:
        raise ValueError("Maximum 50 elements allowed.")
    records = [{"index": i, "value": num} for i, num in enumerate(numbers)]
except ValueError as err:
    input_error_msg = str(err)


# ============================================================
# TOP HEADER BAR: HAMBURGER MENU + CLEAN TITLE
# ============================================================

ham_col, title_col = st.columns([0.42, 7.58], vertical_alignment="center")

with ham_col:
    ham_symbol = "✕" if st.session_state["qs_menu_open"] else "☰"
    if st.button(ham_symbol, key="toggle_qs_menu_btn", help="Open Sorting Configuration"):
        st.session_state["qs_menu_open"] = not st.session_state["qs_menu_open"]
        st.rerun()

with title_col:
    st.markdown(
        f"""
        <div class="studio-header">
            <div>
                <div style="font-size:1.5rem; font-weight:800; color:#1E2438;">Quick Sort Visualizer</div>
                <div style="font-size:0.86rem; color:#64748B;">Randomized Three-Way Partitioning &bull; Interactive Step Execution &amp; Complexity Analysis</div>
            </div>
            <span class="active-chip">{len(records)} Elements &bull; {st.session_state['qs_direction']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# FLOATING HAMBURGER CONFIGURATION DRAWER
# ============================================================

if st.session_state["qs_menu_open"]:
    with st.container(key="qs_floating_menu"):
        m_head, m_close = st.columns([4, 1], vertical_alignment="center")
        with m_head:
            st.markdown(
                '<div style="font-size:1rem; font-weight:800; color:#1E2438;">Sorting Configuration</div>'
                '<div style="font-size:0.76rem; color:#64748B;">Choose a preset or enter custom values</div>',
                unsafe_allow_html=True,
            )
        with m_close:
            if st.button("✕", key="close_qs_menu_inside", help="Close"):
                st.session_state["qs_menu_open"] = False
                st.rerun()

        st.markdown('<div style="border-bottom:1px solid #EEF1F6; margin:10px 0 12px 0;"></div>', unsafe_allow_html=True)

        presets = [
            ("Best Case (Balanced Split)", "40, 20, 60, 10, 30, 50, 70"),
            ("Average Case (Random)", "50, 25, 75, 12, 37, 62, 88"),
            ("Worst-Case Input (Sorted)", "10, 20, 30, 40, 50, 60, 70"),
            ("Duplicate-Heavy (3-Way)", "40, 20, 40, 80, 40, 20, 80, 40"),
            ("Reverse-Sorted Array", "90, 75, 60, 45, 30, 15, 5"),
        ]
        for idx, (label, preset_str) in enumerate(presets):
            if st.button(label, key=f"menu_preset_{idx}", use_container_width=True):
                st.session_state["qs_custom_input"] = preset_str
                st.session_state.pop("qs_steps", None)
                st.session_state["qs_menu_open"] = False
                st.rerun()

        st.markdown('<div style="border-bottom:1px solid #EEF1F6; margin:12px 0;"></div>', unsafe_allow_html=True)
        st.text_input("Custom Array (comma-separated)", key="qs_custom_input")
        if input_error_msg:
            st.error(input_error_msg)

        st.selectbox("Sorting Order", ["Ascending", "Descending"], key="qs_direction")

        c_info, c_apply = st.columns([1, 1.5], vertical_alignment="center")
        with c_info:
            st.markdown(
                f'<div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:6px 10px; text-align:center;">'
                f'<div style="font-size:0.65rem; font-weight:700; color:#64748B;">ELEMENTS</div>'
                f'<div style="font-family:JetBrains Mono,monospace; font-size:1.1rem; font-weight:800; color:#5E2750;">{len(records)}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with c_apply:
            if st.button("Apply & Sort", type="primary", use_container_width=True, disabled=not records):
                trigger_sort_run(records, st.session_state["qs_direction"])
                st.session_state["qs_menu_open"] = False
                st.rerun()


if records and "qs_steps" not in st.session_state:
    trigger_sort_run(records, st.session_state["qs_direction"])


# ============================================================
# MAIN VISUALIZER + PLAYBACK CONTROLS + CLEAN METRICS BAR
# ============================================================

if "qs_steps" in st.session_state and st.session_state["qs_steps"]:
    steps = st.session_state["qs_steps"]
    current_index = min(st.session_state.get("qs_step_index", 0), len(steps) - 1)
    current_step = steps[current_index]

    action = current_step["action"]
    current_array = current_step["array"]
    values = [float(item["value"]) for item in current_array]
    pivot_index = current_step.get("pivot_index")
    comparing = current_step.get("comparing")

    st.markdown(
        f"""
        <div class="viz-card-top">
            <div style="font-family:'JetBrains Mono', monospace; font-size:0.84rem; font-weight:700; color:#FFFFFF;">
                Step {current_index + 1} of {len(steps)} &mdash; {current_step['description']}
            </div>
            <div class="legend-row">
                <span><span class="swatch" style="background:#5E2750;"></span>Pivot</span>
                <span><span class="swatch" style="background:#E94E65;"></span>Scanning (i)</span>
                <span><span class="swatch" style="background:#CBD5E1;"></span>Unsorted</span>
                <span><span class="swatch" style="background:#10B981;"></span>Sorted</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    fig = build_sort_chart(values, pivot_index, comparing, action)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Compact Media-Player Controls
    ctrl1, ctrl2, ctrl3, ctrl4, ctrl_scrub = st.columns([0.9, 1.05, 0.9, 0.95, 3.4], vertical_alignment="center")
    with ctrl1:
        if st.button("⏮ Prev", key="qs_prev", disabled=current_index == 0, use_container_width=True):
            new_idx = max(0, current_index - 1)
            st.session_state["qs_step_index"] = new_idx
            st.session_state["qs_history_slider"] = new_idx
            st.rerun()
    with ctrl2:
        if st.button("Next ⏭", key="qs_next", type="primary", disabled=current_index >= len(steps) - 1, use_container_width=True):
            new_idx = min(len(steps) - 1, current_index + 1)
            st.session_state["qs_step_index"] = new_idx
            st.session_state["qs_history_slider"] = new_idx
            st.rerun()
    with ctrl3:
        if st.button("↺ Reset", key="qs_reset", use_container_width=True):
            st.session_state["qs_step_index"] = 0
            st.session_state["qs_history_slider"] = 0
            st.rerun()
    with ctrl4:
        if st.button("⏭ Finish", key="qs_finish", use_container_width=True):
            last_idx = len(steps) - 1
            st.session_state["qs_step_index"] = last_idx
            st.session_state["qs_history_slider"] = last_idx
            st.rerun()
    with ctrl_scrub:
        selected_step = st.slider(
            "Step Scrubber",
            0,
            len(steps) - 1,
            current_index,
            key="qs_history_slider",
            label_visibility="collapsed",
        )
        if selected_step != current_index:
            st.session_state["qs_step_index"] = selected_step
            st.rerun()

    # Single Unified Metrics Bar
    stats = current_step["stats"]
    st.markdown(
        f"""
        <div class="metrics-bar">
            <div class="metric-cell">
                <div class="metric-title">Comparisons</div>
                <div class="metric-val" style="color:#5E2750;">{stats['comparisons']}</div>
            </div>
            <div class="metric-cell">
                <div class="metric-title">Swaps</div>
                <div class="metric-val" style="color:#E94E65;">{stats['swaps']}</div>
            </div>
            <div class="metric-cell">
                <div class="metric-title">Recursive Calls</div>
                <div class="metric-val" style="color:#E05A47;">{stats['recursive_calls']}</div>
            </div>
            <div class="metric-cell">
                <div class="metric-title">Max Recursion Depth</div>
                <div class="metric-val" style="color:#059669;">{stats['max_recursion_depth']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if action == "complete":
        sorted_vals = [float(x["value"]) for x in st.session_state["qs_sorted_result"]]
        st.success(f"Sorted Output ({st.session_state['qs_direction']}): {', '.join(f'{v:g}' for v in sorted_vals)}")


# ============================================================
# CLEAN TABBED SECTIONS
# ============================================================

tab_algo, tab_complexity, tab_realworld = st.tabs(
    [
        "Algorithm & Code",
        "Complexity Analysis",
        "Real-World Implementations",
    ]
)

with tab_algo:
    st.markdown(
        """
        <div class="clean-card">
            <div class="clean-card-head" style="background:linear-gradient(90deg, #5E2750, #9E3B67);">
                <span>Algorithm: Randomized Three-Way Quick Sort</span>
                <span class="pill-tag">Divide &amp; Conquer</span>
            </div>
            <div class="clean-card-body">
                <p style="margin-top:0;">
                    Standard two-way Quick Sort degrades to <b>O(n&sup2;)</b> on pre-sorted arrays or datasets with many duplicate values.
                    <b>Randomized Three-Way Quick Sort</b> solves both bottlenecks using three pointers (<code>lt</code>, <code>i</code>, <code>gt</code>):
                </p>
                <ul style="margin-bottom:0;">
                    <li><b>1. Randomized Pivot Selection:</b> Picks a random pivot index in <code>[low, high]</code> so sorted or reverse-sorted inputs cannot trigger worst-case recursion depth.</li>
                    <li><b>2. Three-Way Partitioning:</b> Organizes elements into <code>arr[low .. lt-1] &lt; pivot</code>, <code>arr[lt .. gt] == pivot</code>, and <code>arr[gt+1 .. high] &gt; pivot</code> in a single linear pass.</li>
                    <li><b>3. Duplicate Exclusion:</b> Recursively sorts only the strictly smaller and strictly greater partitions—skipping all <code>== pivot</code> elements permanently.</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, code_btn_col, _ = st.columns([1.2, 1.6, 1.2])
    with code_btn_col:
        btn_label = (
            "Hide Python Code ▲"
            if st.session_state["show_code_panel"]
            else "Show Python Implementation Code ▼"
        )
        if st.button(btn_label, type="secondary", use_container_width=True, key="toggle_code_card_btn"):
            st.session_state["show_code_panel"] = not st.session_state["show_code_panel"]
            st.rerun()

    if st.session_state["show_code_panel"]:
        st.code(
            """import random

def three_way_quicksort(arr, low, high):
    if low >= high:
        return

    # 1. Randomized pivot prevents O(n^2) on sorted inputs
    rand_idx = random.randint(low, high)
    arr[low], arr[rand_idx] = arr[rand_idx], arr[low]
    pivot = arr[low]

    # 2. Three-way partitioning around pivot
    lt = low       # boundary for elements < pivot
    i = low + 1    # current scanning pointer
    gt = high      # boundary for elements > pivot

    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1

    # 3. Recursively sort left (< pivot) and right (> pivot) partitions
    three_way_quicksort(arr, low, lt - 1)
    three_way_quicksort(arr, gt + 1, high)""",
            language="python",
        )

with tab_complexity:
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown(
            """
            <div class="clean-card">
                <div class="clean-card-head" style="background:linear-gradient(90deg, #5E2750, #8E3563);">
                    <span>Best Case</span>
                    <span class="pill-tag">&Theta;(n log n)</span>
                </div>
                <div class="clean-card-body">
                    Every pivot splits the subarray into two equal halves (<code>n/2</code> and <code>n/2</code>).
                    Recursion depth is <code>log₂(n)</code> with <code>O(n)</code> work per level and <code>O(log n)</code> stack space.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="clean-card">
                <div class="clean-card-head" style="background:linear-gradient(90deg, #E94E65, #F36870);">
                    <span>Average Case</span>
                    <span class="pill-tag">&Theta;(n log n)</span>
                </div>
                <div class="clean-card-body">
                    Random pivot selection guarantees logarithmic expected recursion depth even under uneven splits,
                    averaging <code>~1.39 n log₂(n)</code> comparisons in practice.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="clean-card">
                <div class="clean-card-head" style="background:linear-gradient(90deg, #F77965, #FFA07A);">
                    <span>Worst Case</span>
                    <span class="pill-tag">O(n&sup2;)</span>
                </div>
                <div class="clean-card-body">
                    Occurs if the minimum or maximum element is repeatedly chosen as the pivot (<code>n-1</code> and <code>0</code> splits).
                    Randomization + 3-way partitioning prevents this on sorted and duplicate-heavy arrays.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    n_vals = [10, 25, 50, 100, 200, 350, 500]
    growth_df = pd.DataFrame({
        "Input Size (n)": n_vals,
        "Best Case ~ n log₂(n)": [round(n * math.log2(n)) for n in n_vals],
        "Average Case ~ 1.39 n log₂(n)": [round(1.39 * n * math.log2(n)) for n in n_vals],
        "Worst Case ~ n(n - 1)/2": [round(n * (n - 1) / 2) for n in n_vals],
    })
    fig_growth = px.line(
        growth_df,
        x="Input Size (n)",
        y=["Best Case ~ n log₂(n)", "Average Case ~ 1.39 n log₂(n)", "Worst Case ~ n(n - 1)/2"],
        markers=True,
        color_discrete_sequence=["#5E2750", "#E94E65", "#FFA07A"],
        title="Asymptotic Operation Growth Across Input Sizes (n = 10 to 500)",
    )
    fig_growth.update_layout(**PLOT_LAYOUT, height=320, yaxis_title="Operations", legend_title="Complexity Bound")
    st.plotly_chart(fig_growth, use_container_width=True, config={"displayModeBar": False})

with tab_realworld:
    rw_left, rw_right = st.columns(2, gap="large")

    with rw_left:
        st.markdown(
            """
            <div class="clean-card">
                <div class="clean-card-head" style="background:linear-gradient(90deg, #5E2750, #8E3563);">
                    <span>1. E-Commerce Product Catalog Sorter</span>
                    <span class="pill-tag">Java / SQL ORDER BY</span>
                </div>
                <div class="clean-card-body" style="padding-bottom:0.6rem;">
                    Used in storefront search engines and SQL <code>ORDER BY</code> buffers (PostgreSQL <code>work_mem</code>).
                    Duplicate prices ($25, $85) are grouped in O(n) via 3-way partitioning.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        catalog_items = [
            {"Product": "USB-C Hub", "Price ($)": 25, "Rating": 4.2},
            {"Product": "4K Monitor", "Price ($)": 320, "Rating": 4.8},
            {"Product": "Mech Keyboard", "Price ($)": 85, "Rating": 4.7},
            {"Product": "Wireless Mouse", "Price ($)": 45, "Rating": 4.4},
            {"Product": "Desk Mat", "Price ($)": 25, "Rating": 4.1},
            {"Product": "NVMe SSD 1TB", "Price ($)": 110, "Rating": 4.9},
            {"Product": "Webcam HD", "Price ($)": 85, "Rating": 4.3},
        ]

        ec1, ec2 = st.columns(2)
        ec_key = ec1.selectbox("Sort Key", ["Price ($)", "Rating"], key="ec_key")
        ec_ord = ec2.selectbox("Direction", ["Ascending", "Descending"], key="ec_ord")

        sorted_ec, ec_stats = quick_sort(catalog_items, key=ec_key, ascending=(ec_ord == "Ascending"))
        st.dataframe(pd.DataFrame(sorted_ec), use_container_width=True, hide_index=True)
        st.caption(f"Sorted {len(sorted_ec)} records in {ec_stats['comparisons']} comparisons & {ec_stats['swaps']} swaps.")

        if st.button("Visualize Product Values in Chart ↑", key="load_ec_btn", use_container_width=True):
            vals_str = ", ".join(str(x[ec_key]) for x in catalog_items)
            st.session_state["qs_custom_input"] = vals_str
            st.session_state["qs_direction"] = ec_ord
            rec_list = [{"index": idx, "value": float(x[ec_key])} for idx, x in enumerate(catalog_items)]
            trigger_sort_run(rec_list, ec_ord)
            st.rerun()

    with rw_right:
        st.markdown(
            """
            <div class="clean-card">
                <div class="clean-card-head" style="background:linear-gradient(90deg, #E94E65, #FF8C69);">
                    <span>2. OS CPU Task & Process Scheduler</span>
                    <span class="pill-tag">C++ std::sort / Introsort</span>
                </div>
                <div class="clean-card-body" style="padding-bottom:0.6rem;">
                    Used in OS schedulers and C++/Rust standard libraries (Introsort) to order ready-queue tasks
                    in-place with O(log n) auxiliary stack memory.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        os_processes = [
            {"PID": "PID-104", "Process": "Video Encoder", "Burst (ms)": 95, "Priority": 3},
            {"PID": "PID-108", "Process": "Auth Daemon", "Burst (ms)": 15, "Priority": 1},
            {"PID": "PID-112", "Process": "Log Compactor", "Burst (ms)": 60, "Priority": 4},
            {"PID": "PID-119", "Process": "Packet Filter", "Burst (ms)": 15, "Priority": 1},
            {"PID": "PID-123", "Process": "Cache Flush", "Burst (ms)": 35, "Priority": 2},
            {"PID": "PID-127", "Process": "Index Builder", "Burst (ms)": 80, "Priority": 3},
            {"PID": "PID-131", "Process": "Health Probe", "Burst (ms)": 10, "Priority": 2},
        ]

        os1, os2 = st.columns(2)
        os_key = os1.selectbox("Schedule By", ["Burst (ms)", "Priority"], key="os_key")
        os_ord = os2.selectbox("Queue Order", ["Ascending", "Descending"], key="os_ord")

        sorted_os, os_stats = quick_sort(os_processes, key=os_key, ascending=(os_ord == "Ascending"))
        st.dataframe(pd.DataFrame(sorted_os), use_container_width=True, hide_index=True)
        st.caption(f"Scheduled {len(sorted_os)} processes in {os_stats['comparisons']} comparisons & {os_stats['swaps']} swaps.")

        if st.button("Visualize CPU Queue in Chart ↑", key="load_os_btn", use_container_width=True):
            vals_str = ", ".join(str(x[os_key]) for x in os_processes)
            st.session_state["qs_custom_input"] = vals_str
            st.session_state["qs_direction"] = os_ord
            rec_list = [{"index": idx, "value": float(x[os_key])} for idx, x in enumerate(os_processes)]
            trigger_sort_run(rec_list, os_ord)
            st.rerun()