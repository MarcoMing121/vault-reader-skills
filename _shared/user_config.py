#!/usr/bin/env python3
"""
Vault-reader shared config loader.
Reads paths from user-config.json (and user-config.local.json override).
"""

import copy
import json
from functools import lru_cache
from pathlib import Path


DEFAULT_CONFIG = {
    "VAULT_PATH": "/root/.openclaw/shared/ObsidianVault",
    "LEARNING_PATH": "/root/.openclaw/shared/ObsidianVault/Learning",
    "LATEX_CACHE_PATH": "/root/.openclaw/shared/latex-cache",
    "SPARK_PATH": "/root/.openclaw/shared/ObsidianVault/灵光一现",
    "GIT_COMMIT_ENABLED": True,
    "GIT_PUSH_ENABLED": True,
}


def _deep_merge(base: dict, override: dict) -> dict:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
    return base


@lru_cache(maxsize=1)
def load_config() -> dict:
    config = copy.deepcopy(DEFAULT_CONFIG)
    config_dir = Path(__file__).resolve().parent

    for filename in ("user-config.json", "user-config.local.json"):
        config_path = config_dir / filename
        if not config_path.exists():
            continue
        with config_path.open("r", encoding="utf-8") as f:
            loaded = json.load(f)
        if isinstance(loaded, dict):
            _deep_merge(config, loaded)

    return config


def vault_path() -> Path:
    return Path(load_config()["VAULT_PATH"])


def learning_path() -> Path:
    return Path(load_config()["LEARNING_PATH"])


def latex_cache_path() -> Path:
    return Path(load_config()["LATEX_CACHE_PATH"])


def spark_path() -> Path:
    return Path(load_config()["SPARK_PATH"])


def git_commit_enabled() -> bool:
    return bool(load_config().get("GIT_COMMIT_ENABLED", True))


def git_push_enabled() -> bool:
    return bool(load_config().get("GIT_PUSH_ENABLED", True))
