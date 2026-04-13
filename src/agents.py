import google.generativeai as genai
import json
import time

def run_agentic_workflow(image, original_content, log_placeholder):
    """Executes the Multi-Agent Reflection Loop."""
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