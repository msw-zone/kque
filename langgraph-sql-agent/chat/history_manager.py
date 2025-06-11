from __future__ import annotations

import uuid

from .models import Base, Message
from .db import get_engine, get_session_factory


class HistoryManager:
    def __init__(self, db_uri: str):
        self.db_uri = db_uri
        self.engine = get_engine(db_uri)
        Base.metadata.create_all(self.engine)
        self.session_factory = get_session_factory(db_uri)

    def create_session_id(self) -> str:
        return uuid.uuid4().hex

    def add_message(self, session_id: str, role: str, content: str):
        with self.session_factory() as s:
            msg = Message(session_id=session_id, role=role, content=content)
            s.add(msg)
            s.commit()

    def get_messages(self, session_id: str) -> list[Message]:
        with self.session_factory() as s:
            return list(s.query(Message).filter_by(session_id=session_id).order_by(Message.timestamp).all())

    def clear_history(self, session_id: str):
        with self.session_factory() as s:
            s.query(Message).filter_by(session_id=session_id).delete()
            s.commit()
