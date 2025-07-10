"""Rank applicants' resumes against a given job description."""

from __future__ import annotations

import logging
from io import BytesIO
from pathlib import Path
from typing import Iterable, List

from pypdf import PdfReader

from .api import OllamaAPI

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def _extract_text_from_pdf(path: Path) -> str:
    """Return concatenated text from all pages of *path*."""
    reader = PdfReader(BytesIO(path.read_bytes()))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _build_prompt(job_description: str, resume_texts: List[str]) -> str:
    bullet_list = "\n\n".join(
        f"### Applicant {idx + 1}\n\n{txt}" for idx, txt in enumerate(resume_texts)
    )
    return (
        f"You are an expert recruiter.\n\n"
        f"**Job description**\n{job_description}\n\n"
        f"**Applicant résumés**\n\n{bullet_list}\n\n"
        "Rank the applicants from strongest to weakest **by name** if available, "
        "or by the order given if none.  Return just a numbered list."
    )


def rank_applicants(
    job_description: str,
    pdf_paths: Iterable[Path],
    *,
    api: OllamaAPI | None = None,
) -> str:
    """Return a strength ranking for *pdf_paths* according to *job_description*."""
    resume_texts = [_extract_text_from_pdf(p) for p in pdf_paths]
    prompt = _build_prompt(job_description, resume_texts)
    client = api or OllamaAPI()
    response = client.query(prompt) or ""
    return response.strip()
