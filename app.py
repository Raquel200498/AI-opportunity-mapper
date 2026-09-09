import streamlit as st
import json
from anthropic import Anthropic

st.set_page_config(page_title="AI Opportunity Mapper", layout="wide")

# Initialize Anthropic client
client = Anthropic()

# Styling
st.markdown("""
<style>
    .main {
        background-color: #f9f9f9;
    }
    .stButton > button {
        width: 100%;
        background-color: #0f2c4a;
        color: white;
        font-weight: 600;
    }
    .about-section {
        background-color: #e8f0f7;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #0f2c4a;
        margin-bottom: 1rem;
    }
    .footer-section {
        border-top: 2px solid #0f2c4a;
        padding-top: 1.5rem;
        margin-top: 1.5rem;
        text-align: center;
        color: #0f2c4a;
    }
    .footer-name {
        font-weight: 600;
        font-size: 16px;
    }
    .footer-title {
        font-size: 13px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("# AI Opportunity Mapper")
st.markdown("*Tailored AI Transformation Roadmaps*")
st.divider()

# About section
st.markdown("""
<div class="about-section">
    <b>About this app:</b><br><br>
    AI Opportunity Mapper is a digital transformation roadmap generator designed to help organizations accelerate their AI journey. Whether you're starting from scratch or optimizing existing processes, this tool generates detailed, actionable AI transformation roadmaps tailored to your specific business challenges.
    <br><br>
    <b>How it works:</b> Describe your business problem, select your industry, and receive a comprehensive roadmap including AI opportunities, week-by-week implementation phases, budget estimates, required team composition, ROI projections, and risk mitigation strategies.
    <br><br>
    <b>Perfect for:</b> Business leaders, digital strategists, CTOs, and consultants evaluating AI initiatives and planning digital transformation.
    <br><br>
    <i>Created by <b>Raquel Rodrigues dos Santos</b> - Digital Strategy & AI Transformation Specialist</i>
</div>
""", unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.header("Your Challenge")
    
    industry = st.selectbox(
        "What is your industry?",
        ("Finance", "Retail", "Healthcare", "Manufacturing", "Tech", "Other")
    )
    
    challenge = st.text_area(
        "Describe your key business challenge",
        placeholder="What specific problem are you trying to solve?\n\nInclude:\n• Current situation (what's happening now?)\n• Pain points (what's costing you money/time?)\n• Desired outcome (what do you want to achieve?)\n• Any constraints or priorities",
        height=220
    )
    
    company_size = st.selectbox(
        "Company size",
        ("Startup (1-50)", "SMB (50-500)", "Mid-market (500-5K)", "Enterprise (5K+)")
    )
    
    generate_btn = st.button("Generate Roadmap", type="primary")

# Main content area
if generate_btn:
    if not industry or not challenge or not company_size:
        st.error("Please complete all fields")
    else:
        with st.spinner("Analyzing your challenge and generating roadmap..."):
            try:
                prompt = f"""You are an elite AI consulting expert specializing in digital transformation and AI implementation. Your task is to create a detailed, specific, and actionable AI transformation roadmap.

USER'S SITUATION:
- Industry: {industry}
- Company Size: {company_size}
- Challenge: {challenge}

GENERATE A COMPREHENSIVE ROADMAP AS VALID JSON (no markdown, no code blocks, no preamble):

{{
  "title": "Specific roadmap title",
  "subtitle": "Executive summary (one line)",
  "narrative": "2-3 paragraphs explaining the challenge and transformation approach",
  "opportunities": [
    {{
      "name": "Specific AI opportunity name",
      "description": "2-3 sentences describing it",
      "implementation": "Week-by-week breakdown (Week 1-2: task, Week 3-4: task, etc)",
      "tools": "Specific tech (e.g., TensorFlow, Snowflake, AWS SageMaker)",
      "investment": "Specific amount (e.g., $45K)",
      "team": "Team composition (e.g., 2 Data Scientists, 1 ML Engineer)",
      "roi": "Specific ROI (e.g., 180-220%)",
      "businessImpact": "Specific impact with numbers"
    }}
  ],
  "phases": [
    {{
      "number": 1,
      "title": "Phase title",
      "duration": "X weeks | $YYK",
      "focus": "What this phase achieves",
      "milestones": ["Week 1-2: milestone", "Week 3: milestone"],
      "activities": ["Activity 1", "Activity 2"],
      "deliverables": ["Deliverable 1", "Deliverable 2"],
      "investment": "$XXXK",
      "team": "Team composition"
    }}
  ],
  "risks": [
    {{"risk": "Risk description", "mitigation": "Specific mitigation"}}
  ],
  "successMetrics": [
    "Metric 1 with numbers",
    "Metric 2 with numbers"
  ]
}}

CRITICAL REQUIREMENTS:
1. WEEK-BY-WEEK DETAILS: Real weeks, not vague phases
2. REAL NUMBERS: Dollar amounts, percentages, quantities
3. SPECIFIC TOOLS: Real software/services
4. TEAM COMPOSITION: Roles and FTE
5. 3+ PHASES: Each 4-10 weeks
6. ROI CALCULATIONS: Show the math
7. RISKS & MITIGATIONS: 4-5 specific risks with tactical solutions

GENERATE NOW:"""

                message = client.messages.create(
                    model="claude-opus-4-1-20250805",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                response_text = message.content[0].text.strip()
                
                # Clean markdown if present
                if response_text.startswith('```'):
                    response_text = response_text.split('```')[1]
                    if response_text.startswith('json'):
                        response_text = response_text[4:]
                    response_text = response_text.strip()
                
                roadmap = json.loads(response_text)
                
                # Display roadmap
                st.success("Roadmap generated successfully!")
                st.divider()
                
                # Title and subtitle
                st.markdown(f"## {roadmap.get('title', 'AI Roadmap')}")
                if roadmap.get('subtitle'):
                    st.markdown(f"*{roadmap['subtitle']}*")
                
                # Narrative
                if roadmap.get('narrative'):
                    st.info(roadmap['narrative'])
                
                # Opportunities
                if roadmap.get('opportunities'):
                    st.markdown("### AI Opportunities")
                    for idx, opp in enumerate(roadmap['opportunities'], 1):
                        with st.expander(f"{idx}. {opp.get('name', 'Opportunity')}"):
                            st.write(opp.get('description', ''))
                            if opp.get('implementation'):
                                st.markdown("**Implementation:**")
                                st.code(opp['implementation'])
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Investment", opp.get('investment', 'N/A'))
                            with col2:
                                st.metric("ROI", opp.get('roi', 'N/A'))
                            with col3:
                                st.metric("Team", opp.get('team', 'N/A'))
                            if opp.get('tools'):
                                st.write(f"**Tools:** {opp['tools']}")
                            if opp.get('businessImpact'):
                                st.write(f"**Business Impact:** {opp['businessImpact']}")
                
                # Phases
                if roadmap.get('phases'):
                    st.markdown("### Implementation Roadmap")
                    for phase in roadmap['phases']:
                        with st.expander(f"Phase {phase.get('number', 1)}: {phase.get('title', 'Phase')} ({phase.get('duration', '')})"):
                            if phase.get('focus'):
                                st.write(f"**Focus:** {phase['focus']}")
                            if phase.get('milestones'):
                                st.markdown("**Key Milestones:**")
                                for m in phase['milestones']:
                                    st.write(f"• {m}")
                            if phase.get('activities'):
                                st.markdown("**Activities:**")
                                for a in phase['activities']:
                                    st.write(f"• {a}")
                            if phase.get('deliverables'):
                                st.markdown("**Deliverables:**")
                                for d in phase['deliverables']:
                                    st.write(f"• {d}")
                            col1, col2 = st.columns(2)
                            with col1:
                                if phase.get('investment'):
                                    st.metric("Investment", phase['investment'])
                            with col2:
                                if phase.get('team'):
                                    st.write(f"**Team:** {phase['team']}")
                
                # Risks
                if roadmap.get('risks'):
                    st.markdown("### Key Risks & Mitigation")
                    for risk in roadmap['risks']:
                        with st.expander(f"⚠️ {risk.get('risk', 'Risk')}"):
                            st.write(risk.get('mitigation', ''))
                
                # Success metrics
                if roadmap.get('successMetrics'):
                    st.markdown("### Success Metrics")
                    for metric in roadmap['successMetrics']:
                        st.write(f"• {metric}")
                
            except json.JSONDecodeError as e:
                st.error(f"Error parsing response: {str(e)}")
            except Exception as e:
                st.error(f"Error generating roadmap: {str(e)}")

# Footer
st.markdown("""
<div class="footer-section">
    <div class="footer-name">Crafted by Raquel Rodrigues dos Santos</div>
    <div class="footer-title">Digital Strategy & AI Transformation Specialist</div>
</div>
""", unsafe_allow_html=True)
