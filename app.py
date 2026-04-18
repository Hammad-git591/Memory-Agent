import uuid
import streamlit as st
from agent import agent, save_message
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Memory Agent", layout="wide")
st.title("AI Memory Agent")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

session_id = st.session_state.session_id

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    save_message(session_id, "user", user_input)

    if "confirm" in user_input.lower():
        choice = st.radio("Confirm this action?", ["Haan", "Nahi"], key=f"confirm_{session_id}")
        if choice == "Nahi":
            assistant_reply = "Okay, action cancelled."
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            with st.chat_message("assistant"):
                st.markdown(assistant_reply)
            save_message(session_id, "assistant", assistant_reply)
            st.stop()

    with st.spinner("Soch raha hoon..."):
        try:
            response = agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config={"configurable": {"thread_id": session_id}}
            )
            final = response["messages"][-1].content

            if isinstance(final, list):
                final = " ".join([
                    item["text"]
                    for item in final
                    if isinstance(item, dict) and "text" in item
                ])
        except Exception:
            final = "Server busy hai, thodi der baad try karo! 🙏"

    st.session_state.messages.append({"role": "assistant", "content": final})
    with st.chat_message("assistant"):
        st.markdown(final)

    save_message(session_id, "assistant", final)