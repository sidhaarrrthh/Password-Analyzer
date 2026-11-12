
import html

import streamlit as st
from password_analyzer import analyze_password


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Password Analyzer | Security Dashboard",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Main application background */
.stApp {
    background-color: #F8FAFC;
    color: #0F172A;
}

/* Main content width */
.block-container {
    max-width: 900px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

/* Hide Streamlit decoration */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Main heading */
.main-title {
    font-size: 2.3rem;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 0.3rem;
    letter-spacing: -1px;
}

.subtitle {
    color: #64748B;
    font-size: 1rem;
    margin-bottom: 2rem;
}

/* Cards */
.dashboard-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 18px rgba(15, 23, 42, 0.035);
}

/* Section heading */
.section-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 15px;
}

/* Score card */
.metric-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
}

.metric-label {
    color: #64748B;
    font-size: 0.85rem;
    font-weight: 500;
}

.metric-value {
    font-size: 1.7rem;
    font-weight: 750;
    color: #0F172A;
    margin-top: 8px;
}

/* Warning and recommendation cards */
.warning-box {
    background: #FFF7ED;
    border-left: 4px solid #F59E0B;
    padding: 14px 16px;
    border-radius: 8px;
    margin-bottom: 10px;
    color: #92400E;
    font-size: 0.94rem;
}

.recommendation-box {
    background: #EFF6FF;
    border-left: 4px solid #3B82F6;
    padding: 14px 16px;
    border-radius: 8px;
    margin-bottom: 10px;
    color: #1E40AF;
    font-size: 0.94rem;
}

.success-box {
    background: #F0FDF4;
    border-left: 4px solid #22C55E;
    padding: 14px 16px;
    border-radius: 8px;
    color: #166534;
    margin-bottom: 12px;
}

/* Strength bar */
.strength-track {
    height: 12px;
    width: 100%;
    background: #E2E8F0;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 14px;
    margin-bottom: 10px;
}

.strength-fill {
    height: 100%;
    border-radius: 20px;
    transition: width 0.3s ease;
}

/* Buttons */
div.stButton > button {
    background-color: #2563EB;
    color: #FFFFFF;
    border-radius: 10px;
    padding: 0.7rem 1.4rem;
    border: none;
    font-weight: 600;
    width: 100%;
}

div.stButton > button:hover {
    background-color: #1D4ED8;
    color: #FFFFFF;
    border: none;
}

/* Input styling */
div[data-testid="stTextInput"] input {
    border-radius: 10px;
    background: #FFFFFF;
    color: #0F172A;
}

/* Footer */
.custom-footer {
    text-align: center;
    color: #94A3B8;
    font-size: 0.8rem;
    margin-top: 35px;
    padding-top: 20px;
    border-top: 1px solid #E2E8F0;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def safe_text(value):
    """Escape text before inserting it into HTML."""
    return html.escape(str(value))


def render_card(title, value, color="#0F172A"):
    """Display a dashboard metric card."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{safe_text(title)}</div>
            <div class="metric-value" style="color:{color};">
                {safe_text(value)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_message(message, style="recommendation"):
    """Display a styled warning or recommendation."""
    allowed_styles = {
        "warning": "warning-box",
        "recommendation": "recommendation-box",
        "success": "success-box"
    }

    css_class = allowed_styles.get(style, "recommendation-box")

    st.markdown(
        f'<div class="{css_class}">{safe_text(message)}</div>',
        unsafe_allow_html=True
    )


def get_strength_style(score):
    """Return strength label color and progress percentage."""

    styles = {
        0: ("#EF4444", 5),
        1: ("#F97316", 25),
        2: ("#F59E0B", 50),
        3: ("#3B82F6", 75),
        4: ("#16A34A", 100)
    }

    return styles.get(score, ("#64748B", 0))


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="main-title">🔐 Password Analyzer</div>
    <div class="subtitle">
        Evaluate password strength, identify security weaknesses,
        and receive actionable recommendations.
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "🔒 Privacy First — Password analysis runs locally. "
    "The application does not intentionally save submitted passwords."
)


# --------------------------------------------------
# PASSWORD INPUT
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Password Security Check</div>',
    unsafe_allow_html=True
)

with st.form("password_form", clear_on_submit=False):

    password = st.text_input(
        "Enter password",
        type="password",
        placeholder="Enter a password to evaluate",
        help="For testing, use sample passwords rather than real credentials."
    )

    analyze_button = st.form_submit_button(
        "Analyze Password",
        use_container_width=True
    )


# --------------------------------------------------
# PASSWORD ANALYSIS
# --------------------------------------------------

if analyze_button:

    if not password:
        st.warning("Please enter a password to continue.")

    else:
        results = analyze_password(password)

        score = results["score"]
        strength = results["strength"]
        color, percentage = get_strength_style(score)

        st.divider()

        st.markdown(
            '<div class="section-title">Security Overview</div>',
            unsafe_allow_html=True
        )

        # Metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            render_card("Password Strength", strength, color)

        with col2:
            render_card("Strength Score", f"{score}/4", "#2563EB")

        with col3:
            render_card(
                "Password Length",
                f'{results["length"]} chars',
                "#0F172A"
            )

        # Strength meter
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="section-title">Strength Assessment</div>
                <div class="metric-label">
                    Estimated password resistance
                </div>
                <div class="strength-track">
                    <div class="strength-fill"
                         style="width:{percentage}%;background:{color};">
                    </div>
                </div>
                <div style="color:{color};font-weight:700;">
                    {safe_text(strength)}
                </div>
                <div style="color:#64748B;font-size:0.8rem;margin-top:8px;">
                    Estimated by zxcvbn. This is not a security guarantee.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Custom review status
        st.markdown(
            '<div class="section-title">Security Review</div>',
            unsafe_allow_html=True
        )

        if results["warnings"]:
            render_message(
                "Additional security review recommended.",
                "warning"
            )
        else:
            render_message(
                "No custom security checks were triggered.",
                "success"
            )

        # Security warnings
        st.markdown(
            '<div class="section-title">Security Warnings</div>',
            unsafe_allow_html=True
        )

        if results["warnings"]:
            for warning in results["warnings"]:
                render_message("⚠ " + warning, "warning")
        else:
            render_message(
                "No additional weaknesses detected by custom checks.",
                "success"
            )

        # Recommendations
        st.markdown(
            '<div class="section-title">Recommendations</div>',
            unsafe_allow_html=True
        )

        recommendations = results["suggestions"]

        if recommendations:
            for recommendation in recommendations:
                render_message("→ " + recommendation)
        else:
            render_message(
                "No additional length or character recommendations.",
                "success"
            )

        # zxcvbn feedback
        feedback = results["feedback"]

        if feedback["warning"] or feedback["suggestions"]:

            st.markdown(
                '<div class="section-title">Additional Security Insights</div>',
                unsafe_allow_html=True
            )

            if feedback["warning"]:
                render_message(
                    "⚠ " + feedback["warning"],
                    "warning"
                )

            for suggestion in feedback["suggestions"]:
                render_message("→ " + suggestion)

        st.caption(
            "Security note: Password strength is an estimate. "
            "Use unique passwords and multifactor authentication "
            "where available."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="custom-footer">
        Password Analyzer | Cybersecurity Project<br>
        Built with Python, Streamlit and zxcvbn
    </div>
    """,
    unsafe_allow_html=True
)