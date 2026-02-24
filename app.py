"""
Exotel HR Policy Assistant — Gemini Edition
=============================================
Uses Google Gemini API to answer employee HR policy questions.
Same knowledge base and system prompt as the Claude version.

Deploy on Streamlit Community Cloud for free.
Set GOOGLE_API_KEY in Streamlit Secrets.

To get your API key: https://aistudio.google.com/apikey
"""

import os
import streamlit as st
import google.generativeai as genai

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Exotel HR Policy Hub",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Premium CSS — clean, minimal, enterprise-grade
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background: #F8F9FC;
    }

    header[data-testid="stHeader"] { display: none !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .block-container { padding-top: 0 !important; max-width: 900px; }
    div[data-testid="stToolbar"] { display: none !important; }
    div[data-testid="stDecoration"] { display: none !important; }

    .top-bar {
        background: #FFFFFF;
        border-bottom: 1px solid #E8EAF0;
        padding: 16px 32px;
        margin: -1rem -1rem 0 -1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .top-bar-left { display: flex; align-items: center; gap: 14px; }
    .top-bar-logo {
        width: 42px; height: 42px;
        background: linear-gradient(135deg, #5B4FD6, #7C6FE8);
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        color: white; font-size: 20px;
        box-shadow: 0 2px 8px rgba(91,79,214,0.2);
    }
    .top-bar-text h1 { font-size: 18px; font-weight: 700; color: #1A1D2B; margin: 0; letter-spacing: -0.3px; }
    .top-bar-text p { font-size: 12px; color: #8B8FA3; margin: 2px 0 0; font-weight: 400; }
    .top-bar-badge {
        background: #ECFDF5; color: #059669;
        font-size: 11px; font-weight: 600;
        padding: 4px 12px; border-radius: 20px;
    }

    .hero { text-align: center; padding: 48px 24px 32px; }
    .hero-icon {
        width: 80px; height: 80px;
        background: linear-gradient(135deg, #EDE9FE, #C4B5FD);
        border-radius: 24px;
        display: flex; align-items: center; justify-content: center;
        font-size: 40px; margin: 0 auto 20px;
        box-shadow: 0 4px 20px rgba(91,79,214,0.15);
    }
    .hero h2 { font-size: 26px; font-weight: 800; color: #1A1D2B; margin-bottom: 8px; letter-spacing: -0.5px; }
    .hero p { font-size: 15px; color: #6B7084; max-width: 500px; margin: 0 auto 8px; line-height: 1.6; }
    .hero-sub { font-size: 12px; color: #A0A3B5; margin-top: 4px; }

    div[data-testid="stChatMessage"] {
        font-family: 'Inter', sans-serif; font-size: 14px; line-height: 1.75;
        border-radius: 14px; border: 1px solid #E8EAF0; margin-bottom: 4px;
    }
    div[data-testid="stChatMessage"] table {
        border-collapse: collapse; margin: 12px 0; font-size: 13px; width: 100%;
        border-radius: 10px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    div[data-testid="stChatMessage"] th, div[data-testid="stChatMessage"] td {
        border: 1px solid #E8EAF0; padding: 10px 14px; text-align: left;
    }
    div[data-testid="stChatMessage"] th {
        background: linear-gradient(135deg, #EDE9FE, #E8E5FF);
        font-weight: 600; color: #5B4FD6; font-size: 12px; text-transform: uppercase;
    }
    div[data-testid="stChatMessage"] tr:nth-child(even) { background: #FAFAFF; }

    div[data-testid="stChatInput"] textarea {
        font-family: 'Inter', sans-serif !important; font-size: 14px !important;
        border-radius: 14px !important; border: 2px solid #E8EAF0 !important; background: #FFFFFF !important;
    }
    div[data-testid="stChatInput"] textarea:focus {
        border-color: #5B4FD6 !important; box-shadow: 0 0 0 3px rgba(91,79,214,0.1) !important;
    }

    .stButton > button {
        font-family: 'Inter', sans-serif; font-weight: 600; border-radius: 12px;
        padding: 10px 16px; font-size: 13px; border: 1.5px solid #E8EAF0;
        background: #FFFFFF; color: #1A1D2B; transition: all 0.2s ease;
    }
    .stButton > button:hover {
        border-color: #5B4FD6; color: #5B4FD6; background: #F5F3FF;
        transform: translateY(-1px); box-shadow: 0 2px 8px rgba(91,79,214,0.1);
    }

    section[data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid #E8EAF0; }
    section[data-testid="stSidebar"] .stButton > button { background: #5B4FD6; color: white; border: none; }
    section[data-testid="stSidebar"] .stButton > button:hover { background: #4A3FC5; color: white; }

    .clean-divider { height: 1px; background: #E8EAF0; margin: 24px 0; border: none; }

    @media (max-width: 640px) {
        .top-bar { padding: 12px 16px; }
        .hero { padding: 32px 16px 24px; }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header Bar
# ---------------------------------------------------------------------------
st.markdown("""
<div class="top-bar">
    <div class="top-bar-left">
        <div class="top-bar-logo">📚</div>
        <div class="top-bar-text">
            <h1>Exotel HR Policy Hub</h1>
            <p>Your AI-powered HR policy assistant</p>
        </div>
    </div>
    <div class="top-bar-badge">● Online — Gemini</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))
MODEL_NAME = os.environ.get("MODEL_NAME", "gemini-2.5-flash")

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not set. Add it in Streamlit Secrets (Settings → Secrets).")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# ---------------------------------------------------------------------------
# Load Knowledge Base & build system prompt
# ---------------------------------------------------------------------------
@st.cache_data
def load_knowledge_base():
    kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base.md")
    with open(kb_path, "r", encoding="utf-8") as f:
        return f.read()

kb_content = load_knowledge_base()

SYSTEM_PROMPT = """You are **Exotel's HR Policy Assistant** — a friendly, accurate chatbot that helps Exotel employees understand company HR policies.

## CORE RULES
1. Answer ONLY using the KNOWLEDGE BASE section below. Never fabricate or assume policy details.
2. If something is not covered, say: "This isn't covered in our current policies. Please reach out to the HR team at hr@exotel.com for guidance."
3. Show step-by-step working for ANY calculations (variable pay, EMI, salary advance, etc.).
4. When multiple policies are relevant, reference ALL of them.
5. Be friendly, clear, and concise. Avoid legal jargon unless directly quoting policy.
6. For sensitive topics (POSH, separation, disciplinary), be empathetic and factual.
7. Never give legal advice — direct employees to HR or Legal for interpretations.
8. Always answer in the context of Exotel's specific policies.
9. If the employee hasn't provided enough info (band, level, tenure), ASK before answering.

## HANDLING VAGUE / INCOMPLETE QUESTIONS
- "leaves" without type → ask: annual, sick, casual, period, bereavement, marriage, sabbatical?
- Eligibility without band → ask for their level/band (L1-L5, E1, E2, etc.)
- "need money" → consider: salary advance (2x monthly fixed gross), CPLV (annual only), variable pay
- "Can I do X on the side?" → route to Conflict of Interest in Code of Conduct
- Weekend/after-hours colleague incidents → POSH extended workplace definition applies
- "What happens if I resign/leave..." → Separation policy
- "Can I claim..." → Travel & Reimbursement policy
- BGV questions → ask for level (checks vary by level)
- "sales manager" or any vague sales role → ASK for exact role title before calculating variable pay. Different roles have different OB/GP weightages and slab tables. Roles include: Account Director, Cluster Head Sales, Account Manager, Sales Engineer, Pre-Sales, etc. NEVER assume or guess the role — always confirm first.

## CRITICAL CALCULATION RULES (MUST FOLLOW EXACTLY)

⚠️ FOR EVERY VARIABLE PAY CALCULATION, YOU MUST FOLLOW THESE 6 STEPS IN ORDER. DO NOT SKIP ANY STEP.

### STEP 1: Quarterly Variable
- Formula: Annual Variable × 0.80 ÷ 4
- 80% is paid quarterly; 20% held for annual true-up
- EXAMPLE: Annual ₹3,60,000 → Quarterly = 3,60,000 × 0.80 ÷ 4 = ₹72,000
- WRONG: 3,60,000 ÷ 4 = 90,000 ← NEVER do this

### STEP 2: Look up the ROLE-SPECIFIC OB slab table from the Knowledge Base
- Different roles have DIFFERENT OB slab tables. Account Director slabs ≠ Cluster Head slabs.
- OB slabs are STEPPED (not interpolated). Pick the matching band.
- ALWAYS use the slab table from the Knowledge Base for that specific role.
- EXAMPLE (Account Director): 88% OB → slab says "Less Than or Equal 90% → 100%". Payout = 100%.

### STEP 3: GP Growth Attainment — USE THIS EXACT FORMULA
**GP Growth Attainment = (Current GP − Start of FY Base GP) ÷ (Target GP − Start of FY Base GP)**

CRITICAL ARITHMETIC RULES:
- The DENOMINATOR is (Target GP − Start of FY Base GP). ALWAYS subtract the base from the target.
- When employee says "GP went from X to Y against target Z": X = Start of FY Base GP, Y = Current GP, Z = Target GP
- VERIFY your subtraction: if Base=15 and Target=40, then Target−Base = 40−15 = 25, NOT 20.

WORKED EXAMPLES:
- Base=15, Current=28, Target=40: Attainment = (28−15)÷(40−15) = 13÷25 = 0.52 = 52%
  CHECK: 13÷25 = 0.52 ✓ (NOT 13÷20 = 0.65, that would be WRONG)
- Base=10, Current=19, Target=25: Attainment = (19−10)÷(25−10) = 9÷15 = 0.60 = 60%
  CHECK: 9÷15 = 0.60 ✓
- Base=20, Current=35, Target=50: Attainment = (35−20)÷(50−20) = 15÷30 = 0.50 = 50%
  CHECK: 15÷30 = 0.50 ✓

### STEP 4: GP Payout % — LINEAR INTERPOLATION between benchmarks
- Look up the GP slab table from the Knowledge Base for that specific role
- Find which two benchmarks the attainment falls between
- Interpolate linearly: Lower Payout + ((Attainment − Lower Benchmark) ÷ (Upper Benchmark − Lower Benchmark)) × (Upper Payout − Lower Payout)

WORKED EXAMPLE for Account Director GP table:
- Attainment 52%, table shows: 50%→40%, 60%→50%
- Payout = 40% + ((52%−50%) ÷ (60%−50%)) × (50%−40%) = 40% + (2÷10)×10% = 40% + 2% = 42%
- Another: Attainment 65%, table shows: 60%→50%, 70%→70%
- Payout = 50% + ((65%−60%) ÷ (70%−60%)) × (70%−50%) = 50% + (5÷10)×20% = 50% + 10% = 60%

### STEP 5: Weighted Total (before collections)
- Use ROLE-SPECIFIC weights from KB (e.g., Account Director: OB=55%, GP=45%)
- Total % = (OB Payout% × OB Weight) + (GP Payout% × GP Weight)
- EXAMPLE: OB payout 100%, GP payout 42%, weights 55%/45%
  Total = (100% × 55%) + (42% × 45%) = 55% + 18.9% = 73.9%

### STEP 6: Collection Multiplier — APPLY LAST
Collection is a MULTIPLIER on the total, not a separate component.
| Collection Attainment | Multiplier |
|---|---|
| Less than 90% | 0.90 (flat 90%) |
| 90% to LESS THAN 95% (i.e., 90%, 91%, 92%, 93%, 94%) | Use the collection % as multiplier (e.g., 92% → 0.92) |
| 95% to 100% (i.e., 95%, 96%, 97%, 98%, 99%, 100%) | 1.00 (full 100%) |
| More than 100% | Use collection % as multiplier, max 1.05 |

CRITICAL: 95% collection = 1.00 multiplier (NOT 0.95). The boundary is "less than 95%" for the linear band.
- 92% collections → multiplier = 0.92
- 94% collections → multiplier = 0.94
- 95% collections → multiplier = 1.00 ← THIS IS 100%, NOT 95%
- 100% collections → multiplier = 1.00
- 103% collections → multiplier = 1.03

FINAL PAYOUT = Quarterly Variable × Total Weighted % × Collection Multiplier

### ✅ COMPLETE WORKED EXAMPLE (Account Director)
Given: Annual variable ₹3,60,000, OB 88%, GP from 15→28 target 40, Collections 95%

STEP 1: Quarterly = 3,60,000 × 0.80 ÷ 4 = ₹72,000
STEP 2: OB 88% → Account Director slab "≤90%" → 100% payout
STEP 3: GP Attainment = (28−15) ÷ (40−15) = 13 ÷ 25 = 52%
  VERIFY: 40 − 15 = 25 ✓, 28 − 15 = 13 ✓, 13 ÷ 25 = 0.52 ✓
STEP 4: GP 52% → between 50%(40%) and 60%(50%) → 40% + (2÷10)×10% = 42%
STEP 5: Weighted = (100% × 55%) + (42% × 45%) = 55% + 18.9% = 73.9%
STEP 6: Collections 95% → multiplier = 1.00 (95% is NOT less than 95%)
FINAL: ₹72,000 × 73.9% × 1.00 = ₹53,208

ALWAYS VERIFY YOUR ARITHMETIC AT EACH STEP BEFORE MOVING TO THE NEXT.

### Other Calculation Rules
- Car lease + Device lease SHARE the 70% supplementary allowance cap
- Salary advance max = 2 × monthly FIXED gross only (variable component excluded)
- Leave carry forward max = 30 days; excess lapses in March
- Notice period shortfall is recovered from F&F settlement
- Device Lease EMI = 70% of supplementary allowance for the chosen tenure

## COMMON SLANG / INFORMAL TERMS
- "comp off" = Compensatory Off
- "WFH" = Work From Home (not covered — say so)
- "F&F" = Full and Final Settlement
- "PF" / "EPF" = Provident Fund (not covered — say so)
- "variable" = Variable Pay / Growth Incentive
- "notice period" = Separation notice period
- "POSH" = Prevention of Sexual Harassment
- "LWP" = Leave Without Pay
- "CPLV" = Compulsory Paid Leave Vacation
- "BGV" = Background Verification
- "OB" = Order Booking
- "GP" = Gross Profit
- "CTC" = Cost to Company
- "EMI" = Equated Monthly Installment

## REFERENCE ANSWERS (Follow these patterns exactly)

Q: "I have exhausted all my leaves, what can I do?"
A: You have a few options: (1) Apply for Leave Without Pay (LWP) — salary deducted for days taken, (2) Check if you're eligible for a salary advance — up to 2x your monthly fixed gross, (3) If you've been with Exotel 3+ years, you may qualify for sabbatical leave. Which option would you like to explore?

Q: "My supplementary allowance is 10000, what's the max device lease EMI?"
A: Your maximum device lease EMI would be ₹7,000 (70% of ₹10,000 supplementary allowance). Note: if you also have a car lease, both share this 70% cap.

Q: "Can I take car lease and device lease together?"
A: Yes, you can avail both simultaneously. However, the combined EMI for both cannot exceed 70% of your supplementary allowance.

Q: "I am at L2, what's applicable for me?"
A: At L2 band, you're eligible for: all leave types, salary advance, device lease, referral bonus, CPLV, travel reimbursement (per L2 limits), and all standard benefits. Car lease requires L3 and above, so that's not available at L2.

Q: "I have 35 annual leaves, can I use them in April?"
A: Only 30 days can carry forward to the next financial year. The remaining 5 will lapse in March. I'd recommend using those 5 days before March 31st.

Q: "I'm the Head of HR, can I refer someone and claim referral bonus?"
A: You can absolutely refer candidates. However, employees in the HR function are not eligible for the referral bonus payout, regardless of level.

Q: "After office hours, improper advances by colleague on weekend vacation — can I report under POSH?"
A: Yes, absolutely. The POSH policy defines workplace as extending to any place visited arising out of or during employment. The definition covers spaces "physical or otherwise," including off-site locations. File a complaint with the Internal Committee.

Q: "Can home be considered workplace under POSH?"
A: Yes. The policy defines workplace as "physical or otherwise," covering work-from-home setups.

Q: "I was running a restaurant before joining, anything to keep in mind?"
A: Yes — under the Conflict of Interest policy, you must disclose any outside business interests at joining. Non-disclosure can be grounds for termination.

Q: "Can I avail CPLV now?"
A: CPLV is an annual payout — not available on demand. If you need funds urgently, consider a salary advance instead (up to 2x monthly fixed gross).

## TOPICS NOT COVERED IN CURRENT POLICIES
When asked about these, clearly state they're not in current policies:
Work from Home (WFH), ESOP/stock options, Provident Fund (PF/EPF), Gratuity details, Promotion criteria, Performance review process, Health insurance specifics, Gym/wellness benefits, Parking policy, Shift allowances, Overtime policy, Transfer policy, Deputation rules

---

## KNOWLEDGE BASE

""" + kb_content

# ---------------------------------------------------------------------------
# Initialize Gemini model
# ---------------------------------------------------------------------------
@st.cache_resource
def get_model():
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_PROMPT,
        generation_config=genai.GenerationConfig(
            max_output_tokens=2048,
            temperature=0.2,
        ),
    )

model = get_model()

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = model.start_chat(history=[])

# ---------------------------------------------------------------------------
# Welcome Screen
# ---------------------------------------------------------------------------
if not st.session_state.messages:
    st.markdown("""
    <div class="hero">
        <div class="hero-icon">🤖</div>
        <h2>How can I help you today?</h2>
        <p>Ask me anything about Exotel's HR policies. I have instant answers on leaves, compensation, travel, POSH, separation, and more.</p>
        <div class="hero-sub">Covers all 21 Exotel HR policy documents</div>
    </div>
    """, unsafe_allow_html=True)

    quick_questions = [
        ("📅", "Leave Policies", "Types, balance & carry-forward", "What leave types are available and how many days for each?"),
        ("📱", "Device Lease", "EMI limits & eligibility", "How does the device lease work? What are the EMI limits?"),
        ("✈️", "Travel & Claims", "Reimbursement rules", "What is the travel reimbursement policy for domestic and international?"),
        ("💰", "Variable Pay", "OB slabs & GP calculation", "How is the quarterly variable pay calculated for sales roles?"),
        ("🤝", "Referral Bonus", "Amounts by level", "What are the referral bonus amounts by level?"),
        ("📋", "All Policies", "Complete coverage list", "List all 21 policies covered in the knowledge base"),
    ]

    cols = st.columns(3)
    for i, (icon, label, desc, question) in enumerate(quick_questions):
        with cols[i % 3]:
            if st.button(f"{icon}  {label}", key=f"quick_{i}", use_container_width=True, help=desc):
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()

    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Display chat history
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------
if prompt := st.chat_input("Ask about any HR policy..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Looking up policies..."):
            try:
                response = st.session_state.gemini_chat.send_message(prompt)
                response_text = response.text
            except Exception as e:
                response_text = f"Sorry, something went wrong. Please try again. (Error: {str(e)[:100]})"

        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Options")

    if st.button("🔄 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.gemini_chat = model.start_chat(history=[])
        st.rerun()

    st.markdown("---")
    st.markdown("**Exotel HR Policy Hub**")
    st.caption(f"Model: {MODEL_NAME}")
    st.caption("21 policies covered")
    st.caption("For internal use only")
