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
        with st.spinner("Analyzing your challenge and generating roadmap..."):
            try:
                prompt = f"""You are an elite AI consulting expert specializing in digital transformation and AI implementation. Your task is to create a detailed, specific, and actionable AI transformation roadmap.

USER'S SITUATION:
- Industry: {industry}
- Company Size: {company_size}
- Budget: {budget}
- Timeline: {timeline}
- Challenge: {challenge}

GENERATE A COMPREHENSIVE ROADMAP AS MARKDOWN (NOT JSON):

Use this structure:

# [Roadmap Title]

## Executive Summary
[One line summary]

## Overview
[2-3 paragraphs explaining the challenge and transformation approach]

## AI Opportunities

### 1. [Opportunity Name]
[2-3 sentences describing it]

**Implementation:**
Week 1-2: [specific tasks]
Week 3-4: [next tasks]
...

**Tools:** [Specific tech - e.g., TensorFlow, Snowflake, AWS SageMaker]
**Investment:** [Specific amount - e.g., $45K]
**Team:** [Team composition - e.g., 2 Data Scientists, 1 ML Engineer]
**ROI:** [Specific ROI - e.g., 180-220%]
**Business Impact:** [Specific impact with numbers]

### 2. [Opportunity Name]
[Same structure as above]

## Implementation Roadmap

### Phase 1: [Title]
**Duration:** X weeks | $YYK
**Focus:** [What this phase achieves]
**Milestones:**
- Week 1-2: [milestone]
- Week 3: [milestone]

**Activities:**
- [Activity 1]
- [Activity 2]

**Deliverables:**
- [Deliverable 1]
- [Deliverable 2]

**Investment:** $XXXK
**Team:** [Team composition]

### Phase 2: [Title]
[Same structure]

### Phase 3: [Title]
[Same structure]

## Key Risks & Mitigation

### Risk 1: [Risk description]
**Mitigation:** [Specific tactical mitigation strategy]

### Risk 2: [Risk description]
**Mitigation:** [Specific tactical mitigation strategy]

## Success Metrics
- [Metric 1 with numbers]
- [Metric 2 with numbers]
- [Metric 3 with numbers]

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
                    model="claude-haiku-4-5-20251001",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                response_text = ""
                
                # Extract text from response, skip thinking blocks
                for block in message.content:
                    if hasattr(block, 'type') and block.type == 'text':
                        response_text = block.text.strip()
                        break
                
                if not response_text:
                    raise ValueError("No text content found in response")
                
                # Display roadmap generated successfully
                st.success("Roadmap generated successfully!")
                st.divider()
                
                # Display the markdown roadmap directly
                st.markdown(response_text)
                
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
