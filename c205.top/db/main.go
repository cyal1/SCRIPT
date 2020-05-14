package main

import (
	"database/sql"
	"fmt"
	"os"

	"github.com/gookit/color"
	_ "github.com/mattn/go-sqlite3"
)

type db struct {
	db         *sql.DB
	InserStmt  *sql.Stmt
	UpdateStmt *sql.Stmt
	ShowStmt   *sql.Stmt
}

func main() {

	db, err := sql.Open("sqlite3", "./subdomain.db")
	if err != nil {
		color.Error.Prompt("%v", err)
		os.Exit(0)
	}
	defer db.Close()

	sqlStmt := `
	CREATE TABLE IF NOT EXISTS "subdomain" (
		"ID"	INTEGER UNIQUE,
		"PREFIX"	TEXT UNIQUE,
		"RANK"	INTEGER NOT NULL DEFAULT 0,
		PRIMARY KEY("ID" AUTOINCREMENT)
	);
	CREATE INDEX IF NOT EXISTS "rank"  ON "subdomain" (
		"RANK"	DESC,
		"PREFIX"
	);
	CREATE TABLE IF NOT EXISTS "history" (
		"ID"	INTEGER UNIQUE,
		"DOMAIN"	TEXT NOT NULL UNIQUE,
		"LATEST"	datetime default current_timestamp,
		PRIMARY KEY("ID" AUTOINCREMENT)
	);
	CREATE UNIQUE INDEX IF NOT EXISTS "domain"  ON "history" (
		"DOMAIN"
	);
	`
	_, err = db.Exec(sqlStmt)
	if err != nil {
		color.Error.Prompt("%v", err)
		return
	}

	showtables(db, "subdomain")

	// stmt.Exec("wangshubo")
	// test := "SELECT * FROM sqlite_master"
	// r, err := db.Exec(test)
	// if err != nil {
	// 	log.Println(err)
	// 	return
	// }
	// a, b := r.LastInsertId()
	// c, d := r.RowsAffected()
	// fmt.Println(a, b, c, d)
}

func showtables(db *sql.DB, tablename string) {
	rows, _ := db.Query("SELECT * FROM " + tablename)
	var x interface{}
	var x1 interface{}
	var x2 interface{}

	for rows.Next() {
		err := rows.Scan(&x, &x1, &x2)
		if err != nil {
			fmt.Println(err)
		}
		fmt.Println(x, x1, x2)
	}
	rows.Close()
}

// Insert ...
func Insert(db *sql.DB, prefix string) {
	stmt, err := db.Prepare("INSERT INTO subdomain(PREFIX) values(?)")
	if err != nil {
		color.Error.Prompt("%v", err)
		return
	}
	stmt.Exec(prefix)
	stmt.Close()
}

// Inital ...
func Inital() (*sql.DB, error) {
	db, err := sql.Open("sqlite3", "subdomain.db")
	if err != nil {
		return db, err
	}
	return db, nil
}
