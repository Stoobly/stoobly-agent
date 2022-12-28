from orator.migrations import Migration


class AddFilterColumnsToRequests(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('requests') as table:
            table.boolean('is_deleted').default(False)
            table.boolean('starred').default(False)

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('requests') as table:
            table.drop_column('is_deleted', 'starred')
