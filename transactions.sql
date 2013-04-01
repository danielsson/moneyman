DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
	id integer primary key autoincrement,
	time integer not null,
	message string,
	amount integer not null,
	type integer not null
);