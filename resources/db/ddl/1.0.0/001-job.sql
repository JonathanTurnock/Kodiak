create table job
(
    id   INTEGER not null constraint job_pk primary key autoincrement,
    uuid TEXT    not null,
    name TEXT,
    url  TEXT
);

create unique index job_id_uindex on job (id);

create unique index job_uuid_uindex on job (uuid);

