CREATE DATABASE IF NOT EXISTS logging_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

create table if not exists logging_db.logging_table
(
	id int auto_increment
		primary key,
	script_type varchar(10) null,
	script_name varchar(512) null,
	feature_name varchar(512) null,
	client_name varchar(50) null,
	url varchar(512) null,
	result boolean null,
    description text null,
	created_date date null,
    created_time time null,
	user_email varchar(100) null
)
charset=utf8;



		
