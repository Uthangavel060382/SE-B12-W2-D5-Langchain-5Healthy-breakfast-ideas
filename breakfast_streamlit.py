
import os
import streamlit as st

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


# STEP 1: Load the API key
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


# STEP 2: Configure Streamlit
st.set_page_config(
    page_title="AI Breakfast Generator",
    page_icon="🥗",
    layout="centered"
)

st.title("🥗 AI Healthy Breakfast Generator")
st.caption("Built with Python, LangChain and OpenAI")


# STEP 3: Validate API key
if not api_key:
    st.error("OPENAI_API_KEY is missing from .env")
    st.stop()


# STEP 4: Accept user preferences
diet = st.selectbox(
    "Select dietary preference",
    ["Vegetarian", "Non-vegetarian", "Vegan"]
)

temperature = st.slider(
    "Model Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.1
)

st.info(
    "Temperature 0 produces more consistent answers, "
    "but identical outputs are not guaranteed."
)


# STEP 5: Initialize model
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=temperature,
    api_key=api_key
)


# STEP 6: Create the prompt
prompt = f"""
Suggest exactly 5 healthy breakfast ideas.

Dietary preference: {diet}

Requirements:
- Include protein-rich and fiber-rich foods.
- Minimize added sugar.
- Follow the selected dietary preference.
- Provide exactly 5 ideas.
- Number the ideas from 1 to 5.
- Write exactly one idea per line.
- Do not include a title or introduction.
- Do not include a conclusion.
"""


# STEP 7: Initialize Streamlit session state
if "results" not in st.session_state:
    st.session_state.results = []


# STEP 8: Generate breakfast ideas
if st.button("Generate Breakfast Ideas", type="primary"):

    with st.spinner("Generating healthy breakfast ideas..."):

        try:
            # Invoke the LangChain model
            response = llm.invoke(prompt)

            # Extract only the message text
            answer = response.content

            # Save for comparison
            st.session_state.results.append({
                "diet": diet,
                "temperature": temperature,
                "answer": answer
            })

        except Exception as error:
            st.error(f"Error: {error}")


# STEP 9: Display generated results
if st.session_state.results:

    st.subheader("Generated Breakfast Ideas")

    latest = st.session_state.results[-1]

    st.text(latest["answer"])

    st.caption(
        f"Diet: {latest['diet']} | "
        f"Temperature: {latest['temperature']}"
    )


# STEP 10: Compare the last two executions
if len(st.session_state.results) >= 2:

    st.subheader("Compare Last Two Runs")

    run1 = st.session_state.results[-2]
    run2 = st.session_state.results[-1]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Previous Run**")
        st.text(run1["answer"])

    with col2:
        st.markdown("**Latest Run**")
        st.text(run2["answer"])

    if (
        run1["diet"] == run2["diet"]
        and run1["temperature"] == run2["temperature"]
    ):
        if run1["answer"] == run2["answer"]:
            st.success("Both results are identical.")
        else:
            st.info("The two results are different.")
    else:
        st.warning(
            "Preferences changed between runs. "
            "Use the same settings for a fair comparison."
        )


# STEP 11: Clear saved results
if st.button("Clear Results"):
    st.session_state.results = []
    st.rerun()
