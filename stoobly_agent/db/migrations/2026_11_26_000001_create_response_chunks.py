from stoobly_orator.migrations import Migration


class CreateResponseChunks(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('response_chunks') as table:
            table.increments('id')
            table.integer('response_id').unsigned()
            table.foreign('response_id').references('id').on('responses').index()
            table.integer('sequence').unsigned()
            table.binary('payload')
            table.timestamps()
            table.unique(['response_id', 'sequence'])

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('response_chunks')
