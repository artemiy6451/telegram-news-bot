create table post(
    id integer primary key autoincrement,
    author varchar(80) not null,
    name varchar(150) not null,
    difficulty varchar(15) not null,
    time_to_read varchar(20) not null,
    description text not null,
    published timestamp default current_timestamp not null,
    url varchar(150) not null
);

create table tag(
    id integer primary key autoincrement,
    name varchar(80) unique not null
);

create table label(
    id integer primary key autoincrement,
    name varchar(80) unique not null
);


create table tags(
    id integer primary key autoincrement,
    tag_id integer not null,
    post_id integer not null,

    foreign key(tag_id) references tag(id),
    foreign key(post_id) references post(id)
);

create table labels(
    id integer primary key autoincrement,
    label_id integer not null,
    post_id integer not null,

    foreign key(label_id) references labels(id),
    foreign key(post_id) references post(id)
);
