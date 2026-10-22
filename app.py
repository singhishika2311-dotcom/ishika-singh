import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
import streamlit.components.v1 as components
from matplotlib.colors import LinearSegmentedColormap

st.set_page_config(page_title="Social Media Screen Time & Mental Health", page_icon="📱", layout="wide")

# ============================================================
# Colours — soft, calm palette (validated colour-blind safe on white)
# ============================================================
INK, INK_2, MUTED, GRID = "#2b3044", "#5a6178", "#8b91a7", "#eceff5"
PERI, TEAL, SAND, ROSE, SAGE, LAVENDER, CORAL, SKY = (
    "#5b7fde", "#00897b", "#e0a030", "#d6728f", "#6a994e", "#9b7fd1", "#e07a5f", "#4cb3d4")
PALETTE = [PERI, TEAL, SAND, ROSE, SAGE, LAVENDER, CORAL, SKY]
PERI_RAMP = ["#e3e9fb", "#b9c8f3", "#8ea6ea", "#5b7fde", "#3a5bbf"]
BAND_COLORS = {"Low": "#e76f6f", "Moderate": "#f2b84b", "High": "#3fb68b"}
YES_NO = {"Yes": LAVENDER, "No": TEAL}

pio.templates["calm"] = go.layout.Template(pio.templates["plotly_white"])
pio.templates["calm"].layout.update(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", colorway=PALETTE, height=360,
    font=dict(family="Poppins, system-ui, sans-serif", color=INK_2, size=12),
    xaxis=dict(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID, tickfont_color=MUTED, title_font_color=INK_2),
    yaxis=dict(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID, tickfont_color=MUTED, title_font_color=INK_2),
    legend=dict(orientation="h", y=-0.2, x=0, title_font_color=MUTED),
    hoverlabel=dict(bgcolor="white", bordercolor=PERI, font=dict(color=INK, family="Poppins")),
    margin=dict(l=10, r=45, t=10, b=10), barcornerradius=6, bargap=0.28,
)
px.defaults.template = "calm"
px.defaults.color_discrete_sequence = PALETTE
CHART_CFG = {"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d"]}

# ============================================================
# Styles & animations
# ============================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,500,1,0');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
html, body, .stMarkdown, .stTabs, p, label {{ font-family: 'Poppins', system-ui, sans-serif; }}
.mi {{ font-family: 'Material Symbols Rounded'; font-weight: normal; font-style: normal; line-height: 1;
      display: inline-block; vertical-align: middle; font-feature-settings: 'liga'; -webkit-font-smoothing: antialiased; }}

@keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes drift  {{ 0%,100% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} }}
@keyframes bob    {{ 0%,100% {{ transform: translateY(0) rotate(-4deg); }} 50% {{ transform: translateY(-10px) rotate(4deg); }} }}
@keyframes pulse  {{ 0% {{ box-shadow: 0 0 0 0 rgba(63,182,139,.55); }} 100% {{ box-shadow: 0 0 0 10px rgba(63,182,139,0); }} }}
@keyframes grow   {{ from {{ width: 0; }} }}

.stApp {{
    background:
      radial-gradient(700px 400px at 0% 0%, rgba(91,127,222,.10), transparent 60%),
      radial-gradient(700px 400px at 100% 0%, rgba(0,137,123,.08), transparent 60%),
      radial-gradient(800px 500px at 50% 100%, rgba(155,127,209,.08), transparent 60%), #f6f7fb;
}}
.block-container {{ padding-top: 2rem; max-width: 1380px; }}
header[data-testid="stHeader"] {{ background: transparent; }}

