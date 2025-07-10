"""Wrapper around the local Ollama HTTP API."""

from __future__ import annotations

import json
import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class OllamaAPI:
    """Thin client for the *Ollama* text-generation service running locally."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model_name: str = "gemma3:latest",
        *,
        timeout: float | None = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model_name = model_name
        self.timeout = timeout

    # --------------------------------------------------------------------- #
    # Public helpers
    # --------------------------------------------------------------------- #
    def query(self, prompt: str, *, model_name: str | None = None) -> Optional[str]:
        """Send *prompt* to Ollama and return the model’s textual response."""
        model = model_name or self.model_name
        payload = {"model": model, "prompt": prompt, "stream": False}

        try:
            resp = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )
            resp.raise_for_status()
        except requests.exceptions.RequestException as exc:
            logger.error("Ollama request failed: %s", exc, exc_info=True)
            return None

        # In practice Ollama may return one JSON object or many newline-delimited
        # fragments.  Coalesce them and take the last full object.
        responses: list[dict] = []
        for line in resp.text.splitlines():
            try:
                responses.append(json.loads(line))
            except json.JSONDecodeError:
                continue

        if not responses:
            logger.warning("No JSON content returned from Ollama")
            return None

        return responses[-1].get("response")
