from enum import Enum

from tortoise.models import Model
from tortoise import fields


class Permission(Enum):
    owner = 'owner'
    editor = 'editor'
    viewer = 'viewer'


class Calendar(Model):
    id = fields.IntField(pk=True)

    uuid = fields.UUIDField(unique=True)

    users = fields.ReverseRelation['User']

    is_public = fields.BooleanField(default=False)

    timetables = fields.ReverseRelation['TimeTable']

    def __str__(self):
        return self.uuid


class CalendarUser(Model):
    id = fields.IntField(pk=True)

    telegram_id = fields.IntField()
    permission = fields.CharEnumField(Permission, default=None)

    calendar: fields.ForeignKeyRelation[Calendar] = fields.ForeignKeyField('models.Calendar', related_name='users',
                                                                            to_field='id')

    def __str__(self):
        return self.id


class TimeTable(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=30)

    calendar: fields.ForeignKeyRelation[Calendar] = fields.ForeignKeyField('models.Calendar',
                                                                            related_name='timetables',
                                                                            to_field='id')

    odd_week: fields.ReverseRelation['Day']
    even_week: fields.ReverseRelation['Day']

    def __str__(self):
        return self.name


class Day(Model):
    id = fields.IntField(pk=True)

    timetable: fields.ForeignKeyRelation[TimeTable] = fields.ForeignKeyField('models.TimeTable')

    tasks: fields.ManyToManyRelation['Task'] = fields.ManyToManyField('models.Task', related_name='days')

    def __str__(self):
        return self.id


class Task(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=120)
    days: fields.ManyToManyRelation[Day]

    start_time = fields.SmallIntField()
    end_time = fields.SmallIntField()

    def __str__(self):
        return self.name
