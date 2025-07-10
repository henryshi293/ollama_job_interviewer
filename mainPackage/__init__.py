"""Public interface for *mypackage*.

Re-export the key building blocks so that users can do::

    import mypackage as mp
    jd  = mp.generate_job_description("Software Engineer")
    rank = mp.rank_applicants(jd, pdf_paths)
"""

from importlib.metadata import PackageNotFoundError, version

from .api import OllamaAPI
from .job_description import generate_job_description
from .ranking import rank_applicants

__all__ = [
    "OllamaAPI",
    "generate_job_description",
    "rank_applicants",
]

# Optional: expose package version if you’re using setuptools-scm / Poetry
try:
    __version__: str = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"