from orator.migrations import Migration

class AddScenarioIdReferenceToRequests(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('requests') as table:
            table.integer('scenario_id').nullable()
            table.foreign('scenario_id').references('id').on('scenarios').index() 

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('requests') as table:
            table.drop_column('scenario_id')
