create table changelog
(
    id           INTEGER constraint changelog_pk primary key autoincrement,
    version      TEXT not null,
    author       TEXT,
    comment      TEXT,
    created_date TIMESTAMP default CURRENT_TIMESTAMP
);

create unique index changelog_id_uindex on changelog (id);

create unique index changelog_version_uindex on changelog (version);

