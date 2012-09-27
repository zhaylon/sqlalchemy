from .. import fixtures, config, util
from ..config import requirements
from ..assertions import eq_

from sqlalchemy import Table, Column, Integer, String


class TableDDLTest(fixtures.TestBase):

    def _simple_fixture(self):
        return Table('test_table', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('data', String(50))
            )

    def _simple_roundtrip(self):
        with config.db.begin() as conn:
            conn.execute("insert into test_table(id, data) values "
                            "(1, 'some data')")
            result = conn.execute("select id, data from test_table")
            eq_(
                result.first(),
                (1, 'some data')
            )


    @requirements.create_table
    @util.provide_metadata
    def test_create_table(self):
        table = self._simple_fixture()
        table.create(
            config.db, checkfirst=False
        )
        self._simple_roundtrip()


    @requirements.drop_table
    @util.provide_metadata
    def test_drop_table(self):
        table = self._simple_fixture()
        table.create(
            config.db, checkfirst=False
        )
        table.drop(
            config.db, checkfirst=False
        )


__all__ = ('TableDDLTest', )