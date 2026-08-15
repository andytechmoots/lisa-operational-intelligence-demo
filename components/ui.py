import streamlit as st


FEEDBACK_URL = "https://forms.gle/3R27EMmUa7gcWNW96"


def apply_app_styles() -> None:
    st.markdown(
        """
<style>

/* --------------------------------------------------
   Main page
-------------------------------------------------- */

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}


/* --------------------------------------------------
   LISA hero
-------------------------------------------------- */

.lisa-hero {
    padding: 1.25rem 1.5rem;
    border-radius: 14px;

    background: linear-gradient(
        135deg,
        #f8fafc 0%,
        #eaf2ff 100%
    );

    border: 1px solid #dbe5f0;
    margin-bottom: 1rem;
}

.lisa-hero h1 {
    margin: 0;
    padding: 0;

    font-size: 2rem;
    font-weight: 750;
    line-height: 1.2;

    color: #0f172a !important;
}

.lisa-hero p {
    margin-top: 0.55rem;
    margin-bottom: 0;

    font-size: 1rem;
    line-height: 1.5;

    color: #475569 !important;
}


/* --------------------------------------------------
   Scenario box
-------------------------------------------------- */

.scenario-box {
    padding: 1.3rem 1.4rem;

    border-radius: 14px;

    background: linear-gradient(
        135deg,
        #111827 0%,
        #172033 100%
    );

    border: 1px solid #334155;

    margin-top: 0.75rem;
    margin-bottom: 1rem;
}

.scenario-label {
    color: #94a3b8 !important;

    font-size: 0.78rem;
    font-weight: 700;

    letter-spacing: 0.06em;
    text-transform: uppercase;

    margin-bottom: 0.5rem;
}

.scenario-question {
    color: #f8fafc !important;

    font-size: 1.28rem;
    font-weight: 700;
    line-height: 1.5;
}

.scenario-support {
    color: #cbd5e1 !important;

    margin-top: 0.7rem;

    font-size: 0.95rem;
    line-height: 1.55;
}


/* --------------------------------------------------
   Workflow
-------------------------------------------------- */

.workflow-card {
    min-height: 150px;

    padding: 1rem 1.05rem;

    border-radius: 14px;
    border: 1px solid rgba(148, 163, 184, 0.35);

    box-shadow:
        0 1px 2px rgba(15, 23, 42, 0.04);
}

.workflow-spot {
    background: #fff8e8;
}

.workflow-investigate {
    background: #eef6ff;
}

.workflow-owner {
    background: #f4f1ff;
}

.workflow-action {
    background: #eefbf3;
}

.workflow-number {
    font-size: 0.72rem;
    font-weight: 700;

    letter-spacing: 0.04em;
    text-transform: uppercase;

    color: #64748b !important;

    margin-bottom: 0.45rem;
}

.workflow-title {
    font-size: 1.05rem;
    font-weight: 700;

    line-height: 1.35;

    margin-bottom: 0.45rem;

    color: #0f172a !important;
}

.workflow-text {
    font-size: 0.9rem;
    line-height: 1.55;

    color: #475569 !important;
}

.flow-arrow {
    text-align: center;

    font-size: 1.5rem;
    font-weight: 600;

    color: #94a3b8 !important;

    padding-top: 3.25rem;
}


/* --------------------------------------------------
   Attention
-------------------------------------------------- */

.attention-box {
    background: #fff7ed;

    border: 1px solid #fed7aa;
    border-left: 5px solid #f97316;

    border-radius: 12px;

    padding: 1rem 1.15rem;

    margin-top: 0.5rem;
    margin-bottom: 1rem;

    color: #431407 !important;
}

.attention-box strong {
    color: #9a3412 !important;
}


/* --------------------------------------------------
   Next step
-------------------------------------------------- */

.next-step-box {
    background: #eff6ff;

    border: 1px solid #bfdbfe;
    border-left: 5px solid #3b82f6;

    border-radius: 12px;

    padding: 1rem 1.15rem;

    margin-top: 1rem;
    margin-bottom: 0.75rem;

    color: #1e3a5f !important;
}

.next-step-box strong {
    color: #1e40af !important;
}


/* --------------------------------------------------
   Primary CTA
-------------------------------------------------- */

div.stButton > button[kind="primary"] {
    min-height: 4rem !important;

    font-size: 1.18rem !important;
    font-weight: 800 !important;

    letter-spacing: 0.01em;

    border-radius: 0.85rem !important;

    padding-left: 1.3rem !important;
    padding-right: 1.3rem !important;

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease,
        filter 0.18s ease !important;
}


/* Hover */

div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px);

    box-shadow:
        0 10px 24px rgba(0, 0, 0, 0.22) !important;

    filter: brightness(1.08);
}


/* Click */

div.stButton > button[kind="primary"]:active {
    transform: translateY(0);

    box-shadow:
        0 4px 10px rgba(0, 0, 0, 0.18) !important;
}


/* --------------------------------------------------
   Feedback
-------------------------------------------------- */

.feedback-box {
    background: #f8fafc;

    border-radius: 14px;
    border: 1px solid #e2e8f0;

    padding: 1rem 1.15rem;

    color: #334155 !important;
}


/* --------------------------------------------------
   Responsive
-------------------------------------------------- */

@media (max-width: 900px) {

    .lisa-hero h1 {
        font-size: 1.65rem;
    }

    .scenario-question {
        font-size: 1.08rem;
    }

    .workflow-card {
        min-height: auto;
    }

    .flow-arrow {
        padding-top: 1rem;
    }
}

</style>
""",
        unsafe_allow_html=True,
    )


