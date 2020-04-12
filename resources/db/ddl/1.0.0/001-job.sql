create table job
(
    id   INTEGER not null constraint job_pk primary key autoincrement,
    name TEXT,
    url  TEXT
);

create unique index job_id_uindex on job (id);


