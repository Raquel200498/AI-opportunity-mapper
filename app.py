import streamlit as st
import json
from anthropic import Anthropic

st.set_page_config(page_title="AI Opportunity Mapper", layout="wide")

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
    
    /* Aggressive spacing reduction */
    div[data-testid="stMarkdownContainer"] {
        margin-bottom: 0 !important;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        margin-bottom: 0.1rem !important;
    }
    
    p {
        margin: 0 !important;
        padding: 0.2rem 0 !important;
    }
    
    li {
        margin: 0.1rem 0 !important;
        padding: 0.1rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("# AI Opportunity Mapper")
st.markdown("*Tailored AI Transformation Roadmaps*")

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
        ("Finance", "Retail", "Healthcare", "Manufacturing", "Tech")
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
    
    budget = st.selectbox(
        "Approximate budget for this initiative",
        ("$25K-50K", "$50K-100K", "$100K-250K", "$250K-500K", "$500K+")
    )
    
    timeline = st.selectbox(
        "Timeline to implement",
        ("1-3 months", "3-6 months", "6-12 months", "12+ months")
    )
    
    generate_btn = st.button("Generate Roadmap", type="primary")

# Main content area
if generate_btn:
    if not industry or not challenge or not company_size or not budget or not timeline:
        st.error("Please complete all fields")
    else:
        with st.spinner("Generating your roadmap..."):
            try:
                prompt = f"""You are an elite AI consulting expert. Generate a JSON roadmap for this challenge.

SITUATION:
- Industry: {industry}
- Company Size: {company_size}
- Budget: {budget}
- Timeline: {timeline}
- Challenge: {challenge}

Return ONLY valid JSON (no markdown, no code blocks):

{{
  "title": "Specific roadmap title",
  "subtitle": "One-line executive summary",
  "narrative": "2-3 sentences on the challenge and approach",
  "opportunities": [
    {{
      "name": "Opportunity name",
      "emoji": "🎯",
      "description": "Brief description",
      "implementation": "Week 1-2: Task 1\\nWeek 3-4: Task 2",
      "tools": "Tool 1, Tool 2, Tool 3",
      "investment": "$XXK",
      "team": "X role, Y role",
      "roi": "XXX%",
      "impact": "Specific business impact"
    }}
  ],
  "phases": [
    {{
      "number": 1,
      "title": "Phase title",
      "duration": "X weeks",
      "focus": "What this achieves",
      "milestones": ["Milestone 1", "Milestone 2"],
      "investment": "$XXK",
      "team": "Team composition"
    }}
  ],
  "risks": [
    {{
      "risk": "Risk name",
      "mitigation": "How to mitigate"
    }}
  ],
  "metrics": ["Metric 1", "Metric 2", "Metric 3"]
}}"""

                message = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # Extract text
                response_text = ""
                for block in message.content:
                    if hasattr(block, 'type') and block.type == 'text':
                        response_text = block.text.strip()
                        break
                
                # Clean and parse JSON
                if response_text.startswith('```'):
                    response_text = response_text.split('```')[1]
                    if response_text.startswith('json'):
                        response_text = response_text[4:]
                    response_text = response_text.strip()
                
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    response_text = response_text[start_idx:end_idx+1]
                
                roadmap = json.loads(response_text)
                
                # Display roadmap
                st.success("Roadmap generated successfully!")
                st.divider()
                
                # Title and subtitle
                st.markdown(f"## {roadmap.get('title', 'AI Roadmap')}")
                st.markdown(f"*{roadmap.get('subtitle', '')}*")
                
                # Narrative
                if roadmap.get('narrative'):
                    st.info(roadmap['narrative'])
                
                # Opportunities
                if roadmap.get('opportunities'):
                    st.markdown("## AI Opportunities")
                    for idx, opp in enumerate(roadmap['opportunities'], 1):
                        with st.expander(f"{idx}. {opp.get('name', 'Opportunity')}", expanded=idx==1):
                            col_main, col_metrics = st.columns([2, 1])
                            
                            with col_main:
                                st.write(opp.get('description', ''))
                                
                                if opp.get('implementation'):
                                    st.markdown("**Implementation Timeline**")
                                    for line in opp['implementation'].split('\n'):
                                        if line.strip():
                                            st.write(f"• {line.strip()}")
                                
                                if opp.get('impact'):
                                    st.markdown("**Business Impact**")
                                    st.write(opp['impact'])
                            
                            with col_metrics:
                                st.markdown("**Investment**")
                                st.metric("", opp.get('investment', 'TBD'))
                                st.markdown("**ROI**")
                                st.metric("", opp.get('roi', 'TBD'))
                                st.markdown("---")
                                st.write(f"**Team:** {opp.get('team', 'TBD')}")
                                st.write(f"**Tools:** {opp.get('tools', 'TBD')}")
                
                # Phases
                if roadmap.get('phases'):
                    st.markdown("## Implementation Roadmap")
                    for phase in roadmap['phases']:
                        with st.expander(f"Phase {phase.get('number', 1)}: {phase.get('title', 'Phase')} | {phase.get('duration', '')}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**Focus**")
                                st.write(phase.get('focus', 'N/A'))
                                if phase.get('milestones'):
                                    st.markdown("**Milestones**")
                                    for m in phase['milestones']:
                                        st.write(f"• {m}")
                            
                            with col2:
                                st.metric("Investment", phase.get('investment', 'TBD'))
                                st.write(f"**Team:** {phase.get('team', 'TBD')}")
                
                # Risks
                if roadmap.get('risks'):
                    st.markdown("## Key Risks & Mitigation")
                    for risk in roadmap['risks']:
                        with st.expander(f"{risk.get('risk', 'Risk')}"):
                            st.write(risk.get('mitigation', ''))
                
                # Metrics
                if roadmap.get('metrics'):
                    st.markdown("## Success Metrics")
                    
                    # Show max 4 metrics in 2 rows of 2
                    metrics_to_show = roadmap['metrics'][:4]
                    
                    for row_idx in range(0, len(metrics_to_show), 2):
                        cols = st.columns(2)
                        for col_idx, col in enumerate(cols):
                            metric_idx = row_idx + col_idx
                            if metric_idx < len(metrics_to_show):
                                metric = metrics_to_show[metric_idx]
                                
                                # Try to extract number and description
                                parts = metric.split(':')
                                if len(parts) >= 2:
                                    # Extract potential number from first part
                                    first_part = parts[0].strip()
                                    # Get last number-like part
                                    import re
                                    numbers = re.findall(r'\d+[\d%\+\-]*', first_part)
                                    if numbers:
                                        value = numbers[-1]
                                        description = ':'.join(parts[1:]).strip()[:40]
                                    else:
                                        value = first_part[-20:]
                                        description = ':'.join(parts[1:]).strip()[:30]
                                else:
                                    value = metric[:25]
                                    description = ""
                                
                                with col:
                                    st.markdown(f"""
                                    <div style="
                                        background: linear-gradient(135deg, #0f2c4a 0%, #1a3f5c 100%);
                                        padding: 1.5rem 1rem;
                                        border-radius: 12px;
                                        color: white;
                                        text-align: center;
                                        min-height: 180px;
                                        display: flex;
                                        flex-direction: column;
                                        justify-content: center;
                                    ">
                                        <div style="font-size: 32px; font-weight: 700; margin-bottom: 0.8rem; word-wrap: break-word;">
                                            {value}
                                        </div>
                                        <div style="font-size: 12px; opacity: 0.85; line-height: 1.3;">
                                            {description}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                
            except json.JSONDecodeError as e:
                st.error(f"Error parsing response. Please try again.")
            except Exception as e:
                st.error(f"Error generating roadmap: {str(e)}")

# Footer
st.markdown("""
<div class="footer-section">
    <div class="footer-name">Crafted by Raquel Rodrigues dos Santos</div>
    <div class="footer-title">Digital Strategy & AI Transformation Specialist</div>
</div>
""", unsafe_allow_html=True)
