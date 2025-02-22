# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List

import pytest

from datadog_checks.base.utils.db.utils import DBMAsyncJob

from .common import POSTGRES_VERSION
from .utils import run_one_check

pytestmark = [pytest.mark.integration, pytest.mark.usefixtures('dd_environment')]


@pytest.fixture
def dbm_instance(pg_instance):
    pg_instance['dbm'] = True
    pg_instance['min_collection_interval'] = 0.1
    pg_instance['query_samples'] = {'enabled': False}
    pg_instance['query_activity'] = {'enabled': False}
    pg_instance['query_metrics'] = {'enabled': False}
    pg_instance['collect_resources'] = {'enabled': True, 'run_sync': True, 'collection_interval': 0.1}
    pg_instance['collect_settings'] = {'enabled': True, 'run_sync': True, 'collection_interval': 0.1}
    return pg_instance


@pytest.fixture(autouse=True)
def stop_orphaned_threads():
    # make sure we shut down any orphaned threads and create a new Executor for each test
    DBMAsyncJob.executor.shutdown(wait=True)
    DBMAsyncJob.executor = ThreadPoolExecutor()


def test_collect_metadata(integration_check, dbm_instance, aggregator):
    check = integration_check(dbm_instance)
    check.check(dbm_instance)
    dbm_metadata = aggregator.get_event_platform_events("dbm-metadata")
    event = next((e for e in dbm_metadata if e['kind'] == 'pg_settings'), None)
    assert event is not None
    assert event['host'] == "stubbed.hostname"
    assert event['dbms'] == "postgres"
    assert event['kind'] == "pg_settings"
    assert len(event["metadata"]) > 0


def test_collect_schemas(integration_check, dbm_instance, aggregator):
    dbm_instance["collect_schemas"] = {'enabled': True, 'collection_interval': 0.5}
    dbm_instance['relations'] = [{'relation_regex': ".*"}]
    dbm_instance["database_autodiscovery"] = {"enabled": True, "include": ["datadog"]}
    del dbm_instance['dbname']
    check = integration_check(dbm_instance)
    run_one_check(check, dbm_instance)
    dbm_metadata = aggregator.get_event_platform_events("dbm-metadata")
    schema_event = next(e for e in dbm_metadata if e['kind'] == 'pg_databases')

    # there should only be one database, datadog_test
    database_metadata = schema_event['metadata']
    assert len(database_metadata) == 1
    assert 'datadog_test' == database_metadata[0]['name']

    # there should only two schemas, 'public' and 'datadog'. datadog is empty
    schema_names = [s['name'] for s in database_metadata[0]['schemas']]
    assert 'public' in schema_names
    assert 'datadog' in schema_names
    schema_public = None
    for schema in database_metadata[0]['schemas']:
        if schema['name'] == 'public':
            schema_public = schema

    # check that all expected tables are present
    tables_set = {'persons', "personsdup1", "personsdup2", "pgtable", "pg_newtable", "cities"}
    # if version isn't 9 or 10, check that partition master is in tables
    if float(POSTGRES_VERSION) >= 11:
        tables_set.update({'test_part', 'test_part_no_children'})
    tables_not_reported_set = {'test_part1', 'test_part2'}

    tables_got = []
    for table in schema_public['tables']:
        tables_got.append(table['name'])

        # make some assertions on fields
        if table['name'] == "persons":
            # check that foreign keys, indexes get reported
            keys = list(table.keys())
            assert_fields(keys, ["foreign_keys", "columns", "toast_table", "id", "name"])
            assert_fields(list(table['foreign_keys'][0].keys()), ['name', 'definition'])
            assert_fields(
                list(table['columns'][0].keys()),
                [
                    'name',
                    'nullable',
                    'data_type',
                    'default',
                ],
            )
        if table['name'] == "cities":
            keys = list(table.keys())
            assert_fields(keys, ["indexes", "columns", "toast_table", "id", "name"])
            assert_fields(list(table['indexes'][0].keys()), ['name', 'definition'])
        if float(POSTGRES_VERSION) >= 11:
            if table['name'] == 'test_part':
                keys = list(table.keys())
                assert_fields(keys, ["indexes", "num_partitions", "partition_key"])
                assert table['num_partitions'] == 2
            elif table['name'] == 'test_part_no_children':
                keys = list(table.keys())
                assert_fields(keys, ["indexes", "num_partitions", "partition_key"])
                assert table['num_partitions'] == 0

    assert_fields(tables_got, tables_set)
    assert_not_fields(tables_got, tables_not_reported_set)


def assert_fields(keys: List[str], fields: List[str]):
    for field in fields:
        assert field in keys


def assert_not_fields(keys: List[str], fields: List[str]):
    for field in fields:
        assert field not in keys
