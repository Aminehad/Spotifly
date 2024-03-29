package main

import (
	songs "middleware/example/internal/controllers/songs"
	"middleware/example/internal/helpers"
	_ "middleware/example/internal/models"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/sirupsen/logrus"
)

func main() {
	r := chi.NewRouter()

	r.Route("/songs", func(r chi.Router) {

		// get all
		r.Get("/", songs.GetSongs)

		r.Route("/{id}", func(r chi.Router) {
			r.Use(songs.Ctx)
			// get one
			r.Get("/", songs.GetSong)
			// delete one
			r.Delete("/", songs.DeleteSong)

			r.Put("/", songs.UpdateSong)
		})

		// create
		r.Post("/", songs.AddSong)

	})

	logrus.Info("[INFO] Web server started. Now listening on *:8181")
	logrus.Fatalln(http.ListenAndServe(":8181", r))
}

func init() {
	db, err := helpers.OpenDB()
	if err != nil {
		logrus.Fatalf("error while opening database : %s", err.Error())
	}
	schemes := []string{

		`CREATE TABLE IF NOT EXISTS songs(
			id VARCHAR(255) PRIMARY KEY NOT NULL UNIQUE,
			title VARCHAR(255) NOT NULL,
			artist VARCHAR(255) NOT NULL,
			filename VARCHAR(255) NOT NULL,
			published DATE NOT NULL
		);`,
	}
	for _, scheme := range schemes {
		if _, err := db.Exec(scheme); err != nil {
			logrus.Fatalln("Could not generate table ! Error was : " + err.Error())
		}
	}
	helpers.CloseDB(db)
}
