create table command
(
    id          INTEGER not null constraint table_name_pk primary key autoincrement,
    step_id     INTEGER not null constraint run_step_id_fk references step on update cascade on delete cascade,
    number      INTEGER not null,
    instruction TEXT    not null,
    std_out     TEXT,
    std_error   TEXT
);

create unique index command_id_uindex on command (id);

create unique index command_step_id_number_uindex on command (step_id, number);