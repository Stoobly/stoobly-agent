from orator.migrations import Migration

from stoobly_agent.lib.orm.response import Response

class AddHttpVersionColumnToResponses(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('responses') as table:
            table.decimal('http_version').nullable()

        for response in Response.all():
            response.update(http_version=1.1)

        with self.schema.table('responses') as table:
            table.decimal('http_version').default(1.1).change()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('responses') as table:
            table.drop_column('http_version')

