# app.py
import streamlit as st
from graph.review_graph import run_review
from datetime import datetime

st.set_page_config(page_title="AI Code Reviewer",
                   page_icon="🤖", layout="wide")

st.title("🤖 AI Code Review Agent")
st.caption("Powered by LangGraph + LM Studio")
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔗 Submit PR")
    pr_url = st.text_input(
        "GitHub Repo URL",
        placeholder="https://github.com/owner/repo"
    )

    with st.expander("⚙️ Options"):
        show_suggestions = st.checkbox("Include fix suggestions", value=True)
        save_report      = st.checkbox("Save report to file",     value=True)

    if st.button("🚀 Review", type="primary", use_container_width=True):
        if not pr_url:
            st.error("Please enter a PR URL")
        else:
            with st.spinner("🤖 Agents working... (this may take 1-2 mins)"):
                try:
                    report = run_review(pr_url)
                    st.session_state["report"]  = report
                    st.session_state["pr_url"]  = pr_url

                    if save_report:
                        fname = f"review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                        with open(fname, "w", encoding="utf-8") as f:
                            f.write(report)
                        st.success(f"Report saved to: {fname}")
                except Exception as e:
                    st.error(f" Error: {str(e)}")

with col2:
    st.subheader("📋 Review History")
    if "pr_url" in st.session_state:
        st.info(f"Last reviewed: {st.session_state['pr_url']}")

if "report" in st.session_state:
    st.divider()
    st.subheader("📄 Review Report")
    st.markdown(st.session_state["report"])
    st.download_button(
        "⬇️ Download Report",
        data=st.session_state["report"],
        file_name="code_review.md",
        mime="text/markdown"
    )
