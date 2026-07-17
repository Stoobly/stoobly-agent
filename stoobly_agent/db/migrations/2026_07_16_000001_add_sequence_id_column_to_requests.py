from stoobly_orator.migrations import Migration


class AddSequenceIdColumnToRequests(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('requests') as table:
            table.integer('sequence_id').nullable()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('requests') as table:
            table.drop_column('sequence_id')
