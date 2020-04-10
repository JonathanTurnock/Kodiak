from sqlite3 import Connection


def setup_job(kodiak_db: Connection):
    kodiak_db.execute("drop table if exists job")

    kodiak_db.execute("""\
        create table job
        (
            id INTEGER constraint job_pk primary key autoincrement,
            uuid TEXT not null,
            name TEXT,
            url TEXT
        )\
        """)

    kodiak_db.execute("create unique index job_id_uindex on job (id)")

    kodiak_db.execute("create unique index job_uuid_uindex on job (uuid)")


def setup(kodiak_db: Connection):
    setup_job(kodiak_db)
