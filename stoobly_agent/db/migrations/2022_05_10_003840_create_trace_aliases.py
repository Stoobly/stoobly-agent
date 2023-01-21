from orator.migrations import Migration

class CreateTraceAliases(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('trace_aliases') as table:
            table.increments('id')
            table.integer('trace_id').unsigned()
            table.foreign('trace_id').references('id').on('traces').index()
            table.text('name')
            table.binary('value')
            table.string('value_inferred_type').nullable()
            table.text('assigned_to').nullable()
            table.string('assigned_to_inferred_type').nullable()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('trace_aliases')
