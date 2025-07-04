import streamlit as st
import os
from agent import create_agent
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

# Load environment variables from .env file
load_dotenv()

def main():
    """
    Main function to run the Streamlit application.
    """
    st.set_page_config(page_title="Novelix", page_icon="💡")
    st.title("💡 Novelix", help="Research Idea Generation AI Agent")

    # --- Sidebar Configuration ---
    with st.sidebar:
        st.title("Setting")

        # Framework selection
        framework_options = [
            "Auto selection (Let the agent decide)",
            "BeHEMoTh | Be: behavior of interest, H: health context, E: exclusions, MoTh: models or theories | Questions about theories, health behavior",
            "CHIP | Context, How, Issues, Population | Psychology, qualitative research",
            "CIMO | Context, Intervention, Mechanisms, Outcomes | Management, business, administration",
            "CLIP | Client group, Location of provided service, Improvement/Information/Innovation, Professionals | Librarianship, management, policy",
            "COPES | Client-Oriented, Practical, Evidence, Search | Social work, health care, nursing",
            "ECLIPSE | Expectation, Client, Location, Impact, Professionals, Service | Management, services, policy, social care",
            "PEO | Population, Exposure, Outcome | Qualitative research",
            "PECODR | Patient/population/problem, Exposure, Comparison, Outcome, Duration, Results | Medicine, clinical research",
            "PerSPECTiF | Perspective, Setting, Phenomenon of interest/Problem, Environment, Comparison, Time/Timing, Findings | Qualitative research",
            "PESICO | Person, Environments, Stakeholders, Intervention, Comparison, Outcome | Augmentative and alternative communication",
            "PICO | Patient, Intervention, Comparison, Outcome | Clinical medicine, evidence-based practice",
            "PICO+ | Patient, Intervention, Comparison, Outcome, +context, patient values, preferences | Occupational therapy",
            "PICOC | Patient, Intervention, Comparison, Outcome, Context | Social sciences",
            "PICOS | Patient, Intervention, Comparison, Outcome, Study Type | Medicine, systematic reviews",
            "PICOT | Patient, Intervention, Comparison, Outcome, Time | Education, health care",
            "PICO (for diagnostic tests) | Patient/participants/population, Index tests, Comparator/reference tests, Outcome | Diagnostic questions, clinical research",
            "PIPOH | Population, Intervention, Professionals, Outcomes, Health care setting/context | Screening, health care",
            "PCC | Population, Concept, Context | Scoping reviews",
            "PPICO | Population (with two descriptors), Intervention, Comparison, Outcome | Complex population studies, clinical research",
            "PI_O | Population, Intervention, Outcome (without comparison) | Clinical research, no comparison needed",
            "ProPheT | Problem, Phenomenon of interest, Time | Social sciences, qualitative, library science",
            "SPICE | Setting, Perspective, Interest, Comparison, Evaluation | Qualitative research, evaluating outcomes",
            "SPIDER | Sample, Phenomenon of interest, Design, Evaluation, Research type | Health, qualitative or mixed methods research",
            "WWH | Who, What, How | General research, not discipline-specific",
        ]
        selected_framework = st.selectbox(
            "Choose a Research Framework",
            framework_options,
            index=0,
            help="Select the framework to guide the research idea generation."
        )

        # LLM Configuration
        st.title("LLM Configuration")
        model_name = st.selectbox(
            "Select LLM Model",
            ("gpt-4.1-nano", "gpt-4.1-mini", "gpt-4.1", "gpt-4o-mini", "gpt-4o"),
            index=0,
            help="Choose the underlying language model for the agent."
        )
        temperature = st.slider(
            "Set Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Controls the randomness of the output. Lower values are more deterministic."
        )

    # --- API Key Check ---
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        st.error("🚨 API keys not found! Please set your OPENAI_API_KEY and TAVILY_API_KEY in a .env file.")
        st.info("Create a file named `.env` in the `Novelix` directory and add the necessary keys.")
        st.stop()

    # --- Agent and Chat History Initialization ---
    # Re-initialize the agent if model or temperature settings change.
    if ("agent_executor" not in st.session_state or
        st.session_state.get("model_name") != model_name or
        st.session_state.get("temperature") != temperature):
        
        with st.spinner("Configuring new agent..."):
            st.session_state.agent_executor = create_agent(model_name=model_name, temperature=temperature)
        
        st.session_state.model_name = model_name
        st.session_state.temperature = temperature
        # Reset chat history when settings change, as the new agent has no context.
        st.session_state.messages = [{"role": "assistant", "content": f"Hello! I'm here to help you generate research ideas. What topics are you interested in?"}]
        # Force a rerun to display the new welcome message immediately
        st.rerun()

    # --- Chat Interface ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Enter your topics or response:"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            thinking_expander = st.expander("Thinking...", expanded=True)
            response_placeholder = st.empty()
            assistant_response_content = ""

            try:
                chat_history = [
                    HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"])
                    for msg in st.session_state.messages[:-1]
                ]

                agent_input = {
                    "input": user_input,
                    "chat_history": chat_history,
                    "framework_choice": selected_framework
                }

                response_generator = st.session_state.agent_executor.stream(agent_input)
                for chunk in response_generator:
                    if "actions" in chunk:
                        for action in chunk["actions"]:
                            thinking_expander.write(f"**Calling Tool:** `{action.tool}` with input `{action.tool_input}`")
                    elif "steps" in chunk:
                        for step in chunk["steps"]:
                            thinking_expander.write(f"**Tool Output:** `{step.observation}`")
                    elif "output" in chunk:
                        assistant_response_content += chunk["output"]
                        response_placeholder.markdown(assistant_response_content + "▌")
                
                response_placeholder.markdown(assistant_response_content)

            except Exception as e:
                st.error(f"An error occurred: {e}")
                assistant_response_content = "I encountered an error. Please try again."
                response_placeholder.markdown(assistant_response_content)

            st.session_state.messages.append({"role": "assistant", "content": assistant_response_content})

if __name__ == "__main__":
    main()
