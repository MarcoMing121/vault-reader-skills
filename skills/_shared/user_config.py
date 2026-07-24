#!/usr/bin/env python3
"""
Vault-reader shared config loader.
All configuration is embedded here — no external JSON needed.
For local overrides, create user-config.local.json alongside this file.
"""

import copy
import json
from functools import lru_cache
from pathlib import Path


DEFAULT_CONFIG = {
    "VAULT_PATH": "~/ObsidianVault",
    "LEARNING_PATH": "~/ObsidianVault/Learning",
    "SPARK_PATH": "~/ObsidianVault/灵光一现",
    "GIT_COMMIT_ENABLED": False,
    "GIT_PUSH_ENABLED": False,
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

    # Only load local override if exists (optional)
    local_path = config_dir / "user-config.local.json"
    if local_path.exists():
        with local_path.open("r", encoding="utf-8") as f:
            loaded = json.load(f)
        if isinstance(loaded, dict):
            _deep_merge(config, loaded)

    return config


def vault_path() -> Path:
    return Path(load_config()["VAULT_PATH"])


def learning_path() -> Path:
    return Path(load_config()["LEARNING_PATH"])


def spark_path() -> Path:
    return Path(load_config()["SPARK_PATH"])


def git_commit_enabled() -> bool:
    return bool(load_config().get("GIT_COMMIT_ENABLED", True))


def git_push_enabled() -> bool:
    return bool(load_config().get("GIT_PUSH_ENABLED", True))
