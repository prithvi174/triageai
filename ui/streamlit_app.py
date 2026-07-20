import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/triage"

st.set_page_config(page_title="TriageAI", page_icon="🎫", layout= "centered")
st.title("TriageAI")
st.caption("LLM-powered IT support ticket classifier")

st.markdown("Paste an IT support ticket below and TriageAI will classify its category, priority, and suggested team.")

ticket_text= st.text_area(
    "ticket description",
    placeholder = "e.g. My laptop won't turn on at all, screen stays black even after charging overnight.",
    height = 120,
)

if st.button("Classify ticket", type="primary"):
    if not ticket_text.strip():
        st.warning("Please enter a ticket description first.")
    else:
        with st.spinner("Classifying...."):
            try:
                response = requests.post(API_URL, json={"ticket_text":ticket_text}, timeout=15)
                response.raise_for_status()
                result = response.json()

                col1, col2, col3 = st.columns(3)
                col1.metric("Category", result["category"])
                col2.metric("Priority", result["priority"])
                col3.metric("Suggested Team", result["suggested_team"])

                st.progress(result["confidence"], text=f"Confidence:{result['confidence']:.0%}")

                st.markdown("**Reasoning:**")
                st.info(result["reasoning"])
                
            except requests.exceptions.ConnectionError:
                st.error("Couldn't reach the TriageAI backend. Make sure the FastAPI server is running (`uvicorn app:app --reload`).")
            except requests.exceptions.HTTPError as e:
                st.error(f"Backend returned an error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
