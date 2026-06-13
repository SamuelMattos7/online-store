from __future__ import annotations
from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, Table, Integer, String, Text, Boolean, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship