"""Módulo de auditoria para decisões e alterações manuais."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class AuditTrail:
    """Regista eventos relevantes à tomada de decisão."""

    def __init__(self, audit_file: str | Path = "audit_log.json") -> None:
        self.audit_file = Path(audit_file)
        self.audit_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self, **payload: Any) -> dict[str, Any]:
        entry = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            **payload,
        }
        existing = []
        if self.audit_file.exists():
            try:
                existing = json.loads(self.audit_file.read_text(encoding="utf-8"))
            except Exception:
                existing = []
        existing.append(entry)
        self.audit_file.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
        return entry
