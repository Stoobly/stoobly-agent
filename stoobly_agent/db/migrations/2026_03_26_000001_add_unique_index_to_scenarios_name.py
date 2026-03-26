from stoobly_orator.migrations import Migration


SCENARIOS_NAME_UNIQUE_INDEX = 'scenarios_name_unique'


class AddUniqueIndexToScenariosName(Migration):
    def up(self):
        """
        Create a unique index on `scenarios.name` to prevent duplicate scenario names.
        """
        with self.schema.table('scenarios') as table:
            # Blueprint.unique() creates an index/constraint named
            # "<table>_<column(s)>_unique" (normalized to lower/underscores).
            # We pass an explicit name for deterministic rollback.
            table.unique('name', SCENARIOS_NAME_UNIQUE_INDEX)

    def down(self):
        """
        Remove the unique index created in `up()`.
        """
        with self.schema.table('scenarios') as table:
            # drop_unique() for postgres drops the unique constraint by name,
            # and for sqlite/mysql it drops the underlying index by name.
            table.drop_unique(SCENARIOS_NAME_UNIQUE_INDEX)

