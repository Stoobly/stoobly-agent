from stoobly_orator.migrations import Migration


class AddOverwritableColumnToScenarios(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('scenarios') as table:
            table.boolean('overwritable').default(False)

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('scenarios') as table:
            table.drop_column('overwritable')
