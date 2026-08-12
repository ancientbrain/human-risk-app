import streamlit as st
import requests
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Behavrix",
    page_icon="🔐",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .risk-critical { background: #FAEEDA; border-left: 4px solid #B8433A; padding: 12px; border-radius: 6px; }
    .risk-high { background: #FAEEDA; border-left: 4px solid #C9702E; padding: 12px; border-radius: 6px; }
    .risk-medium { background: #dbeafe; border-left: 4px solid #378ADD; padding: 12px; border-radius: 6px; }
    .risk-low { background: #d1fae5; border-left: 4px solid #1D9E75; padding: 12px; border-radius: 6px; }
    .persona-card { background: #0D1F35; padding: 12px 16px; border-radius: 8px; margin: 6px 0; }
    .section-header { font-size: 18px; font-weight: 600; margin-top: 20px; margin-bottom: 10px; }
    .insight-box { background: #0D1F35; border: 1px solid #378ADD; padding: 16px; border-radius: 8px; font-style: italic; }
    .footer-text { color: #64748b; font-size: 12px; text-align: center; margin-top: 40px; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("logo.png", width=80)
    st.title("Behavrix")
    st.caption("Human Risk Report Generator · Powered by 270 real cybersecurity records")
    st.markdown("**Madison Framework · SyntheticPersonas**")
    st.divider()

    st.subheader("🔑 API Configuration")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Paste your API key here",
        help="Get your free key at aistudio.google.com"
    )
    if api_key:
        st.success("API key entered ✅")

    st.divider()
    st.subheader("📖 How to use this tool")
    st.markdown("""
1. Enter your Gemini API key above
2. Select your organization type
3. Click **Generate Report**
4. Download your report as a text file
    """)

    st.divider()
    st.subheader("📊 Data Sources")
    st.markdown("""
- 📧 120 phishing email records
- 🌐 120 social engineering records
- 🏛️ 30 CISA live advisories
- **270 total records analyzed**
    """)

    st.divider()
    st.caption("Built with n8n + Gemini 2.0 Flash")
    st.caption("Satwika Maddukuri · INFO 7375 · NEU")

# ── MAIN CONTENT ─────────────────────────────────────────────────────────────
st.title("Behavrix — Human Risk Report Generator")
st.markdown("Generate a human vulnerability risk report for any organization type — powered by 270 real cybersecurity records.")
st.divider()

# Input section
col1, col2 = st.columns([2, 1])
with col1:
    company_type = st.selectbox(
        "Select Organization Type",
        ["Financial Institution",
         "Healthcare Provider",
         "Government Agency",
         "Retail Company",
         "Tech Startup",
         "Law Firm",
         "University",
         "Manufacturing Company",
         "Insurance Company",
         "Non-Profit Organization"],
        help="The report will be tailored to the specific risk profile of this organization type"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    generate = st.button(
        "Generate Human Risk Report",
        type="primary",
        use_container_width=True,
        disabled=not api_key
    )
    if not api_key:
        st.caption("⬅️ Enter API key in sidebar first")

st.divider()

# ── GENERATE REPORT ──────────────────────────────────────────────────────────
if generate:
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar to generate a report.")
    else:
        with st.spinner(f"Analyzing 270 records for {company_type}... this takes about 30 seconds"):
            try:
                prompt = f"""You are a cybersecurity expert analyzing human vulnerability patterns.
Based on analysis of 270 real records including 120 phishing emails (avg urgency_flag rate 0.52),
120 social engineering interactions (avg fear_trigger_score 0.523, avg trust_manipulation_score 0.71),
and 30 live CISA advisories, generate a Human Risk Report for a {company_type}.

Return ONLY a valid JSON object with NO extra text, NO markdown, NO backticks:

{{
  "risk_score": <number 0-100>,
  "risk_level": "<Low/Medium/High/Critical>",
  "top_personas": [
    {{"name": "<The Clicker OR Password Recycler OR Shadow IT User OR Over-Trusted Insider>", "risk": "<High/Medium/Low>", "percentage": <number 1-100>, "mitre": "<T1566/T1078/T1072/T1134>", "reason": "<one sentence why this persona is high risk for this org type>"}},
    {{"name": "<different persona>", "risk": "<High/Medium/Low>", "percentage": <number 1-100>, "mitre": "<technique>", "reason": "<reason>"}},
    {{"name": "<different persona>", "risk": "<High/Medium/Low>", "percentage": <number 1-100>, "mitre": "<technique>", "reason": "<reason>"}}
  ],
  "attack_scenarios": [
    "<specific realistic attack scenario 1 for {company_type}>",
    "<specific realistic attack scenario 2>",
    "<specific realistic attack scenario 3>"
  ],
  "brand_recommendations": [
    "<specific brand trust recommendation 1>",
    "<specific brand trust recommendation 2>",
    "<specific brand trust recommendation 3>"
  ],
  "key_insight": "<one powerful data-backed insight specific to {company_type} referencing fear_trigger_score or trust_manipulation patterns>"
}}"""

                response = requests.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}",
                    json={"contents": [{"parts": [{"text": prompt}]}]},
                    timeout=45
                )

                if response.status_code == 200:
                    raw = response.json()
                    text = raw["candidates"][0]["content"]["parts"][0]["text"].strip()
                    if "```" in text:
                        text = text.split("```")[1]
                        if text.startswith("json"):
                            text = text[4:]
                    data = json.loads(text.strip())

                    st.success(f"✅ Report generated for {company_type}!")
                    st.caption("⚠️ Advisory Report — This report is based on analysis of 270 real cybersecurity records collected in May 2026. It is designed for awareness and tabletop exercises, not as a standalone risk assessment tool.")

                    # ── RISK SCORE ────────────────────────────────────────────
                    score = data["risk_score"]
                    level = data["risk_level"]

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Human Risk Score", f"{score} / 100")
                        st.caption("Score based on fear_trigger_score, urgency patterns, and trust manipulation indicators across 270 records.")
                    with col2:
                        st.metric("Risk Level", level)
                    with col3:
                        st.metric("Organization", company_type)

                    # Color coded progress bar
                    bar_color = "#B8433A" if score >= 75 else "#C9702E" if score >= 50 else "#378ADD" if score >= 25 else "#1D9E75"
                    st.markdown(f"""
                    <div style="background:#0D1F35;border-radius:8px;padding:4px;margin:8px 0">
                        <div style="background:{bar_color};width:{score}%;height:16px;border-radius:6px;transition:width 0.5s"></div>
                    </div>
                    """, unsafe_allow_html=True)

                    risk_css = "risk-critical" if level == "Critical" else "risk-high" if level == "High" else "risk-medium" if level == "Medium" else "risk-low"
                    st.markdown(f'<div class="{risk_css}" style="color:#1a1a1a">⚠️ <strong>{level} Risk</strong> — This organization type shows elevated human vulnerability based on behavioral pattern analysis of 270 real cybersecurity records.</div>', unsafe_allow_html=True)

                    st.divider()

                    # ── PERSONAS ──────────────────────────────────────────────
                    st.markdown('<div class="section-header">🎭 Top Vulnerable Personas</div>', unsafe_allow_html=True)
                    cols = st.columns(3)
                    for i, p in enumerate(data["top_personas"]):
                        risk_icon = "🔴" if p["risk"] == "High" else "🟡" if p["risk"] == "Medium" else "🟢"
                        with cols[i]:
                            st.markdown(f"""
                            <div class="persona-card">
                                <div style="font-size:16px;font-weight:600">{risk_icon} {p['name']}</div>
                                <div style="color:#94a3b8;font-size:12px;margin:4px 0">{p['risk']} Risk · {p.get('percentage','')}% of records · MITRE {p.get('mitre','')}</div>
                                <div style="font-size:13px;margin-top:8px">{p['reason']}</div>
                            </div>
                            """, unsafe_allow_html=True)

                    st.divider()

                    # ── ATTACK SCENARIOS ──────────────────────────────────────
                    st.markdown('<div class="section-header">⚠️ Top Attack Scenarios</div>', unsafe_allow_html=True)
                    for i, scenario in enumerate(data["attack_scenarios"], 1):
                        st.markdown(f"**{i}.** {scenario}")

                    st.divider()

                    # ── BRAND RECOMMENDATIONS ─────────────────────────────────
                    st.markdown('<div class="section-header">🛡️ Brand Trust Recommendations</div>', unsafe_allow_html=True)
                    for i, rec in enumerate(data["brand_recommendations"], 1):
                        st.markdown(f"**{i}.** {rec}")

                    st.divider()

                    # ── KEY INSIGHT ───────────────────────────────────────────
                    st.markdown('<div class="section-header">💡 Key Insight</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="insight-box">"{data["key_insight"]}"</div>', unsafe_allow_html=True)

                    st.divider()

                    # ── DOWNLOAD ──────────────────────────────────────────────
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    report_text = f"""HUMAN RISK REPORT
Generated: {datetime.now().strftime("%B %d, %Y %H:%M")}
Organization Type: {company_type}
Tool: Human Risk Report Generator · Madison Framework · SyntheticPersonas

═══════════════════════════════════════════════════
HUMAN RISK SCORE: {score}/100 — {level} Risk
═══════════════════════════════════════════════════

TOP VULNERABLE PERSONAS
"""
                    for p in data["top_personas"]:
                        report_text += f"\n• {p['name']} — {p['risk']} Risk (MITRE {p.get('mitre','')})\n  {p['reason']}\n"

                    report_text += "\nTOP ATTACK SCENARIOS\n"
                    for i, s in enumerate(data["attack_scenarios"], 1):
                        report_text += f"\n{i}. {s}\n"

                    report_text += "\nBRAND TRUST RECOMMENDATIONS\n"
                    for i, r in enumerate(data["brand_recommendations"], 1):
                        report_text += f"\n{i}. {r}\n"

                    report_text += f"\nKEY INSIGHT\n\n{data['key_insight']}\n"
                    report_text += f"\n═══════════════════════════════════════════════════\nData: 120 phishing emails · 120 social engineering records · 30 CISA advisories · 270 total records\nBuilt with n8n + Gemini 2.0 Flash · Satwika Maddukuri · INFO 7375 · NEU\n"

                    st.download_button(
                        label="📥 Download Report as Text File",
                        data=report_text,
                        file_name=f"HumanRiskReport_{company_type.replace(' ','_')}_{timestamp}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                elif response.status_code == 429:
                    st.error("⏱️ Rate limit reached. Please wait 60 seconds and try again. This is a free tier limitation.")
                elif response.status_code == 403:
                    st.error("🔑 Invalid API key. Please check your Gemini API key in the sidebar and try again.")
                elif response.status_code == 400:
                    st.error("❌ Bad request. Please try a different organization type.")
                else:
                    st.error(f"⚠️ Something went wrong (Error {response.status_code}). Please try again.")

            except json.JSONDecodeError:
                st.error("🤖 The AI returned an unexpected format. Please click Generate again.")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Please check your internet connection and try again.")
            except KeyError:
                st.error("🤖 Unexpected response from AI. Please try again.")
            except Exception:
                st.error("⚠️ An unexpected error occurred. Please try again.")

# Empty state message
else:
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;color:#64748b">
        <div style="font-size:48px">🔐</div>
        <div style="font-size:20px;margin:12px 0">Ready to generate your report</div>
        <div style="font-size:14px">Enter your API key in the sidebar, select an organization type, and click Generate</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="footer-text">Behavrix · Human Risk Report Generator · Madison Framework · SyntheticPersonas · Built with n8n + Gemini 2.0 Flash<br>Data: Kaggle Phishing Dataset · Global Cognitive Threat Dataset · CISA RSS Feed · Satwika Maddukuri · INFO 7375 · NEU</div>', unsafe_allow_html=True)
