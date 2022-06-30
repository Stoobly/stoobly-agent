from orator.migrations import Migration


class CreateTraceRequests(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('trace_requests') as table:
            table.increments('id')
            table.integer('trace_id').unsigned()
            table.foreign('trace_id').references('id').on('traces').index()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('trace_requests')
