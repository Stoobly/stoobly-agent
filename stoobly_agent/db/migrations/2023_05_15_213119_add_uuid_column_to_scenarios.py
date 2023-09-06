import uuid

from stoobly_orator.migrations import Migration

from stoobly_agent.lib.orm.scenario import Scenario

class AddUuidColumnToScenarios(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('scenarios') as table:
            table.string('uuid', 36).index().default('')

        for scenario in Scenario.all():
            scenario.update(uuid=str(uuid.uuid4()))

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('scenarios') as table:
            table.drop_column('uuid')
