from stoobly_orator.migrations import Migration


class CreateReplayedResponses(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('replayed_responses') as table:
            table.increments('id')
            table.integer('request_id').unsigned()
            table.foreign('request_id').references('id').on('requests').index()
            table.binary('raw')
            table.integer('status')
            table.integer('latency')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('replayed_responses')
