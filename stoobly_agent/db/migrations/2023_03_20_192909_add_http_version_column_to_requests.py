import pdb

from stoobly_orator.migrations import Migration

from stoobly_agent.lib.orm.request import Request

class AddHttpVersionColumnToRequests(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('requests') as table:
            table.decimal('http_version').default(1.1)

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('requests') as table:
            table.drop_column('http_version')
