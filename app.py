import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from PIL import Image
import json
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Troopod AI: Multi-Agent Personalizer", layout="wide")

# Initialize Gemini API securely from Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize Gemini API
with st.sidebar:
    st.title("🎯 Troopod AI PM")
    st.markdown("---")
    
    st.info("""
    **Architecture:** Multi-Agent Reflection  
    **Framework:** LangGraph-inspired Cycles  
    **Goal:** CRO 'Message Match'
    """)
    
    st.subheader("🛠️ The Agents")
    st.caption("1. **Extractor:** Scrapes metadata.")
    st.caption("2. **Writer:** Personalizes copy.")
    st.caption("3. **Critic:** Audits brand safety.")

# --- SCRAPER ENGINE ---
def scrape_landing_page(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return {"error": f"Site blocked (Status: {response.status_code})"}
        
        soup = BeautifulSoup(response.content, 'html.parser')
        h1 = soup.find('h1').text.strip() if soup.find('h1') else "Welcome"
        p_text = soup.find('p').text.strip()[:200] if soup.find('p') else "Premium product."
        
        return {"headline": h1, "sub_headline": p_text, "cta_button": "Learn More"}
    except Exception as e:
        return {"error": str(e)}

# --- MULTI-AGENT WORKFLOW ---
def run_agentic_workflow(image, original_content, log_placeholder):
    # Using 3-flash for the best balance of speed and logic
    model = genai.GenerativeModel('gemini-3-flash-preview')
    
    # STAGE 1: WRITER
    log_placeholder.write("🤖 **Agent 1 (Writer):** Analyzing Ad context and rewriting copy...")
    writer_prompt = f"Personalize this page for this Ad. Page: {json.dumps(original_content)}. Return ONLY JSON: headline, sub_headline, cta_button, audit_score, gap_analysis, recommendations, faq_suggestion."
    first_draft = model.generate_content([writer_prompt, image]).text
    time.sleep(1)
    
    # STAGE 2: CRITIC
    log_placeholder.write("🧐 **Agent 2 (Critic):** Auditing for hallucinations & safety...")
    critic_prompt = f"Audit this draft for hallucinations vs the original page: {first_draft}. Return 'PASS' or 'FAIL: [Reason]'."
    critic_review = model.generate_content([critic_prompt, image]).text
    time.sleep(1)
    
    # STAGE 3: SELF-CORRECTION
    if "PASS" in critic_review.upper():
        log_placeholder.write("✅ **Audit Passed.** Outputting final results.")
        return first_draft, "Pass"
    else:
        log_placeholder.write("🔄 **Agent 3 (Refiner):** Fixing errors found by Critic...")
        refine_prompt = f"Fix this draft: {first_draft}. Feedback: {critic_review}. Return JSON."
        final_draft = model.generate_content([refine_prompt, image]).text
        return final_draft, f"Refined: {critic_review[:50]}"

# --- VIRTUAL DOM RENDERER (The 'Enhanced' Page Mockup) ---
def render_personalized_mockup(data):
    # This creates a visual "Hero Section" that looks like a real website
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 60px 40px; 
        border-radius: 15px; 
        border: 2px dashed #ff4b4b; 
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    ">
        <p style="color: #ff4b4b; font-weight: bold; text-transform: uppercase; font-size: 12px; letter-spacing: 2px;">
            Personalized Experience Layer Active
        </p>
        <h1 style="color: #1f1f1f; font-size: 48px; margin-bottom: 20px;">
            {data['headline']}
        </h1>
        <p style="color: #4b4b4b; font-size: 18px; line-height: 1.6; max-width: 600px; margin: 0 auto 30px;">
            {data['sub_headline']}
        </p>
        <button style="
            background-color: #ff4b4b; 
            color: white; 
            border: none; 
            padding: 15px 35px; 
            font-size: 18px; 
            font-weight: bold; 
            border-radius: 5px; 
            cursor: pointer;
        ">
            {data['cta_button']}
        </button>
    </div>
    <p style="text-align: center; font-size: 12px; color: #888; margin-top: 10px;">
        Note: In production, these elements are injected directly into the existing URL's DOM.
    </p>
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
            # Create the log expander first
            with st.expander("🛠️ Processing: View Agent Audit Trail", expanded=True):
                log_box = st.empty()
                with log_box.container():
                    st.write("📡 Scraping original webpage...")
                    original_data = scrape_landing_page(target_url)
                    
                    if "error" in original_data:
                        st.error(original_data["error"])
                    else:
                        # Run agents and get results
                        raw_result, audit_log = run_agentic_workflow(Image.open(uploaded_file), original_data, st)
                        
                        try:
                            # Parse JSON
                            clean_json = raw_result.strip()
                            if "```json" in clean_json: clean_json = clean_json.split("```json")[1].split("```")[0]
                            elif "```" in clean_json: clean_json = clean_json.split("```")[1].split("```")[0]
                            data = json.loads(clean_json)
                            
                            # Success Message
                            st.success("✨ Personalization Engine Complete!")
                            
                            # --- RESULTS ---
                            st.markdown("---")
                            tab1, tab2 = st.tabs(["🖼️ Personalized Preview", "📈 Strategic Audit"])
                            
                            with tab1:
                                st.write("### Enhanced Landing Page Preview")
                                render_personalized_mockup(data) # This shows the beautiful mockup
                                
                                st.write("---")
                                st.caption("⚖️ **Original for reference:**")
                                st.caption(f"H1: {original_data['headline']}")

                            with tab2:
                                st.metric("CRO Lift Score", f"{data.get('audit_score')}/100")
                                st.warning(f"**AI Gap Analysis:** {data.get('gap_analysis')}")
                                
                                st.write("**Future Optimization Roadmap:**")
                                for rec in data.get('recommendations', []):
                                    st.write(f"- [ ] {rec}")
                                
                                st.write("**Personalized FAQ Suggestion:**")
                                faq_data = data.get('faq_suggestion', 'No FAQ generated.')
                                
                                # Safely render the FAQ whether the AI returns a dictionary or a string
                                if isinstance(faq_data, dict):
                                    # If the AI perfectly formatted it as Q&A
                                    for k, v in faq_data.items():
                                        st.info(f"**{k.upper()}:** {v}")
                                else:
                                    # If the AI just returned a normal text string
                                    st.info(faq_data)
                                    
                        except Exception as e:
                            st.error(f"Logic Error: {e}")
                            st.code(raw_result)  
