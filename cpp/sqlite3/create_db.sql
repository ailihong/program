PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
 
CREATE TABLE face(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL, 
	tdatetime DATETIME DEFAULT (datetime('now', 'localtime')),
	feature blob NOT NULL
);
COMMIT;
