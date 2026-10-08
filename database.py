"""Base de dados SQLite para armazenar empresas, pedidos e resultados."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent / "data" / "credit_engine.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    connection = get_connection()
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id TEXT,
                company_name TEXT,
                nif TEXT,
                sector TEXT,
                province TEXT,
                payload TEXT
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id TEXT,
                requested_amount REAL,
                requested_term_months INTEGER,
                currency TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                payload TEXT
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id TEXT,
                user_name TEXT,
                score REAL,
                risk_class TEXT,
                recommendation TEXT,
                explanation TEXT,
                conditions TEXT,
                rules_version TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id TEXT,
                level TEXT,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT,
                user_name TEXT,
                company_id TEXT,
                details TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()
    finally:
        connection.close()


def save_company(payload: dict[str, Any]) -> None:
    connection = get_connection()
    try:
        connection.execute(
            "INSERT INTO companies (company_id, company_name, nif, sector, province, payload) VALUES (?, ?, ?, ?, ?, ?)",
            (
                payload.get("company_id", ""),
                payload.get("company_name", ""),
                payload.get("nif", ""),
                payload.get("sector", ""),
                payload.get("province", ""),
                json.dumps(payload, ensure_ascii=False),
            ),
        )
        connection.commit()
    finally:
        connection.close()


def save_analysis(payload: dict[str, Any]) -> None:
    connection = get_connection()
    try:
        connection.execute(
            "INSERT INTO analyses (company_id, user_name, score, risk_class, recommendation, explanation, conditions, rules_version) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                payload.get("company_id", ""),
                payload.get("user_name", ""),
                float(payload.get("score", 0.0)),
                payload.get("risk_class", ""),
                payload.get("recommendation", ""),
                payload.get("explanation", ""),
                json.dumps(payload.get("conditions", []), ensure_ascii=False),
                payload.get("rules_version", "1.0.0"),
            ),
        )
        connection.commit()
    finally:
        connection.close()


def save_application(payload: dict[str, Any]) -> None:
    """Guarda o pedido actual. A persistência depende do ambiente onde o protótipo corre."""
    connection = get_connection()
    try:
        connection.execute(
            "INSERT INTO applications (company_id, requested_amount, requested_term_months, currency, payload) VALUES (?, ?, ?, ?, ?)",
            (
                payload.get("company_id", ""),
                float(payload.get("requested_amount", 0.0)),
                int(payload.get("requested_term_months", 0)),
                payload.get("currency", "AOA"),
                json.dumps(payload, ensure_ascii=False),
            ),
        )
        connection.commit()
    finally:
        connection.close()


def list_analyses(limit: int = 100) -> list[dict[str, Any]]:
    """Devolve análises recentes para o módulo de auditoria."""
    connection = get_connection()
    try:
        rows = connection.execute(
            "SELECT * FROM analyses ORDER BY id DESC LIMIT ?", (max(1, int(limit)),)
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def save_audit_event(action: str, user_name: str, company_id: str, details: dict[str, Any]) -> None:
    connection = get_connection()
    try:
        connection.execute(
            "INSERT INTO audit_log (action, user_name, company_id, details) VALUES (?, ?, ?, ?)",
            (action, user_name, company_id, json.dumps(details, ensure_ascii=False)),
        )
        connection.commit()
    finally:
        connection.close()
