
from alerta.app import db


class SwitchState(object):
    ON = True
    OFF = False

    @staticmethod
    def to_state(string):
        return SwitchState.ON if string == "ON" else SwitchState.OFF

    @staticmethod
    def to_string(state):
        return "ON" if state else "OFF"


class Switch(object):

    switches = []

    def __init__(self, name, title=None, description=None, value=SwitchState.ON):
        self.group = 'switch'
        self.name = name
        self.title = title
        self.description = description
        self.type = 'text'
        self.value = value

        self.set("ON")

    def serialize(self):
        return {
            'name': self.name,
            'title': self.title,
            'description': self.description,
            'type': self.type,
            'value': "ON" if self.is_on else "OFF",
        }

    def __repr__(self):
        return 'Switch(name=%r, description=%r, state=%r)' % (
            self.name, self.description, SwitchState.to_string(self.value)
        )

    @classmethod
    def from_document(cls, doc):
        return Switch(
            name=doc.get('name'),
            title=doc.get('title', None),
            description=doc.get('description', None),
            value=doc.get('value', None)
        )

    @classmethod
    def from_record(cls, rec):
        return Switch(
            name=rec.name,
            title=rec.title,
            description=rec.description,
            value=rec.value
        )

    @classmethod
    def from_db(cls, r):
        if isinstance(r, dict):
            return cls.from_document(r)
        elif isinstance(r, tuple):
            return cls.from_record(r)
        else:
            return

    def set(self, state):
        self.value = state
        return Switch.from_db(db.set_switch(self))

    @classmethod
    def find_all(cls):
        return [Switch.from_db(switch) for switch in db.get_metrics(type='text', group='switch')]

    @property
    def is_on(self):
        return self.value
