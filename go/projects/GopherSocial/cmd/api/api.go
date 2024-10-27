package main

import (
	"log"
	"net/http"
	"time"

	"github.com/NavinKumarMNK/My-Works/tree/main/go/projects/GopherSocial/internal/store"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

type application struct {
	config config
	store store.Storage
}

type config struct {
	addr string
	db dbConfig
}

type dbConfig struct {
	addr string
	maxOpenConns int
	maxIdleConns int
	maxIdleTime string
}

func (app *application) mount() http.Handler {
	r := chi.NewRouter()
	
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	r.Use(middleware.Recoverer)
	r.Use(middleware.Logger)
	r.Use(middleware.Timeout(60 * time.Second))

	r.Route("/v1", func (r chi.Router) {
		r.Get("/health", app.healthCheckHandler)
	})
	
	
	return r
}


func (app *application) run() error {
	mux := app.mount()

	srv := http.Server{
		Addr: app.config.addr,
		Handler: mux,
		WriteTimeout: time.Second * 30,
		ReadTimeout: time.Second * 10,
		IdleTimeout: time.Minute,
	}

	log.Printf("Server Started at %s", app.config.addr)

	return srv.ListenAndServe()
}