/* ---------- Hero ---------- */
.hero {{
    position: relative; overflow: hidden; border-radius: 28px; padding: 2.3rem 2.6rem;
    background: linear-gradient(120deg, #e8edfc, #e3f4f1, #efe9fa, #e8f4fb);
    background-size: 300% 300%; animation: drift 16s ease infinite, fadeUp .7s ease backwards;
    border: 1px solid #e1e6f3; box-shadow: 0 18px 40px -20px rgba(91,127,222,.35); margin-bottom: 1.5rem;
    display: flex; align-items: center; justify-content: space-between; gap: 2rem;
}}
.hero .tag {{
    display: inline-flex; align-items: center; gap: .45rem; padding: .35rem .85rem; border-radius: 999px;
    font-size: .75rem; font-weight: 600; letter-spacing: .07em; text-transform: uppercase;
    color: {PERI}; background: white; box-shadow: 0 4px 12px rgba(91,127,222,.12);
}}
.hero .dot {{ width: 8px; height: 8px; border-radius: 50%; background: #3fb68b; animation: pulse 1.8s infinite; }}
.hero h1 {{
    margin: .8rem 0 .4rem; font-size: 2.6rem; font-weight: 800; line-height: 1.15; padding: 0;
    background: linear-gradient(90deg, #3a5bbf, {PERI} 45%, {TEAL});
    -webkit-background-clip: text; background-clip: text; color: transparent;
}}
.hero p {{ color: {INK_2}; font-size: 1.02rem; margin: 0; max-width: 680px; }}
.hero-art {{ font-size: 7.5rem; color: {PERI}; opacity: .85; animation: bob 5s ease-in-out infinite; }}
.chips {{ display: flex; gap: .6rem; flex-wrap: wrap; margin-top: 1.3rem; }}
.chip {{
    display: inline-flex; align-items: center; gap: .4rem; padding: .45rem .9rem; border-radius: 12px;
    font-size: .86rem; color: {INK_2}; background: rgba(255,255,255,.75); border: 1px solid #e1e6f3;
    transition: transform .2s ease, box-shadow .2s ease;
}}
.chip:hover {{ transform: translateY(-2px); box-shadow: 0 6px 14px rgba(91,127,222,.15); }}
.chip .mi {{ font-size: 1.1rem; color: {PERI}; }}
.chip b {{ color: {INK}; }}

/* ---------- KPI cards ---------- */
.kpi {{
    background: white; border-radius: 20px; padding: 1.1rem 1.2rem; height: 100%;
    border: 1px solid #e8ebf3; box-shadow: 0 6px 18px -10px rgba(43,48,68,.15);
    animation: fadeUp .6s ease backwards; transition: transform .25s ease, box-shadow .25s ease;
}}
.kpi:hover {{ transform: translateY(-5px); box-shadow: 0 16px 30px -14px var(--c); }}
.kpi .icon {{
    width: 44px; height: 44px; border-radius: 14px; display: grid; place-items: center;
    background: color-mix(in srgb, var(--c) 14%, white); color: var(--c); transition: transform .3s ease;
}}
.kpi:hover .icon {{ transform: scale(1.12) rotate(-8deg); }}
.kpi .icon .mi {{ font-size: 1.5rem; }}
.kpi .label {{ color: {MUTED}; font-size: .78rem; margin-top: .75rem; font-weight: 500; }}
.kpi .value {{ font-size: 1.75rem; font-weight: 700; color: {INK}; line-height: 1.25; }}
.kpi .hint {{ font-size: .76rem; color: {MUTED}; display: flex; align-items: center; gap: .2rem; }}
.kpi .bar {{ height: 5px; border-radius: 99px; background: {GRID}; margin-top: .65rem; overflow: hidden; }}
.kpi .bar span {{ display: block; height: 100%; border-radius: 99px; background: var(--c); animation: grow 1.2s ease both; }}

/* ---------- Section headers ---------- */
.section {{ display: flex; align-items: center; gap: .8rem; margin: 1.4rem 0 .8rem; animation: fadeUp .6s ease backwards; }}
.section .badge {{
    width: 42px; height: 42px; border-radius: 13px; display: grid; place-items: center; color: white;
    background: linear-gradient(135deg, {PERI}, {TEAL}); box-shadow: 0 8px 18px -8px {PERI};
}}
.section h3 {{ margin: 0; padding: 0; font-size: 1.25rem; font-weight: 700; color: {INK}; }}
.section p {{ margin: 0; color: {MUTED}; font-size: .88rem; }}

/* ---------- Insight cards ---------- */
.insights {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; }}
.insight {{
    background: white; border-radius: 18px; padding: 1.1rem 1.2rem; border: 1px solid #e8ebf3;
    color: {INK_2}; font-size: .9rem; animation: fadeUp .6s ease backwards;
    transition: transform .25s ease, box-shadow .25s ease;
}}
.insight:hover {{ transform: translateY(-4px); box-shadow: 0 14px 28px -14px rgba(91,127,222,.4); }}
.insight .mi {{ font-size: 1.6rem; color: var(--c); }}
.insight .big {{ display: block; font-size: 1.45rem; font-weight: 700; color: {INK}; margin: .35rem 0 .15rem; }}

/* ---------- Chart cards (bordered containers with key "card_*") ---------- */
div[class*="st-key-card"] {{
    background: white; border-radius: 20px !important; border: 1px solid #e8ebf3 !important;
    box-shadow: 0 6px 20px -12px rgba(43,48,68,.18); animation: fadeUp .6s ease backwards;
    transition: transform .25s ease, box-shadow .25s ease;
}}
/* no transform on hover: a transformed parent would trap the chart's fullscreen view inside the card */
div[class*="st-key-card"]:hover {{ border-color: #cdd7f5 !important; box-shadow: 0 18px 34px -18px rgba(91,127,222,.45); }}
div[class*="st-key-anim"] {{ display: none; }}
.card-head {{ display: flex; align-items: center; gap: .65rem; }}
.card-head .ic {{
    width: 36px; height: 36px; border-radius: 11px; display: grid; place-items: center;
    background: color-mix(in srgb, var(--c) 14%, white); color: var(--c);
}}
.card-head .ic .mi {{ font-size: 1.25rem; }}
.card-head .t {{ font-weight: 600; color: {INK}; font-size: .98rem; }}
.card-head .s {{ color: {MUTED}; font-size: .78rem; }}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {{
    gap: .35rem; background: white; padding: .4rem; border-radius: 16px; border: 1px solid #e8ebf3;
    box-shadow: 0 6px 18px -12px rgba(43,48,68,.2); flex-wrap: wrap;
}}
.stTabs [data-baseweb="tab"] {{
    height: auto; padding: .55rem 1.1rem; border-radius: 12px; color: {INK_2};
    transition: background .25s ease, color .25s ease, transform .2s ease;
}}
.stTabs [data-baseweb="tab"]:not([aria-selected="true"]):hover {{ background: #eef1fa; transform: translateY(-1px); }}
.stTabs [data-baseweb="tab"] p {{ font-weight: 600; }}
.stTabs [aria-selected="true"] {{ background: linear-gradient(135deg, {PERI}, #7b95e6); box-shadow: 0 8px 18px -8px {PERI}; }}
.stTabs [aria-selected="true"] p, .stTabs [aria-selected="true"] span {{ color: white !important; }}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {{ display: none; }}
.stTabs [data-baseweb="tab-panel"] {{ animation: fadeUp .45s ease backwards; }}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {{ background: #ffffff; border-right: 1px solid #e8ebf3; }}
section[data-testid="stSidebar"] .block-container, section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{ padding-top: .5rem; }}
.brand {{ display: flex; align-items: center; gap: .7rem; padding: .2rem 0 1rem; border-bottom: 1px solid #eef0f5; margin-bottom: 1rem; }}
.brand .logo {{
    width: 40px; height: 40px; border-radius: 12px; display: grid; place-items: center; color: white;
    background: linear-gradient(135deg, {PERI}, {TEAL}); box-shadow: 0 8px 16px -8px {PERI};
}}
.brand .name {{ font-weight: 700; color: {INK}; font-size: 1rem; line-height: 1.2; }}
.brand .sub {{ color: {MUTED}; font-size: .75rem; }}
.side-count {{
    border-radius: 16px; padding: .9rem 1rem; margin-bottom: 1.1rem; color: white;
    background: linear-gradient(135deg, {PERI}, {TEAL}); box-shadow: 0 12px 24px -14px {PERI};
}}
.side-count .row {{ display: flex; align-items: baseline; justify-content: space-between; }}
.side-count .n {{ font-size: 1.7rem; font-weight: 800; }}
.side-count .pct {{ font-size: .8rem; font-weight: 600; background: rgba(255,255,255,.2); padding: .15rem .55rem; border-radius: 99px; }}
.side-count .t {{ font-size: .78rem; opacity: .9; }}
.side-count .meter {{ height: 6px; border-radius: 99px; background: rgba(255,255,255,.25); margin-top: .6rem; overflow: hidden; }}
.side-count .meter span {{ display: block; height: 100%; background: white; border-radius: 99px; transition: width .6s ease; }}
.side-title {{ font-weight: 700; color: {INK}; font-size: .95rem; display: flex; align-items: center; gap: .4rem; }}
.side-title .mi {{ color: {PERI}; font-size: 1.15rem; }}
.side-title .badge {{ white-space: nowrap; background: #e8edfc; color: {PERI}; font-size: .7rem; padding: .1rem .5rem; border-radius: 99px; }}
section[data-testid="stSidebar"] .stButton button {{ white-space: nowrap; padding: 0; }}
section[data-testid="stSidebar"] .stButton {{ display: flex; justify-content: flex-end; }}
.side-hint {{ color: {MUTED}; font-size: .76rem; margin: .1rem 0 .6rem; }}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
    font-size: .72rem; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: {MUTED};
}}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] [data-testid="stIconMaterial"] {{ color: {PERI}; }}
section[data-testid="stSidebar"] .stElementContainer {{ margin-bottom: .15rem; }}
/* Filter chips */
button[data-testid="stBaseButton-pills"], button[data-testid="stBaseButton-pillsActive"] {{
    border-radius: 99px; font-size: .8rem; padding: .2rem .75rem; min-height: 0;
    transition: all .2s ease;
}}
button[data-testid="stBaseButton-pills"] {{ background: white; border: 1px solid #e1e6f0; color: {INK_2}; }}
button[data-testid="stBaseButton-pills"]:hover {{ border-color: {PERI}; color: {PERI}; background: #f5f7fe; }}
button[data-testid="stBaseButton-pillsActive"] {{
    background: #e8edfc; border: 1px solid {PERI}; color: #34449a; font-weight: 600;
}}
.side-foot {{ color: {MUTED}; font-size: .74rem; border-top: 1px solid #eef0f5; padding-top: .8rem; margin-top: 1rem; display: flex; gap: .4rem; }}
.side-foot .mi {{ font-size: 1rem; }}

/* ---------- Buttons ---------- */
.stDownloadButton button {{ border-radius: 12px; transition: transform .2s ease, box-shadow .2s ease; }}
.stDownloadButton button:hover {{ transform: translateY(-2px); box-shadow: 0 10px 20px -10px {PERI}; }}

.footer {{ text-align: center; color: {MUTED}; margin: 2.5rem 0 1rem; font-size: .88rem; }}
.footer .mi {{ color: {ROSE}; font-size: 1.1rem; }}

@media (prefers-reduced-motion: reduce) {{ *, *::before, *::after {{ animation: none !important; transition: none !important; }} }}
@media (max-width: 900px) {{ .hero-art {{ display: none; }} .hero h1 {{ font-size: 2rem; }} }}
</style>
""", unsafe_allow_html=True)


# ============================================================
# UI helpers
# ============================================================
def mi(name):
    return f'<span class="mi">{name}</span>'


def html(markup, where=st):
    where.markdown(markup, unsafe_allow_html=True)


def section(icon, title, subtitle):
    html(f'<div class="section"><div class="badge">{mi(icon)}</div>'
         f'<div><h3>{title}</h3><p>{subtitle}</p></div></div>')


_card_n = 0


def chart(where, icon, title, subtitle, fig, color=PERI):
    """A white animated card with an icon header and the plotly chart inside."""
    global _card_n
    _card_n += 1
    with where.container(border=True, key=f"card_{_card_n}"):
        html(f'<div class="card-head" style="--c:{color}"><div class="ic">{mi(icon)}</div>'
             f'<div><div class="t">{title}</div><div class="s">{subtitle}</div></div></div>')
        if isinstance(fig, plt.Figure):
            st.pyplot(fig)
        else:
            st.plotly_chart(fig.update_layout(paper_bgcolor="white", plot_bgcolor="white"),
                            config=CHART_CFG, theme=None)


def gaps(fig, width=1.5):
    """Thin white outlines so neighbouring colours never touch."""
    return fig.update_traces(marker_line_color="white", marker_line_width=width)


# ============================================================
# Data
# ============================================================
@st.cache_data
def load_data():
    return pd.read_csv("social_media_screentime_mental_health_2026.csv")


try:
    df = load_data()
except FileNotFoundError:
    st.error("Dataset not found. Put `social_media_screentime_mental_health_2026.csv` next to app.py "
             "(or run `python make_sample_data.py` to create a sample).", icon=":material/error:")
    st.stop()

BAND_ORDER = [b for b in ["Low", "Moderate", "High"] if b in df["wellbeing_band"].unique()] or None
# Fixed colour per platform, so filtering never repaints the remaining ones
PLATFORM_COLORS = dict(zip(sorted(df.most_used_platform.unique()), PALETTE))

# ============================================================
# Sidebar filters
# ============================================================
FILTERS = [  # column, label shown above the chips
    ("occupation", ":material/work: Occupation"),
    ("region", ":material/public: Region"),
    ("gender", ":material/wc: Gender"),
    ("most_used_platform", ":material/smartphone: Most used platform"),
]
AGE_MIN, AGE_MAX = int(df.age.min()), int(df.age.max())


OPTIONS = {col: sorted(df[col].dropna().unique()) for col, _ in FILTERS}
DEFAULTS = {f"f_{col}": OPTIONS[col] for col, _ in FILTERS} | {"f_age": (AGE_MIN, AGE_MAX)}
for k, v in DEFAULTS.items():  # everything selected by default, so the chips match the data shown
    st.session_state.setdefault(k, list(v) if isinstance(v, list) else v)


def reset_filters():
    for k, v in DEFAULTS.items():
        st.session_state[k] = list(v) if isinstance(v, list) else v


sb = st.sidebar
html(f'<div class="brand"><div class="logo">{mi("psychology")}</div>'
     f'<div><div class="name">Screen & Mind</div><div class="sub">Mental health analytics</div></div></div>', sb)
count_slot = sb.empty()  # filled after the filters are read

active = sum(sorted(st.session_state[k]) != sorted(v) if isinstance(v, list) else st.session_state[k] != v
             for k, v in DEFAULTS.items())
head, btn = sb.columns([5, 2], vertical_alignment="center")
html(f'<div class="side-title">{mi("tune")} Filters' + (f' <span class="badge">{active} active</span>' if active else "")
     + "</div>", head)
btn.button("Reset", icon=":material/restart_alt:", on_click=reset_filters, type="tertiary", disabled=not active)
html('<div class="side-hint">All groups are selected by default — tap a chip to remove or add it.</div>', sb)

mask = pd.Series(True, index=df.index)
for col, label in FILTERS:
    picked = sb.pills(label, OPTIONS[col], selection_mode="multi", key=f"f_{col}")
    mask &= df[col].isin(picked)
age_range = sb.slider(":material/cake: Age range", AGE_MIN, AGE_MAX, key="f_age")
f = df[mask & df.age.between(*age_range)]

html(f'<div class="side-count"><div class="row"><span class="n">{len(f):,}</span>'
     f'<span class="pct">{len(f) / len(df):.0%}</span></div><div class="t">participants in view</div>'
     f'<div class="meter"><span style="width:{len(f) / len(df):.0%}"></span></div></div>', count_slot)
html(f'<div class="side-foot">{mi("info")} Survey data · {len(df):,} participants · 2026</div>', sb)

# ============================================================
# Hero
# ============================================================
html(f"""
<div class="hero">
  <div>
    <span class="tag"><span class="dot"></span>Live analytics · 2026</span>
    <h1>Social Media Screen Time<br>& Mental Health</h1>
    <p>How do our scrolling habits shape sleep, self-esteem and life satisfaction?
       Pick filters on the left, then explore the tabs below.</p>
    <div class="chips">
      <span class="chip">{mi("groups")}<b>{len(df):,}</b> participants</span>
      <span class="chip">{mi("public")}<b>{df.region.nunique()}</b> regions</span>
      <span class="chip">{mi("apps")}<b>{df.most_used_platform.nunique()}</b> platforms</span>
      <span class="chip">{mi("work")}<b>{df.occupation.nunique()}</b> occupations</span>
    </div>
  </div>
  <div class="hero-art">{mi("self_improvement")}</div>
</div>
""")

if f.empty:
    st.info("No participants match these filters. Try selecting more options in the sidebar.", icon=":material/search_off:")
    st.stop()


# ============================================================
# KPI cards
# ============================================================
def vs_all(col, unit=""):
    d = f[col].mean() - df[col].mean()
    if abs(d) < 0.05:
        return f'{mi("drag_handle")} same as everyone'
    return f'{mi("arrow_upward" if d > 0 else "arrow_downward")} {abs(d):.1f}{unit} vs everyone'


KPIS = [  # icon, label, value, hint, colour, fill of the mini bar (0–1)
    ("schedule", "Daily screen time", f"{f.daily_screen_hours.mean():.1f} h", vs_all("daily_screen_hours", " h"), PERI,
     f.daily_screen_hours.mean() / 24),
    ("bedtime", "Average sleep", f"{f.avg_sleep_hours.mean():.1f} h", vs_all("avg_sleep_hours", " h"), LAVENDER,
     f.avg_sleep_hours.mean() / 10),
    ("notifications_active", "Notifications / day", f"{f.daily_notifications.mean():.0f}",
     vs_all("daily_notifications"), SAND, f.daily_notifications.mean() / df.daily_notifications.max()),
    ("apps", "Platforms used", f"{f.platforms_used_count.mean():.1f}", vs_all("platforms_used_count"), ROSE,
     f.platforms_used_count.mean() / df.platforms_used_count.max()),
    ("sentiment_satisfied", "Life satisfaction", f"{f.life_satisfaction_1to10.mean():.1f}/10",
     vs_all("life_satisfaction_1to10"), TEAL, f.life_satisfaction_1to10.mean() / 10),
    ("dark_mode", "Night-time users", f"{(f.night_time_use == 'Yes').mean():.0%}",
     f'{mi("nights_stay")} scroll after bedtime', SKY, (f.night_time_use == "Yes").mean()),
]
for i, (col, (icon, label, value, hint, color, fill)) in enumerate(zip(st.columns(6), KPIS)):
    html(f'<div class="kpi" style="--c:{color}; animation-delay:{i * 0.08}s">'
         f'<div class="icon">{mi(icon)}</div><div class="label">{label}</div><div class="value">{value}</div>'
         f'<div class="hint">{hint}</div><div class="bar"><span style="width:{min(fill, 1):.0%}"></span></div></div>', col)
st.write("")

# ============================================================
# Tabs
# ============================================================
t1, t2, t3, t4, t5, t6, t7 = st.tabs([
    ":material/dashboard: Overview", ":material/schedule: Screen & Sleep", ":material/psychology: Mental Health",
    ":material/smartphone: Platforms", ":material/query_stats: Deep Dive",
    ":material/person_search: Check Yourself", ":material/table_view: Data"])

# ---------------- Overview ----------------
with t1:
    section("lightbulb", "Key insights", "Plain-English takeaways for the people you've selected")
    heavy, light = f[f.daily_screen_hours >= 8], f[f.daily_screen_hours < 4]
    corr = f.daily_screen_hours.corr(f.life_satisfaction_1to10)
    cards = [
        ("star", f.most_used_platform.mode()[0], "is the most-used platform", SAND),
        ("wb_twilight", f"{f.minutes_to_first_check_after_waking.median():.0f} min",
         "until the first phone check after waking (median)", ROSE),
        ("insights", f"{corr:+.2f}", "link between screen time and life satisfaction — " +
         ("more screen, less happy" if corr < -0.1 else "more screen, happier" if corr > 0.1 else "barely related"), TEAL),
    ]
    if len(heavy) and len(light):
        cards.insert(0, ("bedtime_off", f"{light.avg_sleep_hours.mean() - heavy.avg_sleep_hours.mean():.1f} h less sleep",
                         "for heavy users (8h+) than light users (&lt;4h)", LAVENDER))
    html('<div class="insights">' + "".join(
        f'<div class="insight" style="--c:{c}; animation-delay:{i * 0.08}s">{mi(ic)}<span class="big">{b}</span>{t}</div>'
        for i, (ic, b, t, c) in enumerate(cards)) + "</div>")

    section("diversity_3", "Who is in the data", "Wellbeing, regions, ages and jobs at a glance")
    c1, c2 = st.columns(2)
    fig = px.pie(f, names="wellbeing_band", hole=0.64, color="wellbeing_band", color_discrete_map=BAND_COLORS,
                 category_orders={"wellbeing_band": BAND_ORDER})
    fig.update_traces(marker_line_color="white", marker_line_width=4, textinfo="percent+label", textfont_color=INK,
                      textposition="outside", sort=False,
                      hovertemplate="%{label}: %{value} people (%{percent})<extra></extra>")
    fig.add_annotation(text=f"<b>{len(f):,}</b><br>people", showarrow=False, font=dict(size=18, color=INK))
    chart(c1, "psychology", "Wellbeing band split", "Share of people in each wellbeing level",
          fig.update_layout(showlegend=False), TEAL)

    reg = f.groupby("region", as_index=False).daily_screen_hours.mean().sort_values("daily_screen_hours")
    fig = px.bar(reg, x="daily_screen_hours", y="region", orientation="h", text_auto=".1f", color="daily_screen_hours",
                 color_continuous_scale=PERI_RAMP[1:], labels={"daily_screen_hours": "Hours / day", "region": ""})
    fig.update_traces(textfont_color=INK, textposition="outside", cliponaxis=False)
    chart(c2, "public", "Screen time by region", "Average hours per day", fig.update_coloraxes(showscale=False))

    c1, c2 = st.columns(2)
    fig = px.histogram(f, x="age", nbins=25, color_discrete_sequence=[LAVENDER], labels={"age": "Age"})
    chart(c1, "cake", "Age distribution", "How old our participants are",
          gaps(fig).update_layout(bargap=0.06, yaxis_title="People"), LAVENDER)
    occ_n = f.occupation.value_counts().reset_index()
    fig = px.pie(occ_n, names="occupation", values="count", hole=0.64)
    fig.update_traces(marker_line_color="white", marker_line_width=4, textfont_color="white",
                      hovertemplate="%{label}: %{value} people (%{percent})<extra></extra>")
    chart(c2, "work", "Participants by occupation", "Who took part", fig, SAND)

# ---------------- Screen time & sleep ----------------
with t2:
    section("schedule", "Screen time & sleep", "Does scrolling eat into our rest?")
    c1, c2 = st.columns(2)
    fig = px.scatter(f, x="daily_screen_hours", y="avg_sleep_hours", color="night_time_use", trendline="ols",
                     opacity=0.55, color_discrete_map=YES_NO,
                     labels={"daily_screen_hours": "Screen hours / day", "avg_sleep_hours": "Sleep hours",
                             "night_time_use": "Night-time use"})
    fig.update_traces(marker=dict(size=8, line=dict(color="white", width=1)), selector=dict(mode="markers"))
    chart(c1, "bedtime", "More screen time, less sleep?", "Each dot is one person · lines show the trend", fig, LAVENDER)
    fig = px.scatter(f, x="daily_screen_hours", y="daily_notifications", color="wellbeing_band", opacity=0.6,
                     color_discrete_map=BAND_COLORS, category_orders={"wellbeing_band": BAND_ORDER},
                     labels={"daily_screen_hours": "Screen hours / day", "daily_notifications": "Notifications / day",
                             "wellbeing_band": "Wellbeing"})
    fig.update_traces(marker=dict(size=8, line=dict(color="white", width=1)))
    chart(c2, "notifications_active", "Screen time vs notifications", "Coloured by wellbeing level", fig, SAND)

    c1, c2 = st.columns(2)
    fig = px.violin(f, x="night_time_use", y="avg_sleep_hours", color="night_time_use", box=True,
                    color_discrete_map=YES_NO,
                    labels={"night_time_use": "Uses social media at night", "avg_sleep_hours": "Sleep hours"})
    chart(c1, "dark_mode", "Night-time scrolling & sleep", "Wider shape = more people at that value",
          fig.update_layout(showlegend=False), SKY)
    occ = f.groupby("occupation", as_index=False).daily_screen_hours.mean().sort_values("daily_screen_hours")
    fig = px.bar(occ, x="daily_screen_hours", y="occupation", orientation="h", text_auto=".1f",
                 color_discrete_sequence=[PERI], labels={"daily_screen_hours": "Hours / day", "occupation": ""})
    chart(c2, "work", "Screen time by occupation", "Average hours per day",
          fig.update_traces(textfont_color=INK, textposition="outside", cliponaxis=False))

    fig = px.density_heatmap(f, x="age", y="daily_screen_hours", nbinsx=24, nbinsy=16,
                             color_continuous_scale=["#ffffff"] + PERI_RAMP,
                             labels={"daily_screen_hours": "Screen hours / day", "age": "Age"})
    chart(st, "local_fire_department", "Where do people cluster?", "Darker = more people of that age & screen time",
          fig.update_coloraxes(colorbar_title="People"), CORAL)

# ---------------- Mental health ----------------
with t3:
    section("psychology", "Mental health", "Wellbeing, self-esteem and life satisfaction")
    c1, c2 = st.columns(2)
    band = f.groupby("wellbeing_band", as_index=False)[["daily_screen_hours", "avg_sleep_hours"]].mean()
    band = band.melt("wellbeing_band", var_name="metric", value_name="hours")
    band["metric"] = band.metric.map({"daily_screen_hours": "Screen time", "avg_sleep_hours": "Sleep"})
    fig = px.bar(band, x="wellbeing_band", y="hours", color="metric", barmode="group", text_auto=".1f",
                 category_orders={"wellbeing_band": BAND_ORDER}, color_discrete_sequence=[PERI, LAVENDER],
                 labels={"wellbeing_band": "Wellbeing band", "hours": "Hours", "metric": ""})
    chart(c1, "balance", "Screen time & sleep per wellbeing level", "Average hours",
          gaps(fig).update_traces(textfont_color="white"), PERI)
    fig = px.box(f, x="primary_purpose", y="self_esteem_1to10", points=False, color_discrete_sequence=[ROSE],
                 labels={"primary_purpose": "", "self_esteem_1to10": "Self-esteem (1–10)"})
    chart(c2, "favorite", "Self-esteem by reason for use", "Why people open social media", fig, ROSE)

    c1, c2 = st.columns(2)
    det = f.groupby("attempted_digital_detox", as_index=False)[["life_satisfaction_1to10", "self_esteem_1to10"]].mean()
    det = det.melt("attempted_digital_detox", var_name="metric", value_name="score")
    det["metric"] = det.metric.map({"life_satisfaction_1to10": "Life satisfaction", "self_esteem_1to10": "Self-esteem"})
    fig = px.bar(det, x="attempted_digital_detox", y="score", color="metric", barmode="group", text_auto=".1f",
                 range_y=[0, 10], color_discrete_sequence=[TEAL, ROSE],
                 labels={"attempted_digital_detox": "Tried a digital detox", "score": "Average score (1–10)", "metric": ""})
    chart(c1, "spa", "Does a digital detox help?", "Average scores out of 10",
          gaps(fig).update_traces(textfont_color="white"), TEAL)
    fig = px.histogram(f, x="life_satisfaction_1to10", color="wellbeing_band", barmode="stack",
                       color_discrete_map=BAND_COLORS, category_orders={"wellbeing_band": BAND_ORDER},
                       labels={"life_satisfaction_1to10": "Life satisfaction (1–10)", "wellbeing_band": "Wellbeing"})
    chart(c2, "sentiment_satisfied", "Life satisfaction scores", "How many people gave each score",
          gaps(fig, 2).update_layout(bargap=0.12, yaxis_title="People"), SAND)

    corr_m = f.select_dtypes("number").corr()
    labels = [c.replace("_1to10", "").replace("minutes_to_first_check_after_waking", "first check (min)")
              .replace("_", " ") for c in corr_m.columns]
    fig, ax = plt.subplots(figsize=(11, 5.5))
    im = ax.imshow(corr_m, cmap=LinearSegmentedColormap.from_list("div", [CORAL, "#f3f4f8", PERI]), vmin=-1, vmax=1)
    ax.set_xticks(range(len(labels)), labels, rotation=35, ha="right", fontsize=9, color=INK_2)
    ax.set_yticks(range(len(labels)), labels, fontsize=9, color=INK_2)
    for i in range(len(labels)):
        for j in range(len(labels)):
            v = corr_m.iat[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8, color="white" if abs(v) > 0.55 else INK)
    cb = fig.colorbar(im, ax=ax, shrink=0.8)
    cb.outline.set_visible(False)
    cb.ax.tick_params(colors=MUTED, length=0)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.tight_layout()
    chart(st, "hub", "How everything is connected",
          "Blue = rise together · Coral = one goes up, the other goes down · Pale = unrelated", fig, PERI)

# ---------------- Platforms & habits ----------------
with t4:
    section("smartphone", "Platforms & habits", "Which apps win, where, and why")
    c1, c2 = st.columns(2)
    plat = f.most_used_platform.value_counts().reset_index()
    fig = px.bar(plat, x="count", y="most_used_platform", orientation="h", text_auto=True, color="most_used_platform",
                 color_discrete_map=PLATFORM_COLORS, labels={"most_used_platform": "", "count": "Participants"})
    fig.update_traces(textfont_color=INK, textposition="outside", cliponaxis=False)
    chart(c1, "emoji_events", "Most popular platforms", "Number of people who use it most",
          fig.update_layout(showlegend=False, yaxis={"categoryorder": "total ascending"}), SAND)
    fig = px.histogram(f, x="region", color="most_used_platform", barnorm="percent", color_discrete_map=PLATFORM_COLORS,
                       labels={"region": "", "most_used_platform": "Platform"})
    chart(c2, "public", "Platform share within each region", "Each bar adds up to 100%",
          gaps(fig).update_layout(yaxis_title="% of participants", barcornerradius=0))

    c1, c2 = st.columns(2)
    fig = px.box(f, x="most_used_platform", y="age", color="most_used_platform", points=False,
                 color_discrete_map=PLATFORM_COLORS, labels={"most_used_platform": "", "age": "Age"})
    chart(c1, "cake", "Age profile of each platform", "Middle line = typical age",
          fig.update_layout(showlegend=False), LAVENDER)
    fig = px.sunburst(f, path=["primary_purpose", "most_used_platform"], color_discrete_sequence=PALETTE)
    chart(c2, "target", "Why people use each platform", "Click a slice to zoom in",
          fig.update_traces(marker_line_color="white", marker_line_width=2, insidetextfont_color="white"), ROSE)

    c1, c2 = st.columns(2)
    fig = px.box(f, x="night_time_use", y="minutes_to_first_check_after_waking", color="night_time_use", points=False,
                 color_discrete_map=YES_NO,
                 labels={"night_time_use": "Uses social media at night", "minutes_to_first_check_after_waking": "Minutes"})
    chart(c1, "wb_twilight", "First phone check after waking", "Minutes from waking up",
          fig.update_layout(showlegend=False), SKY)
    cnt = f.groupby("platforms_used_count", as_index=False).daily_screen_hours.mean()
    fig = px.area(cnt, x="platforms_used_count", y="daily_screen_hours", markers=True, color_discrete_sequence=[PERI],
                  labels={"platforms_used_count": "Number of platforms used", "daily_screen_hours": "Avg screen hours / day"})
    fig.update_traces(line=dict(width=2.5, shape="spline"), marker=dict(size=9, line=dict(color="white", width=2)),
                      fillcolor="rgba(91,127,222,.15)")
    chart(c2, "trending_up", "More apps, more screen time?", "Average screen time by number of platforms", fig)

# ---------------- Deep dive ----------------
SCREEN_BINS, SCREEN_LABELS = [0, 3, 6, 9, 25], ["Light (<3h)", "Moderate (3–6h)", "Heavy (6–9h)", "Extreme (9h+)"]
SLEEP_BINS, SLEEP_LABELS = [0, 6, 7, 8, 25], ["<6h", "6–7h", "7–8h", "8h+"]
AGE_BINS, AGE_LABELS = [0, 18, 25, 35, 45, 120], ["13–17", "18–24", "25–34", "35–44", "45+"]
GROUP_COLORS = ["#b9c8f3", "#8ea6ea", "#5b7fde", "#3a5bbf"]  # one hue, light → dark = more screen time

with t5:
    g = f.assign(screen_group=pd.cut(f.daily_screen_hours, SCREEN_BINS, labels=SCREEN_LABELS, right=False),
                 sleep_group=pd.cut(f.avg_sleep_hours, SLEEP_BINS, labels=SLEEP_LABELS, right=False),
                 age_group=pd.cut(f.age, AGE_BINS, labels=AGE_LABELS, right=False))

    section("stairs", "The screen-time ladder", "What changes as daily screen time climbs?")
    ladder = g.groupby("screen_group", observed=True).agg(
        people=("age", "size"), sleep=("avg_sleep_hours", "mean"), life=("life_satisfaction_1to10", "mean"),
        esteem=("self_esteem_1to10", "mean")).reset_index()
    html('<div class="insights">' + "".join(
        f'<div class="insight" style="--c:{GROUP_COLORS[i]}; animation-delay:{i * 0.08}s">{mi("smartphone")}'
        f'<span class="big">{r.life:.1f}<small style="font-size:.9rem;color:{MUTED}">/10</small></span>'
        f'<b style="color:{INK}">{r.screen_group}</b><br>{r.people:,} people · sleep {r.sleep:.1f} h</div>'
        for i, r in enumerate(ladder.itertuples())) + "</div>")
    st.write("")
    long = ladder.melt("screen_group", ["sleep", "life", "esteem"], var_name="metric", value_name="value")
    long["metric"] = long.metric.map({"sleep": "Sleep (hours)", "life": "Life satisfaction", "esteem": "Self-esteem"})
    fig = px.bar(long, x="screen_group", y="value", color="screen_group", facet_col="metric", text_auto=".1f",
                 color_discrete_sequence=GROUP_COLORS, labels={"screen_group": "", "value": ""})
    fig.for_each_annotation(lambda a: a.update(text=f"<b>{a.text.split('=')[-1]}</b>", font_color=INK))
    fig.update_yaxes(matches=None, showticklabels=True).update_xaxes(tickangle=-25)
    chart(st, "trending_down", "Sleep & mood by screen-time group",
          "Each panel has its own scale · darker bars = more screen time",
          gaps(fig).update_traces(textfont_color="white").update_layout(showlegend=False, height=420,
                                                                        margin=dict(t=40)))

    c1, c2 = st.columns(2)
    cells = g.pivot_table(index="sleep_group", columns="screen_group", values="life_satisfaction_1to10",
                          aggfunc=["mean", "size"], observed=False)
    sweet = cells["mean"].where(cells["size"] >= 5)  # hide cells with too few people to trust
    fig = px.imshow(sweet, text_auto=".1f", aspect="auto",
                    color_continuous_scale=["#eef8f6", "#a8dccf", "#5dbfa9", "#00897b", "#005f56"],
                    labels={"x": "Daily screen time", "y": "Sleep per night", "color": "Life satisfaction"})
    with c1:
        if sweet.notna().any().any():
            best = sweet.stack().idxmax()
            st.caption(f"✨ Happiest combo: **{best[0]} sleep** with **{best[1]}** screen time "
                       f"(average {sweet.stack().max():.1f}/10)")
    chart(c1, "grid_on", "Find the sweet spot", "Average life satisfaction · blank = fewer than 5 people",
          fig.update_yaxes(autorange=True), TEAL)

    with c2.container(border=True, key="card_radar"):
        html(f'<div class="card-head" style="--c:{ROSE}"><div class="ic">{mi("radar")}</div><div>'
             f'<div class="t">Compare platforms</div><div class="s">100 = the average person · pick up to 3</div></div></div>')
        top3 = f.most_used_platform.value_counts().index[:3].tolist()
        picked = st.pills("Platforms", sorted(f.most_used_platform.unique()), selection_mode="multi", default=top3,
                          key="radar_pick", label_visibility="collapsed")[:3]
        metrics = {"daily_screen_hours": "Screen time", "daily_notifications": "Notifications",
                   "platforms_used_count": "Apps used", "avg_sleep_hours": "Sleep",
                   "life_satisfaction_1to10": "Life satisfaction", "self_esteem_1to10": "Self-esteem"}
        fig, all_vals = go.Figure(), []
        for plat in picked:
            sub = f[f.most_used_platform == plat]
            vals = [sub[m].mean() / f[m].mean() * 100 for m in metrics]
            all_vals += vals
            fig.add_trace(go.Scatterpolar(
                r=vals + vals[:1], theta=list(metrics.values()) + [list(metrics.values())[0]], name=plat,
                fill="toself", line=dict(color=PLATFORM_COLORS[plat], width=2.5), opacity=0.85,
                hovertemplate="%{theta}: %{r:.0f}<extra>" + plat + "</extra>"))
        lo, hi = (min(all_vals), max(all_vals)) if all_vals else (90, 110)
        pad = max(3, (hi - lo) * 0.25)  # zoom the scale to the data so small differences are visible
        fig.update_layout(polar=dict(bgcolor="white", radialaxis=dict(range=[lo - pad, hi + pad], showticklabels=False, gridcolor=GRID, linecolor=GRID, tickfont_color=MUTED,
                                                                      angle=90, tickangle=90),
                                     angularaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=INK_2, size=12))),
                          paper_bgcolor="white", height=380, legend=dict(y=-0.08))
        if picked:
            st.plotly_chart(fig, config=CHART_CFG, theme=None)
        else:
            st.info("Pick at least one platform above.", icon=":material/touch_app:")

    section("play_circle", "Watch it change with age", "Press ▶ Play — each bubble is a platform, bigger = more people")
    bub = g.groupby(["age_group", "most_used_platform"], observed=True).agg(
        screen=("daily_screen_hours", "mean"), life=("life_satisfaction_1to10", "mean"), people=("age", "size")
    ).reset_index().sort_values(["age_group", "most_used_platform"])
    bub["age_group"] = bub.age_group.astype(str)
    fig = px.scatter(bub, x="screen", y="life", size="people", color="most_used_platform",
                     animation_frame="age_group", size_max=55, color_discrete_map=PLATFORM_COLORS,
                     range_x=[bub.screen.min() - 1, bub.screen.max() + 1], range_y=[bub.life.min() - 1, bub.life.max() + 1],
                     labels={"screen": "Avg screen hours / day", "life": "Avg life satisfaction",
                             "most_used_platform": "Platform", "age_group": "Age", "people": "People"})
    fig.update_traces(marker=dict(line=dict(color="white", width=2), opacity=0.85))
    if fig.layout.updatemenus:
        fig.layout.updatemenus[0].buttons[0].args[1].update(frame=dict(duration=1400, redraw=False),
                                                           transition=dict(duration=900, easing="cubic-in-out"))
    fig.update_layout(height=500, legend=dict(orientation="h", y=1.1, x=0, title_text=""), sliders=[dict(currentvalue=dict(prefix="Age group: ", font=dict(color=INK)))])
    chart(st, "bubble_chart", "Platforms by age group", "Up = happier · right = more screen time", fig, LAVENDER)

# ---------------- Check yourself ----------------
with t6:
    section("person_search", "Check yourself", "Enter your habits and see how you compare — just for fun, not medical advice")
    c1, c2 = st.columns([1, 1.7], gap="large")
    with c1.container(border=True, key="card_you"):
        html(f'<div class="card-head" style="--c:{PERI}"><div class="ic">{mi("tune")}</div><div>'
             f'<div class="t">Your daily habits</div><div class="s">Move the sliders — results update live</div></div></div>')
        my_screen = st.slider(":material/schedule: Screen time (hours/day)", 0.0, 16.0, 5.0, 0.5)
        my_sleep = st.slider(":material/bedtime: Sleep (hours/night)", 3.0, 11.0, 7.0, 0.5)
        my_notif = st.slider(":material/notifications: Notifications per day", 0, 400, 80, 10)
        my_first = st.slider(":material/wb_twilight: Minutes until first phone check", 0, 120, 15, 5)
        my_night = st.toggle(":material/dark_mode: I scroll in bed at night")

    with c2:
        ranks = [
            ("schedule", f"{(f.daily_screen_hours < my_screen).mean():.0%}", "of people use their screen less than you", PERI),
            ("bedtime", f"{(f.avg_sleep_hours < my_sleep).mean():.0%}", "of people sleep less than you", LAVENDER),
            ("notifications_active", f"{(f.daily_notifications < my_notif).mean():.0%}",
             "of people get fewer notifications", SAND),
            ("wb_twilight", f"{(f.minutes_to_first_check_after_waking > my_first).mean():.0%}",
             "of people wait longer than you to check their phone", ROSE),
        ]
        html('<div class="insights">' + "".join(
            f'<div class="insight" style="--c:{c}">{mi(ic)}<span class="big">{v}</span>{t}</div>'
            for ic, v, t, c in ranks) + "</div>")
        st.write("")

        for tol_s, tol_z in [(1, 0.75), (2, 1.5), (4, 3)]:  # widen until enough similar people
            alike = f[(f.daily_screen_hours.sub(my_screen).abs() <= tol_s) & (f.avg_sleep_hours.sub(my_sleep).abs() <= tol_z)]
            if len(alike) >= 15:
                break
        if len(alike):
            my_life = alike.life_satisfaction_1to10.mean()
            same = abs(my_life - f.life_satisfaction_1to10.mean()) < 0.05
            fig = go.Figure(go.Indicator(
                mode="gauge+number" + ("" if same else "+delta"), value=my_life,
                number=dict(valueformat=".1f", suffix="/10", font=dict(size=44, color=INK)),
                delta=dict(reference=f.life_satisfaction_1to10.mean(), valueformat=".1f",
                           increasing_color="#3fb68b", decreasing_color="#e76f6f"),
                gauge=dict(axis=dict(range=[0, 10], tickcolor=MUTED, tickfont_color=MUTED),
                           bar=dict(color=PERI, thickness=0.3), bgcolor="white", borderwidth=0,
                           steps=[dict(range=[0, 4], color="#fdeaea"), dict(range=[4, 6.5], color="#fdf3dc"),
                                  dict(range=[6.5, 10], color="#e3f5ec")])))
            fig.update_layout(height=300, margin=dict(l=40, r=40, t=30, b=20))
            chart(st, "groups", "People like you",
                  f"Average life satisfaction of {len(alike):,} people with similar screen time & sleep "
                  f"(vs everyone in view)", fig, TEAL)

    heavy_gap = f[f.daily_screen_hours < 4].avg_sleep_hours.mean() - f[f.daily_screen_hours >= 8].avg_sleep_hours.mean()
    night_gap = f[f.night_time_use == "No"].avg_sleep_hours.mean() - f[f.night_time_use == "Yes"].avg_sleep_hours.mean()
    tips = []
    if my_screen >= 6:
        tips.append(("timer", "Set a daily app limit", f"Heavy users (8h+) here sleep about {heavy_gap:.1f} h less than light users."))
    if my_sleep < 7:
        tips.append(("bedtime", "Protect your sleep", "Most adults feel best with 7–9 hours a night."))
    if my_night:
        tips.append(("do_not_disturb_on", "Phone-free bedtime",
                     f"People who don't scroll at night sleep about {night_gap:.1f} h more here."))
    if my_first < 10:
        tips.append(("wb_sunny", "Slow mornings", "Try 15 phone-free minutes after waking up."))
    if my_notif > 100:
        tips.append(("notifications_off", "Silence the noise", "Turn off notifications from apps that aren't people."))
    if not tips:
        tips.append(("celebration", "Nicely balanced!", "Your habits look healthy compared with most people. Keep it up!"))
    section("tips_and_updates", "Small changes that help", "Personal tips based on your answers and the data")
    html('<div class="insights">' + "".join(
        f'<div class="insight" style="--c:{TEAL}">{mi(ic)}<span class="big" style="font-size:1.1rem">{t}</span>{d}</div>'
        for ic, t, d in tips) + "</div>")

# ---------------- Data explorer ----------------
with t7:
    section("table_view", "Data explorer", "Search, browse and download the filtered rows")
    q = st.text_input("Search any value", placeholder="e.g. Instagram, Student, Europe", icon=":material/search:")
    view = f[f.astype(str).apply(lambda r: r.str.contains(q, case=False, regex=False)).any(axis=1)] if q else f
    st.caption(f"Showing **{len(view):,}** rows")
    st.dataframe(view, width="stretch", hide_index=True, height=440,
                 column_config={
                     "daily_screen_hours": st.column_config.ProgressColumn(
                         "Screen hours", min_value=0, max_value=float(df.daily_screen_hours.max()), format="%.1f h"),
                     "life_satisfaction_1to10": st.column_config.ProgressColumn(
                         "Life satisfaction", min_value=0, max_value=10, format="%d/10"),
                 })
    st.download_button("Download filtered data (CSV)", view.to_csv(index=False), "filtered_data.csv", "text/csv",
                       type="primary", icon=":material/download:")
    with st.expander("Summary statistics", icon=":material/analytics:"):
        st.dataframe(view.describe().T.round(2), width="stretch")

html(f'<div class="footer">Made with {mi("favorite")} using Streamlit · Plotly · Pandas · Matplotlib</div>')

# Grow-in / count-up animations (runs once, then watches for new charts)
with st.container(key="anim"):
    components.html(f"<script>{open('animations.js').read()}</script>", height=0)
