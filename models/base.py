from extensions import dbt
from random import randint
import datetime


class BaseMixin(object):
   enabled = dbt.Column(dbt.Boolean, default=True, nullable=False)
   created_at = dbt.Column(dbt.DateTime, default=datetime.datetime.now, nullable=False)
   updated_at = dbt.Column(dbt.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)