from sqlalchemy import Column, Integer, Text, DateTime

from app import Base

class HistoryRecord(Base):

    __tablename__ = 'history_record'

    id = Column(Integer, primary_key=True)
    command = Column(Text)
    time = Column(DateTime)

    def __init__(self, command, time):
        self.command = command
        self.time = time

    def __repr__(self):
        return '<Command: %s, Time: %d, Id: %d>' % (self.command, self.time.isoformat(), self.id)

    def _serialise(self):
        return {
                'id': self.id,
                'Command': self.command,
                'Time': self.time.isoformat(),
                }