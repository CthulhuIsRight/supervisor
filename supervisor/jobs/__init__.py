"""Supervisor job manager."""
import logging
from typing import Dict, List, Optional

from ..coresys import CoreSys, CoreSysAttributes

_LOGGER: logging.Logger = logging.getLogger(__package__)


class SupervisorJob(CoreSysAttributes):
    """Supervisor running job class."""

    def __init__(self, coresys: CoreSys, name: str):
        """Initialize the JobManager class."""
        self.coresys: CoreSys = coresys
        self.name: str = name
        self._progress: int = 0
        self._stage: Optional[str] = None

    @property
    def progress(self) -> int:
        """Return the current progress."""
        return self._progress

    @property
    def stage(self) -> Optional[str]:
        """Return the current stage."""
        return self._stage

    def update(
        self, progress: Optional[int] = None, stage: Optional[str] = None
    ) -> None:
        """Update the job object."""
        if progress is not None:
            if progress >= round(100):
                self.sys_jobs.remove_job(self)
                return
            self._progress = round(progress)
        if stage is not None:
            self._stage = stage
        _LOGGER.debug(
            "Job updated; name: %s, progress: %s, stage: %s",
            self.name,
            self.progress,
            self.stage,
        )


class JobManager(CoreSysAttributes):
    """Job class."""

    def __init__(self, coresys: CoreSys):
        """Initialize the JobManager class."""
        self.coresys: CoreSys = coresys
        self._jobs: Dict[str, SupervisorJob] = {}

    @property
    def jobs(self) -> List[SupervisorJob]:
        """Return a list of current jobs."""
        return self._jobs

    def get_job(self, name: str) -> SupervisorJob:
        """Return a job, create one if it does not exsist."""
        if name not in self._jobs:
            self._jobs[name] = SupervisorJob(self.coresys, name)

        return self._jobs[name]

    def remove_job(self, job: SupervisorJob) -> None:
        """Remove a job."""
        if job.name in self._jobs:
            del self._jobs[job.name]

    def clear(self) -> None:
        """Clear all jobs."""
        self._jobs.clear()
