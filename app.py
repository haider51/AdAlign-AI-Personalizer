import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# Import our custom modules
from src.scraper import scrape_landing_page
from src.agents import run_agentic_workflow

# --- CONFIGURATION ---
st.set_page_config(page_title="Troopod AI: Multi-Agent Personalizer", layout="wide")

# Initialize Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- SIDEBAR ---
with st.sidebar:
    st.title("🎯 Troopod AI PM")
    st.markdown("---")
    st.info("**Architecture:** Multi-Agent Reflection\n\n**Goal:** CRO 'Message Match'")
    st.subheader("🛠️ The Agents")
    st.caption("1. **Extractor:** Scrapes metadata.")
    st.caption("2. **Writer:** Personalizes copy.")
    st.caption("3. **Critic:** Audits brand safety.")

# --- UI COMPONENTS ---
def render_personalized_mockup(data):
    """Renders a visual mockup of the injected DOM elements."""
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 40px; 
        border-radius: 12px; 
        border: 2px dashed #ff4b4b; 
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        margin-top: 10px;
        margin-bottom: 20px;
    ">
        <p style="color: #ff4b4b; font-weight: bold; text-transform: uppercase; font-size: 12px; letter-spacing: 2px; margin-bottom: 20px;">
            ✨ Active Personalization Layer
        </p>
        <h1 style="color: #1f1f1f; font-size: 42px; margin-bottom: 20px; font-weight: 800;">
            {data.get('headline', '')}
        </h1>
        <p style="color: #4b4b4b; font-size: 18px; line-height: 1.6; max-width: 600px; margin: 0 auto 30px;">
            {data.get('sub_headline', '')}
        </p>
        <button style="
            background-color: #ff4b4b; 
            color: white; 
            border: none; 
            padding: 15px 35px; 
            font-size: 16px; 
            font-weight: bold; 
            border-radius: 6px; 
            box-shadow: 0 4px 6px rgba(255, 75, 75, 0.2);
        ">
            {data.get('cta_button', 'Learn More')}
        </button>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN UI ---
st.title("🎯 AI Landing Page Personalizer")
st.write("Turn any generic landing page into a personalized experience for your ad traffic.")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("1. Input Campaign Assets")
    uploaded_file = st.file_uploader("Upload Ad Creative", type=["jpg", "png", "jpeg"])
    target_url = st.text_input("Landing Page URL", placeholder="https://nike.com")
    
    if uploaded_file:
        st.image(Image.open(uploaded_file), caption="Ad Creative", use_container_width=True)

with col2:
    st.subheader("2. Optimization Output")
    
    if st.button("Generate Personalized Experience", type="primary"):
        if not uploaded_file or not target_url:
            st.error("Please provide both an ad image and a URL.")
        else:
            with st.expander("🛠️ Processing: View Agent Audit Trail", expanded=True):
                log_box = st.empty()
                with log_box.container():
                    st.write("📡 Scraping original webpage...")
                    original_data = scrape_landing_page(target_url)
                    
                    if "error" in original_data:
                        st.error(original_data["error"])
                    else:
                        # Call the external agent logic
                        raw_result, audit_log = run_agentic_workflow(Image.open(uploaded_file), original_data, st)
                        
                        try:
                            clean_json = raw_result.strip()
                            if "```json" in clean_json: clean_json = clean_json.split("```json")[1].split("```")[0]
                            elif "```" in clean_json: clean_json = clean_json.split("```")[1].split("```")[0]
                            data = json.loads(clean_json)
                            
                            st.success("✨ Personalization Engine Complete!")
                            st.markdown("---")
                            
                            # --- TABS UI ---
                            tab1, tab2 = st.tabs(["🖼️ Personalized Preview", "📈 Strategic Audit"])
                            
                            with tab1:
                                st.write("### Enhanced Landing Page Preview")
                                st.caption("This mockup represents how the personalized JSON strings are injected into the existing DOM.")
                                
                                # Call the custom UI function
                                render_personalized_mockup(data)
                                
                                st.write("---")
                                st.caption(f"⚖️ **Original Reference H1:** {original_data['headline']}")

                            with tab2:
                                st.metric("CRO Lift Score", f"{data.get('audit_score')}/100")
                                st.warning(f"**AI Gap Analysis:** {data.get('gap_analysis')}")
                                st.write("**Future Optimization Roadmap:**")
                                for rec in data.get('recommendations', []): st.write(f"- [ ] {rec}")
                                st.write("**Personalized FAQ Suggestion:**")
                                faq_data = data.get('faq_suggestion', 'No FAQ generated.')
                                if isinstance(faq_data, dict):
                                    for k, v in faq_data.items(): st.info(f"**{k.upper()}:** {v}")
                                else:
                                    st.info(faq_data)
                                
                        except Exception as e:
                            st.error(f"Logic Error: {e}")
                            st.code(raw_result)
