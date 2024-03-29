package collections

import (
	"context"
	"encoding/json"
	"fmt"
	"middleware/example/internal/models"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/gofrs/uuid"
	"github.com/sirupsen/logrus"
)

func Ctx(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Affichage de l'URL de la requete pour un meilleur debug
		logrus.Infof("Request URL: %s", r.URL)

		songID, err := uuid.FromString(chi.URLParam(r, "id"))
		if err != nil {
			logrus.Errorf("parsing error: %s", err.Error())
			customError := &models.CustomError{
				Message: fmt.Sprintf("cannot parse id (%s) as UUID", chi.URLParam(r, "id")),
				Code:    http.StatusUnprocessableEntity,
			}
			w.WriteHeader(customError.Code)
			body, _ := json.Marshal(customError)
			_, _ = w.Write(body)
			return
		}

		ctx := context.WithValue(r.Context(), "songId", songID)
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}
