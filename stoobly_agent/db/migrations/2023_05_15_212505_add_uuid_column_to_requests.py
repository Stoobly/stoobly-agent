import pdb
import uuid

from stoobly_orator.migrations import Migration

from stoobly_agent.app.proxy.record.request_string_control import RequestStringControl
from stoobly_agent.lib.orm.request import Request

class AddUuidColumnToRequests(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('requests') as table:
            table.string('uuid', 36).default('').index().unique()

        for request in Request.all():
            control = RequestStringControl(request.control)
            try:
                request.update(uuid=str(uuid.UUID(control.id)))
            except Exception:
                request.update(uuid=str(uuid.uuid4()))

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('requests') as table:
            table.drop_column('uuid')
