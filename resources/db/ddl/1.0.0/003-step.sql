create table step
(
    id     INTEGER not null constraint step_pk primary key autoincrement,
    run_id INTEGER not null constraint run_run_id_fk references run on update cascade on delete cascade,
    number INTEGER not null,
    name   TEXT    not null,
    image  TEXT    not null,
    status TEXT
);

create unique index step_id_uindex on step (id);

create unique index step_run_id_number_uindex on step (run_id, number);