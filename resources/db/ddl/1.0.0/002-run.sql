create table run
(
    id      INTEGER not null constraint run_pk primary key autoincrement,
    job_id  INTEGER not null constraint run_job_id_fk references job on update cascade on delete cascade,
    uuid    TEXT    not null,
    status  TEXT,
    started TIMESTAMP,
    ended   TIMESTAMP
);

create unique index run_id_uindex on run (id);

create unique index run_uuid_uindex on run (uuid);
