from orator.migrations import Migration


class CreateRequestsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('requests') as table:
            table.increments('id')
            table.string('scheme').nullable()
            table.string('method')
            table.text('host')
            table.text('path')
            table.integer('port')
            table.string('headers_hash').index()
            table.string('body_text_hash').index()
            table.string('query_params_hash').index()
            table.string('body_params_hash').index()
            table.binary('control')
            table.binary('raw')
            table.timestamp('committed_at').nullable()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('requests')
