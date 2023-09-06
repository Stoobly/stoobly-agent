from stoobly_orator.migrations import Migration

class CreateScenarios(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('scenarios') as table:
            table.increments('id')
            table.string('name')
            table.integer('requests_count').default(0)
            table.string('description').default("")
            table.boolean('starred').default(False)
            table.integer('priority').default(0)
            table.boolean('is_deleted').default(False)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('scenarios')
