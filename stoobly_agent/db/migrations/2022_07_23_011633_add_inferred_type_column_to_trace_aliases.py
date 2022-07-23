from orator.migrations import Migration

class AddInferredTypeColumnToTraceAliases(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('trace_aliases') as table:
            table.string('inferred_type').string().nullable()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('trace_aliases') as table:
            table.drop_column('inferred_type')
