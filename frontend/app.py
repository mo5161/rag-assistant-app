import streamlit as st

from api_client import send_query


st.set_page_config(
    page_title="Laptop Support RAG",
    page_icon="💻",
    layout="centered"
)


st.title("💻 Laptop Support Assistant")
st.write(
    "Ask a question about the laptop manuals and get "
    "an answer based on the retrieved documentation."
)


question = st.text_input(
    "Enter your question:",
    placeholder="Example: How do I charge the laptop?"
)


if st.button("Ask"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner("Searching the manuals..."):

                result = send_query(question)

            st.subheader("Answer")

            st.write(result["answer"])

            st.subheader("Sources")

            if result["sources"]:

                for source in result["sources"]:
                    st.write(f"- {source}")

            else:

                st.write("No sources were returned.")

        except Exception as error:

            st.error(
                f"Could not connect to the backend: {error}"
            )