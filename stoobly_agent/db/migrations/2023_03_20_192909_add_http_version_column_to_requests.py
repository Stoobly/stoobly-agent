import pdb

from orator.migrations import Migration

from stoobly_agent.lib.orm.request import Request

class AddHttpVersionColumnToRequests(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('requests') as table:
            table.decimal('http_version').nullable()

        for request in Request.all():
            request.update(http_version=1.1)

        with self.schema.table('requests') as table:
            table.decimal('http_version').default(1.1).change()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('requests') as table:
            table.drop_column('http_version')
