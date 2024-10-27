package main

import (
	"log"

	"github.com/NavinKumarMNK/My-Works/tree/main/go/projects/GopherSocial/internal/db"
	"github.com/NavinKumarMNK/My-Works/tree/main/go/projects/GopherSocial/internal/env"
	"github.com/NavinKumarMNK/My-Works/tree/main/go/projects/GopherSocial/internal/store"
)

func main() {
	cfg := config{
		addr: env.GetString("ADDR", ":8080"),
		db: dbConfig{
			addr: env.GetString("DB_ADDR", "postgres://admin:adminpassword@localhost/social?sslmode=disable"),
			maxOpenConns: env.GetInt("DB_MAX_OPEN_CONNS", 30),
			maxIdleConns: env.GetInt("DB_MAX_IDLE_CONNS", 30),
			maxIdleTime: env.GetString("DB_MAX_IDLE_TIME", "15m"),
		},
	}

	db, err := db.New(
		cfg.db.addr,
		cfg.db.maxOpenConns,
		cfg.db.maxIdleConns,
		cfg.db.maxIdleTime,
		 
	)

	if err != nil {
		log.Panic(err)
	}

	defer db.Close()
	log.Println("Database Connection Pool Established")

	store := store.NewStorage(db)
	app := &application{
		config: cfg, 
		store: store,
	}
	
	err = app.run()
	if err != nil{
		log.Fatal(err)
	}
}
