USE order;

CREATE TABLE orders(
    id bigint primary key auto_increment,
    item_id bigint not null,
    status varchar(255) default 'pending',
    created_at datetime,
    updated_at datetime
);

CREATE TABLE stocks(
    id bigint primary key auto_increment,
    item_id bigint not null,
    created_at datetime,
    updated_at datetime
);

CREATE TABLE deliveries(
    id bigint primary key auto_increment,
    order_id bigint not null,
    created_at datetime,
    updated_at datetime
);

INSERT INTO stocks(item_id, count) VALUES(1, 100);
INSERT INTO stocks(item_id, count) VALUES(2, 100);
INSERT INTO stocks(item_id, count) VALUES(3, 100);