def render_header(
    title: str,
    subtitle: str,
) -> None:

    apply_app_styles()

    st.markdown(
        f"""
<div class="lisa-hero">
<h1>{title}</h1>
<p>{subtitle}</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.info(
        "SYNTHETIC DEMO — No customer or production data.",
        icon="🧪",
    )


def render_workflow() -> None:

    st.subheader(
        "How LISA turns data into action"
    )

    columns = st.columns(
        [1, 0.12, 1, 0.12, 1, 0.12, 1]
    )

    with columns[0]:

        st.markdown(
            """
<div class="workflow-card workflow-spot">
<div class="workflow-number">STEP 1</div>
<div class="workflow-title">⚠️ Spot what matters</div>
<div class="workflow-text">Find shipments or network signals that may need attention.</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with columns[1]:

        st.markdown(
            '<div class="flow-arrow">→</div>',
            unsafe_allow_html=True,
        )

    with columns[2]:

        st.markdown(
            """
<div class="workflow-card workflow-investigate">
<div class="workflow-number">STEP 2</div>
<div class="workflow-title">🔎 Investigate</div>
<div class="workflow-text">Understand what happened by comparing expected and observed behaviour.</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with columns[3]:

        st.markdown(
            '<div class="flow-arrow">→</div>',
            unsafe_allow_html=True,
        )

    with columns[4]:

        st.markdown(
            """
<div class="workflow-card workflow-owner">
<div class="workflow-number">STEP 3</div>
<div class="workflow-title">🧭 Identify responsibility</div>
<div class="workflow-text">Determine who currently owns the shipment or operational issue.</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with columns[5]:

        st.markdown(
            '<div class="flow-arrow">→</div>',
            unsafe_allow_html=True,
        )

    with columns[6]:

        st.markdown(
            """
<div class="workflow-card workflow-action">
<div class="workflow-number">STEP 4</div>
<div class="workflow-title">✅ Decide the next action</div>
<div class="workflow-text">Turn operational evidence into a clear next step.</div>
</div>
""",
            unsafe_allow_html=True,
        )


def render_feedback() -> None:

    st.divider()

    st.markdown(
        """
<div class="feedback-box">
<strong>Help improve LISA</strong>
<br>
<span style="color:#64748b;">
Explored the demo? Share a quick 2-minute feedback to help shape future iterations.
</span>
</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

    st.link_button(
        "💬 Give Feedback",
        FEEDBACK_URL,
        help="Open the LISA Demo feedback form.",
    )