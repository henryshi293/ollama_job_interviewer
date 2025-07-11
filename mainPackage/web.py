from __future__ import annotations

###############################################################################
# Imports
###############################################################################

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import streamlit as st

from mainPackage.job_description import generate_job_description
from mainPackage.ranking import rank_applicants

###############################################################################
# Core Streamlit UI
###############################################################################

def start() -> None:  # noqa: D401
    """Render the two‑tab app."""

    st.set_page_config(page_title="Ollama Job Interviewer", layout="centered")
    st.title("Ollama Job Interviewer")

    tab_jd, tab_rank = st.tabs(["Generate JD", "Rank résumés"])

    # ────────────────────────────────────────────────────────────────────
    # 1. Job‑description generator
    # ────────────────────────────────────────────────────────────────────
    with tab_jd:
        job_title = st.text_input("Job title", placeholder="e.g. Software Engineer")
        model     = st.text_input("Ollama model", value="gemma3:latest")

        if st.button("Create description", disabled=not job_title):
            jd_text = generate_job_description(job_title, model)
            st.text_area("Job Description", jd_text, height=300)
            st.download_button("Download .txt", jd_text, file_name=f"{job_title}.txt")

    # ────────────────────────────────────────────────────────────────────
    # 2. Résumé ranking
    # ────────────────────────────────────────────────────────────────────
    with tab_rank:
        # 2‑A. Upload the *detailed* job‑description text file (generated via tab 1)
        jd_file = st.file_uploader(
            "Upload job‑description (.txt)",
            type=["txt"],
            accept_multiple_files=False,
        )

        # 2‑B. Upload one or more résumé PDFs to be ranked against the JD
        uploads = st.file_uploader(
            "Upload résumé PDFs", type=["pdf"], accept_multiple_files=True, key="pdfs"
        )

        # Enable the button only when we have both the JD and at least one résumé.
        if st.button("Rank", disabled=not (jd_file and uploads)):
            # Read the JD text into memory
            jd_text: str = jd_file.read().decode("utf‑8", errors="replace")

            # Save uploaded PDFs to a tmp dir so rank_applicants can read them.
            with tempfile.TemporaryDirectory() as tmpdir:
                paths: list[Path] = []
                for f in uploads:
                    p = Path(tmpdir) / f.name
                    with p.open("wb") as w:
                        shutil.copyfileobj(f, w)
                    paths.append(p)

                # ---- invoke ranking logic ----
                ranking_report = rank_applicants(jd_text, paths)  # pass full JD, not just title
                st.subheader("Ranking & Reasoning")
                st.markdown(ranking_report)

                #st.dataframe(table, use_container_width=True)
                #st.download_button(
                    #label="Download CSV",
                    #data=table.to_csv(index=False),
                    #file_name="ranking.csv",
                    #mime="text/csv",
                #)(
                    #label="Download CSV",
                    #data=table.to_csv(index=False),
                    #file_name="ranking.csv",
                    #mime="text/csv",
                #)

###############################################################################
# Console‑script wrapper (entry‑point)
###############################################################################

def cli() -> None:
    """Called by the *mainPackage-web* console script."""
    script_path = Path(__file__).resolve()
    subprocess.run(["streamlit", "run", str(script_path), *sys.argv[1:]], check=True)

###############################################################################
# Direct execution (streamlit run mainPackage/web.py)
###############################################################################

if __name__ == "__main__":
    start()
