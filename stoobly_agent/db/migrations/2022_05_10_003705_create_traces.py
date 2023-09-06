from stoobly_orator.migrations import Migration


class CreateTraces(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('traces') as table:
            table.increments('id')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('traces')
