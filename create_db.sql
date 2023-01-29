CREATE TABLE "files" (
	"id"	INTEGER,
	"userid"	INTEGER,
	"uuid"	TEXT UNIQUE,
	"filename"	TEXT,
	"upload_date" TEXT,
	"is_public" INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "users" (
	"id"	INTEGER,
	"username"	TEXT UNIQUE,
	"password"	TEXT,
	"email"	TEXT UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);

INSERT INTO users(username)
VALUES ("anonymous");

CREATE INDEX ix_file_name ON files (filename COLLATE NOCASE);