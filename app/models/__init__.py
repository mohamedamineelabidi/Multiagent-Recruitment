# Import all models to make them accessible to Base.metadata.create_all()
from .job import Job
from .project import Project
from .candidate import Candidate
from .submission import Submission

__all__ = ["Job", "Project", "Candidate", "Submission"]