from enum import Enum

from typing import Any
from tortoise.models import Model, QuerySet
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Permission(Enum):
    owner = 'owner'
    editor = 'editor'
    viewer = 'viewer'
    no = 'no'


class DayOfWeek(Enum):
    monday = 'monday'
    tuesday = 'tuesday'
    wednesday = 'wednesday'
    thursday = 'thursday'
    friday = 'friday'
    saturday = 'saturday'
    sunday = 'sunday'


class Calendar(Model):
    id = fields.IntField(pk=True)

    uuid = fields.UUIDField(unique=True)

    users = fields.ReverseRelation['User']

    is_public = fields.BooleanField(default=False)

    timetables = fields.ReverseRelation['Timetable']

    def __str__(self):
        return str(self.id)

    class Meta:
        table = 'calendar'

    class PydanticMeta:
        exclude = ['id', 'users']


class CalendarUser(Model):
    id = fields.IntField(pk=True)

    telegram_id = fields.IntField()
    # permission = fields.CharEnumField(Permission, default=Permission.no)
    permission = fields.SmallIntField(default=0)

    calendar: fields.ForeignKeyRelation[Calendar] = fields.ForeignKeyField('models.Calendar', related_name='users',
                                                                           to_field='id')

    def __str__(self):
        return self.id

    class Meta:
        table = 'user'

    class PydanticMeta:
        exclude = ['id']


class Timetable(Model):
    id = fields.IntField(pk=True)

    calendar: fields.ForeignKeyRelation[Calendar] = fields.ForeignKeyField('models.Calendar',
                                                                           related_name='timetables',
                                                                           to_field='id')

    tasks: fields.ReverseRelation['Task']

    def __str__(self):
        return self.name

    class Meta:
        table = 'timetable'

    class PydanticMeta:
        exclude = ["id"]


class Task(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=120)
    timetable = fields.ForeignKeyField('models.Timetable', related_name='tasks', to_field='id')
    # day_of_week = fields.CharEnumField(DayOfWeek, default=DayOfWeek.monday)
    day_of_week = fields.CharField(max_length=10, default=None)
    week_parity = fields.BooleanField(default=True)

    start_time = fields.SmallIntField()
    end_time = fields.SmallIntField()

    class Meta:
        table = 'task'

    def __str__(self):
        return self.name

    class PydanticMeta:
        exclude = ['id']

# Calendar_pydantic = pydantic_model_creator(Calendar, name='Calendar')
# Timetable_pydantic = pydantic_model_creator(Timetable, name='Timetable')
# CalendarUser_pydantic = pydantic_model_creator(CalendarUser, name='User')
# Task_pydantic = pydantic_model_creator(Task, name='Task')
