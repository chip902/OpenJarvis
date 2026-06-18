"""Out-of-tree plugin loader.

OpenJarvis registers components by import side-effect (decorators on
``RegistryBase`` subclasses). External packages are not auto-discovered, so
this imports each comma-separated module named in the ``OPENJARVIS_PLUGINS``
environment variable, firing their ``@Registry.register`` decorators. A failing
import is logged and skipped — one bad plugin must never crash ``build()``.
"""

from __future__ import annotations

import importlib
import logging
import os

logger = logging.getLogger(__name__)

_ENV_VAR = "OPENJARVIS_PLUGINS"


def load_plugins() -> list[str]:
    """Import every module named in ``OPENJARVIS_PLUGINS``; return imported names."""
    raw = os.environ.get(_ENV_VAR, "")
    names = [n.strip() for n in raw.split(",") if n.strip()]
    if not names:
        logger.info("%s is empty; no out-of-tree plugins loaded.", _ENV_VAR)
        return []
    loaded: list[str] = []
    for name in names:
        try:
            importlib.import_module(name)
            loaded.append(name)
            logger.info("Loaded out-of-tree plugin package %r", name)
        except Exception as exc:  # noqa: BLE001 - a bad plugin must not crash build()
            logger.warning("Failed to load plugin %r: %s", name, exc)
    return loaded
