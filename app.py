import streamlit as st
import time
import json
import os
from groq import Groq
from personalities import PERSONALITIES

# Page Config
st.set_page_config(
    page_title="AgentIQ - Premium Multi-Agent Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Custom CSS Injection
st.markdown("""
<style>
    /* Google Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Title and Header styling */
    .main-title {
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        color: #94A3B8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Glassmorphism suggested prompts cards */
    .suggestion-card {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .suggestion-card:hover {
        background: rgba(30, 41, 59, 0.7);
        border-color: #00F2FE;
        transform: translateY(-2px);
    }
    
    /* Badge styling */
    .badge {
        background-color: #1E293B;
        border: 1px solid #334155;
        color: #00F2FE;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    /* Chat window custom borders */
    .stChatMessage {
        background-color: rgba(30, 41, 59, 0.2);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 15px;
        margin-bottom: 10px;
    }
    
    /* Footer styling */
    .footer-text {
        text-align: center;
        color: #64748B;
        font-size: 0.85rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        padding-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE SETUP -----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_personality" not in st.session_state:
    st.session_state.selected_personality = "Math Teacher"
if "telemetry" not in st.session_state:
    st.session_state.telemetry = {
        "last_latency_ms": 0.0,
        "total_requests": 0,
        "last_word_count": 0
    }
if "compare_logs" not in st.session_state:
    st.session_state.compare_logs = []

# API Key — loaded securely from .streamlit/secrets.toml (local)
# or Streamlit Cloud Secrets dashboard (production). Never hardcoded.
def get_groq_client():
    key = ""
    # 1. Try Streamlit secrets first (local secrets.toml or Streamlit Cloud)
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        pass
    # 2. Fallback to environment variable
    if not key:
        key = os.getenv("GROQ_API_KEY", "")
    if not key:
        return None
    try:
        return Groq(api_key=key)
    except Exception as e:
        st.error(f"Failed to initialize Groq Client: {e}")
        return None

# Sidebar - Configuration Panel
st.sidebar.image("https://img.icons8.com/?size=100&id=dJ46wPls9v2K&format=png", width=80)
st.sidebar.markdown("### 🛠️ Configuration Panel")

client = get_groq_client()

# Model Selection
model_options = {
    "Llama 3.3 70B (Versatile)": "llama-3.3-70b-versatile",
    "Llama 3.1 8B (Instant)": "llama-3.1-8b-instant",
    "Mixtral 8x7B (Reasoning)": "mixtral-8x7b-32768",
    "Gemma 2 9B (Lightweight)": "gemma2-9b-it"
}
selected_model_label = st.sidebar.selectbox(
    "Select AI Model",
    options=list(model_options.keys()),
    index=0
)
model_name = model_options[selected_model_label]

# Hyperparameters Expander
with st.sidebar.expander("⚙️ Advanced Model Settings", expanded=False):
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3, step=0.05, 
                            help="Lower values make the output more structured and adhere strictly to guardrails.")
    max_tokens = st.slider("Max Tokens", min_value=128, max_value=4096, value=2048, step=128)

# Reset Button
if st.sidebar.button("🧹 Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.session_state.compare_logs = []
    st.toast("Chat history cleared!")
    st.rerun()

# Dynamic sidebar info based on personality selection
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Live Analytics")
st.sidebar.metric(label="Response Latency", value=f"{st.session_state.telemetry['last_latency_ms']:.2f} ms")
st.sidebar.metric(label="Response Words", value=f"{st.session_state.telemetry['last_word_count']} words")
st.sidebar.metric(label="Total Queries", value=st.session_state.telemetry['total_requests'])

# Header
st.markdown("<div class='main-title'>AgentIQ Hub</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Autonomous, restricted-personality agents engineered to enforce domain boundaries with maximum precision.</div>", unsafe_allow_html=True)

if not client:
    st.warning("⚠️ **Groq API Key Required**: Please provide a Groq API key in the sidebar configuration to begin chatting.")
    st.info("You can get a free API key at [Groq Console](https://console.groq.com/).")
    st.stop()

# Tabs definition
tab_chat, tab_comparison, tab_sandbox = st.tabs(["💬 Interactive Chat", "⚔️ Agent Comparison Mode", "🧪 Prompt Sandbox"])

# ----------------- TAB 1: INTERACTIVE CHAT -----------------
with tab_chat:
    col_left, col_right = st.columns([3, 1])
    
    with col_right:
        st.markdown("### Choose Agent Persona")
        selected_p = st.selectbox(
            "Active Agent",
            options=list(PERSONALITIES.keys()),
            key="current_p_select"
        )
        
        # Reset conversation if personality changes
        if selected_p != st.session_state.selected_personality:
            st.session_state.selected_personality = selected_p
            st.session_state.messages = []
            st.toast(f"Switched to {selected_p}! Cleared previous context.")
            st.rerun()
            
        p_info = PERSONALITIES[st.session_state.selected_personality]
        
        # Details card
        st.markdown(f"""
        <div style="background-color:#1E293B; border-radius:12px; padding:15px; border-left: 5px solid #00F2FE;">
            <h4 style="margin:0; font-size:1.2rem;">{p_info['icon']} {st.session_state.selected_personality}</h4>
            <p style="font-size:0.9rem; color:#94A3B8; margin-top:8px; margin-bottom:0;">{p_info['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Export Actions
        st.markdown("### Export Conversations")
        if st.session_state.messages:
            # Markdown text compile
            md_export = f"# Chat Log with {st.session_state.selected_personality}\nModel: {selected_model_label}\n\n"
            for msg in st.session_state.messages:
                role = "User" if msg["role"] == "user" else st.session_state.selected_personality
                md_export += f"### **{role}** ({msg.get('timestamp', 'N/A')}):\n{msg['content']}\n\n---\n\n"
            
            st.download_button(
                label="📥 Download Markdown Log",
                data=md_export,
                file_name=f"chat_log_{st.session_state.selected_personality.replace(' ', '_').lower()}.md",
                mime="text/markdown",
                use_container_width=True
            )
            
            json_export = json.dumps({
                "personality": st.session_state.selected_personality,
                "model": model_name,
                "messages": st.session_state.messages
            }, indent=2)
            
            st.download_button(
                label="📥 Download JSON Log",
                data=json_export,
                file_name=f"chat_log_{st.session_state.selected_personality.replace(' ', '_').lower()}.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.caption("No messages to export yet.")
            
    with col_left:
        st.markdown(f"### Chatting with {p_info['icon']} **{st.session_state.selected_personality}**")
        
        # Suggestions Section
        st.markdown("<span class='badge'>Quick Suggestions</span>", unsafe_allow_html=True)
        s_cols = st.columns(3)
        clicked_suggestion = None
        for idx, sug in enumerate(p_info["suggestions"]):
            with s_cols[idx]:
                if st.button(sug, key=f"sug_{idx}", use_container_width=True):
                    clicked_suggestion = sug
                    
        # Render historical chat messages
        for message in st.session_state.messages:
            avatar_icon = "👤" if message["role"] == "user" else p_info["icon"]
            with st.chat_message(message["role"], avatar=avatar_icon):
                st.markdown(message["content"])
                
        # Formulate query
        prompt = st.chat_input("Ask me a question...")
        if clicked_suggestion:
            prompt = clicked_suggestion
            
        if prompt:
            # Add user message
            user_time = time.strftime("%H:%M:%S")
            st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": user_time})
            
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)
                
            # Process AI Stream
            with st.chat_message("assistant", avatar=p_info["icon"]):
                # Prepare messages array with System Prompt
                api_messages = [{"role": "system", "content": p_info["system_prompt"]}]
                for msg in st.session_state.messages:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})
                    
                start_time = time.time()
                response_placeholder = st.empty()
                full_response = ""
                
                try:
                    # Stream API response
                    stream = client.chat.completions.create(
                        model=model_name,
                        messages=api_messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        stream=True
                    )
                    
                    for chunk in stream:
                        if chunk.choices[0].delta.content is not None:
                            full_response += chunk.choices[0].delta.content
                            response_placeholder.markdown(full_response + "▌")
                    
                    response_placeholder.markdown(full_response)
                    
                    # Compute latency and counts
                    end_time = time.time()
                    latency_ms = (end_time - start_time) * 1000
                    word_count = len(full_response.split())
                    
                    # Store response
                    asst_time = time.strftime("%H:%M:%S")
                    st.session_state.messages.append({"role": "assistant", "content": full_response, "timestamp": asst_time})
                    
                    # Save telemetry
                    st.session_state.telemetry["last_latency_ms"] = latency_ms
                    st.session_state.telemetry["last_word_count"] = word_count
                    st.session_state.telemetry["total_requests"] += 1
                    
                    st.rerun() # Refresh layout to update sidebar metrics cleanly
                    
                except Exception as e:
                    response_placeholder.error(f"API Error: {e}")

# ----------------- TAB 2: AGENT COMPARISON MODE -----------------
with tab_comparison:
    st.markdown("### Compare Two Personalities Side-by-Side")
    st.caption("Enter a single query to see how different personalities answer under their strict domain rules.")
    
    comp_col1, comp_col2 = st.columns(2)
    with comp_col1:
        p1 = st.selectbox("Select Agent A", options=list(PERSONALITIES.keys()), index=3) # Default Chef
    with comp_col2:
        p2 = st.selectbox("Select Agent B", options=list(PERSONALITIES.keys()), index=1) # Default Doctor
        
    compare_prompt = st.text_input("Enter Prompt for Comparison (e.g. 'Give me an omelette recipe' or 'Solve x^2 = 9')", placeholder="Type prompt here...")
    run_compare = st.button("🚀 Compare Responses", use_container_width=True)
    
    if run_compare and compare_prompt:
        col_res1, col_res2 = st.columns(2)
        
        # Agent A response
        with col_res1:
            st.markdown(f"#### {PERSONALITIES[p1]['icon']} {p1} Output")
            p1_messages = [
                {"role": "system", "content": PERSONALITIES[p1]["system_prompt"]},
                {"role": "user", "content": compare_prompt}
            ]
            response_box1 = st.empty()
            response_box1.info("Thinking...")
            
            try:
                start1 = time.time()
                comp_stream1 = client.chat.completions.create(
                    model=model_name,
                    messages=p1_messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )
                full1 = ""
                for chunk in comp_stream1:
                    if chunk.choices[0].delta.content is not None:
                        full1 += chunk.choices[0].delta.content
                        response_box1.markdown(full1 + "▌")
                response_box1.markdown(full1)
                latency1 = (time.time() - start1) * 1000
                st.caption(f"Latency: {latency1:.2f} ms | Words: {len(full1.split())}")
            except Exception as e:
                response_box1.error(f"Error: {e}")
                
        # Agent B response
        with col_res2:
            st.markdown(f"#### {PERSONALITIES[p2]['icon']} {p2} Output")
            p2_messages = [
                {"role": "system", "content": PERSONALITIES[p2]["system_prompt"]},
                {"role": "user", "content": compare_prompt}
            ]
            response_box2 = st.empty()
            response_box2.info("Thinking...")
            
            try:
                start2 = time.time()
                comp_stream2 = client.chat.completions.create(
                    model=model_name,
                    messages=p2_messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )
                full2 = ""
                for chunk in comp_stream2:
                    if chunk.choices[0].delta.content is not None:
                        full2 += chunk.choices[0].delta.content
                        response_box2.markdown(full2 + "▌")
                response_box2.markdown(full2)
                latency2 = (time.time() - start2) * 1000
                st.caption(f"Latency: {latency2:.2f} ms | Words: {len(full2.split())}")
            except Exception as e:
                response_box2.error(f"Error: {e}")

# ----------------- TAB 3: PROMPT SANDBOX -----------------
with tab_sandbox:
    st.markdown("### 🧪 Inspect & Tweak System Prompt Rules")
    st.caption("Here you can inspect the exact instructions being sent to the LLM to control its domain limits.")
    
    sandbox_p = st.selectbox("Inspect Personality rules for:", options=list(PERSONALITIES.keys()))
    
    # Text area for system prompt modification
    modified_prompt = st.text_area(
        "Current System Prompt Directive", 
        value=PERSONALITIES[sandbox_p]["system_prompt"],
        height=250,
        help="You can review the instructions. Modifying this prompt in the sandbox does not change the core app state unless saved."
    )
    
    if st.button("🔄 Restore Default Rules"):
        st.rerun()

st.markdown("<div class='footer-text'>Built with Streamlit & Groq API • Optimized for Streamlit Cloud Deployment</div>", unsafe_allow_html=True)
