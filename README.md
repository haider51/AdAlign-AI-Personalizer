# 🎯 AdAlign AI: Multi-Agent Personalization Engine

> **Live Demo:** [PASTE_YOUR_STREAMLIT_LINK_HERE]  
> **Strategic Product Brief:** [PASTE_YOUR_GOOGLE_DOC_LINK_HERE]

AdAlign AI is a high-fidelity personalization prototype developed for the **Troopod AI PM Assignment**. It solves the "Ad-to-Page" message mismatch problem by using a Multi-Agent Reflection architecture to intelligently rewrite landing page elements in real-time based on visual ad creative context.

---

## 🚀 The Core Problem: "Message Mismatch"
In performance marketing, the biggest cause of high bounce rates is a lack of continuity. When a user clicks a specific ad (e.g., about "Speed") but lands on a generic page (e.g., about "Quality"), conversion drops. 

**AdAlign AI** automates "Message Match" by ensuring the landing page instantly mirrors the specific value proposition found in the ad creative.

## 🧠 System Architecture: Multi-Agent Reflection
To avoid the common pitfalls of single-prompt AI (hallucinations, broken UI, and generic copy), this project implements a **Reflection Pattern** inspired by LangGraph.

### The Agent Workflow:
1. **The Extractor (Scraper):** Parses the DOM of the target URL to identify original H1, Subheadline, and CTA nodes.
2. **The Vision Writer (Creative Agent):** Uses Gemini 1.5 Flash Vision to analyze the Ad Creative for sentiment, core offer, and brand energy.
3. **The Critic (Auditor):** Compares the Writer's draft against the "Ground Truth" (original ad and site data). It checks for hallucinations (invented facts) and brand safety.
4. **The Refiner (Correction Loop):** If the Critic identifies errors, this agent executes a self-correction loop to rewrite the JSON output until it meets the quality threshold.

## 🛠️ Key Product Features
- **Multimodal Context:** Simultaneous processing of Ad Images and Webpage text.
- **Strategic Audit Hub:** Goes beyond simple text replacement by providing a "Predictive Lift Score," Gap Analysis, and an AI-generated optimization checklist.
- **DOM-Preservation Logic:** Designed to "enhance" rather than "replace." The prototype demonstrates how specific nodes (H1, CTA) are targeted for replacement while keeping the brand's base CSS and layout intact.
- **Agentic Transparency:** A real-time audit trail shows the user exactly which agent is working and why decisions were made.

## 📦 Tech Stack
- **LLM Core:** Google Gemini 1.5 Flash (Multimodal)
- **Frontend:** Streamlit (Python-based Web Framework)
- **Logic:** Python 3.10+, BeautifulSoup4 (Web Scraping)
- **Design Pattern:** Iterative Agentic Reflection

## 🔧 Local Setup
1. Clone the repository:
   git clone https://github.com/your-username/AdAlign-AI-Personalizer.git
   
2. Install requirements:
   pip install -r requirements.txt
   
3. Run the application:
   streamlit run app.py

## 📈 Future Roadmap (Phase 2)
- **Visual Style Matching:** Extracting HEX colors and Font-weights from ads to update page CSS.
- **Browser-Based Injection:** A Chrome Extension to preview these changes directly on the live site via a "Shadow DOM."
- **Multi-Variant A/B Testing:** Automatically generating 3 variants (Urgency, Benefit-driven, Social Proof) for automated traffic split testing.

---
*Created for the Troopod AI PM Internship Assignment.*
