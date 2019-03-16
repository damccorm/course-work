import happybase
import sys

from variables import MACHINE, VUID, PAGE_TABLE, COLUMN_FAMILY, INDEX_TABLE


def setup():
    print 'Creating...'
    connection = happybase.Connection(MACHINE, table_prefix=VUID)
    connection.create_table(PAGE_TABLE, {COLUMN_FAMILY: dict()})
    connection.create_table(INDEX_TABLE, {COLUMN_FAMILY: dict()})


def delete():
    print 'Deleting...'
    connection = happybase.Connection(MACHINE, table_prefix=VUID)
    connection.delete_table(PAGE_TABLE, True)
    connection.delete_table(INDEX_TABLE, True)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'delete':
            delete()
        elif sys.argv[1] == 'scan':
            connection = happybase.Connection(MACHINE, table_prefix=VUID)
            table = connection.table(INDEX_TABLE)
            i = 0
            for k, v in table.scan():
                print i, k, v,
                i += 1
                if i > 10: break
    else:
        setup()
    print 'Done...'
