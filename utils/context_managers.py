"""Context managers for resource management.

Provides reusable context managers for common resource management patterns
across analysis, LLM interactions, and file operations.
"""

import logging
import time
from contextlib import contextmanager
from typing import Generator, Optional

logger = logging.getLogger(__name__)


@contextmanager
def analysis_context(
    project_path: str, operation_name: str = "analysis"
) -> Generator[None, None, None]:
    """Context manager for analysis operations with automatic cleanup.

    Args:
        project_path: Path to project being analyzed.
        operation_name: Name of the operation for logging purposes.

    Yields:
        None

    Example:
        >>> with analysis_context("/path/to/project", "language_detection"):
        ...     detect_languages()
    """
    start_time = time.time()
    logger.info(f"Starting {operation_name} for: {project_path}")

    try:
        yield
    except Exception as e:
        logger.error(f"{operation_name} failed for {project_path}: {e}", exc_info=True)
        raise
    finally:
        duration = time.time() - start_time
        logger.info(f"Completed {operation_name} for {project_path} " f"in {duration:.2f}s")


@contextmanager
def llm_context(model_name: str, provider: str, operation: str) -> Generator[None, None, None]:
    """Context manager for LLM interactions with timing and error handling.

    Args:
        model_name: Name of the LLM model being used.
        provider: Provider name (e.g., 'openai', 'anthropic').
        operation: Description of the LLM operation.

    Yields:
        None

    Example:
        >>> with llm_context("gpt-4", "openai", "code analysis"):
        ...     response = llm.chat(prompt)
    """
    start_time = time.time()
    logger.debug(f"LLM request: {operation} (model: {model_name})")

    try:
        yield
    except Exception as e:
        logger.error(
            f"LLM error during {operation}: {e} " f"(model: {model_name}, provider: {provider})"
        )
        raise
    finally:
        duration = time.time() - start_time
        logger.debug(f"LLM {operation} completed in {duration:.2f}s " f"(model: {model_name})")


@contextmanager
def performance_monitor(operation_name: str) -> Generator[dict, None, None]:
    """Context manager for monitoring performance metrics.

    Args:
        operation_name: Name of the operation being monitored.

    Yields:
        Dictionary to store performance metrics.

    Example:
        >>> with performance_monitor("file_scan") as metrics:
        ...     scan_files()
        ...     metrics['files_processed'] = 100
    """
    metrics = {
        "operation": operation_name,
        "start_time": time.time(),
        "end_time": None,
        "duration": None,
    }

    try:
        yield metrics
    finally:
        metrics["end_time"] = time.time()
        metrics["duration"] = metrics["end_time"] - metrics["start_time"]
        logger.debug(f"Performance: {operation_name} took {metrics['duration']:.2f}s")
