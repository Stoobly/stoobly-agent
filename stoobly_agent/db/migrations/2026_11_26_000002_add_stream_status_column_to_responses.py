from stoobly_orator.migrations import Migration


class AddStreamStatusColumnToResponses(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('responses') as table:
            table.string('stream_status').nullable()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('responses') as table:
            table.drop_column('stream_status')
