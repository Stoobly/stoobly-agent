from orator.migrations import Migration

class CreateResponses(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('responses') as table:
            table.increments('id')
            table.integer('request_id').unsigned()
            table.foreign('request_id').references('id').on('requests').index()
            table.binary('control')
            table.binary('raw')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('responses')
