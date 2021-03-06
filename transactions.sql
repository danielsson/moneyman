DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS users;


CREATE TABLE users (
	id integer primary key autoincrement,
	active integer not null,
	username text not null,
	password text not null
);

CREATE TABLE transactions (
	id integer primary key autoincrement,
	time integer not null,
	message string,
	amount integer not null,
	type integer not null,
	monthid integer not null,
	uid integer not null,

	FOREIGN KEY(uid) REFERENCES users(id) ON DELETE CASCADE
);
