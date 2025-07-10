"""Generate a detailed job description from a one-line job title."""

from __future__ import annotations

from textwrap import dedent

from .api import OllamaAPI

_COMPANY_INFO = dedent(
    """
    Company: Cytoderm
    Location: Beijing, China
    """
).strip()


def _build_prompt(job_title: str) -> str:
    return dedent(
        f"""
        Write a comprehensive, well-structured job description for **{job_title}**.

        Include the following sections:

        1) Role overview
        2) Primary responsibilities
        3) Required skills and qualifications
        4) Nice-to-have skills
        5) Example day-to-day routine

        Company details
        ---------------
        {_COMPANY_INFO}

        Do **not** ask any follow-up questions.
        """
    ).strip()


def generate_job_description(job_title: str, *, api: OllamaAPI | None = None) -> str:
    """Return a full job-description document for *job_title*."""
    client = api or OllamaAPI()
    prompt = _build_prompt(job_title)
    response = client.query(prompt) or ""
    return response.strip()
