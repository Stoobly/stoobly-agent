from stoobly_orator.migrations import Migration

from stoobly_agent.lib.orm.scenario import Scenario


SCENARIOS_NAME_UNIQUE_INDEX = 'scenarios_name_unique'


class AddUniqueIndexToScenariosName(Migration):
    def up(self):
        """
        Create a unique index on `scenarios.name` to prevent duplicate scenario names.
        """
        # Normalize existing duplicates first so the unique index can be created safely.
        self.__rename_duplicate_scenario_names()

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

    def __rename_duplicate_scenario_names(self):
        scenarios = Scenario.order_by('id', 'asc').get()
        if not scenarios:
            return

        used_names = set()
        duplicate_counters = {}

        for scenario in scenarios:
            current_name = scenario.name or ''
            base_name = current_name

            if base_name not in used_names:
                used_names.add(base_name)
                continue

            next_counter = duplicate_counters.get(base_name, 2)
            candidate_name = f'{base_name} ({next_counter})'

            while candidate_name in used_names:
                next_counter += 1
                candidate_name = f'{base_name}-{next_counter}'

            scenario.update(name=candidate_name)

            duplicate_counters[base_name] = next_counter + 1
            used_names.add(candidate_name)
