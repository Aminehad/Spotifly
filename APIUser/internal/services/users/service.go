package collections

import (
	"database/sql"
	"middleware/example/internal/models"
	repository "middleware/example/internal/repositories/users"
	"net/http"

	"github.com/gofrs/uuid"
	"github.com/sirupsen/logrus"
)

func GetAllUsers() ([]models.Users, error) {
	var err error
	// calling repository
	users, err := repository.GetAllUsers()
	// managing errors
	if err != nil {
		logrus.Errorf("error retrieving users : %s", err.Error())
		return nil, &models.CustomError{
			Message: "Something went wrong",
			Code:    500,
		}
	}

	return users, nil
}

func GetUserById(id uuid.UUID) (*models.Users, error) {
	user, err := repository.GetUserById(id)
	if err != nil {
		if err.Error() == sql.ErrNoRows.Error() {
			return nil, &models.CustomError{
				Message: "User not found",
				Code:    http.StatusNotFound,
			}
		}
		logrus.Errorf("error retrieving User : %s", err.Error())
		return nil, &models.CustomError{
			Message: "Something went wrong",
			Code:    500,
		}
	}

	return user, err
}
func CreateUser(user *models.Users) (*models.Users, error) {
	// calling repository
	user, err := repository.CreateUser(user)
	// managing errors
	if err != nil {
		logrus.Errorf("error creating user : %s", err.Error())
		return nil, &models.CustomError{
			Message: "Something went wrong",
			Code:    500,
		}
	}

	return user, nil
}
func DeleteUserByID(id uuid.UUID) error {
	// calling repository
	err := repository.DeleteUserByID(id)
	// managing errors
	if err != nil {
		logrus.Errorf("error deleting user : %s", err.Error())
		return &models.CustomError{
			Message: "Something went wrong",
			Code:    500,
		}
	}

	return nil
}
func ModifyUser(id uuid.UUID, user *models.Users) (*models.Users, error) {
	anuser, err1 := repository.GetUserById(id)
	if err1 != nil {
		logrus.Errorf("error retrieving User : %s", err1.Error())
		return nil, &models.CustomError{
			Message: "Something went wrong",
			Code:    500,
		}
	}
	if user.Name == "" {
		user.Name = anuser.Name
	}
	if user.Email == "" {
		user.Email = anuser.Email
	}

	// calling repository
	user, err := repository.ModifyUser(id, user)
	// managing errors
	if err != nil {
		logrus.Errorf("error updating user : %s", err.Error())
		return nil, &models.CustomError{
			Message: "Something went wrong",
			Code:    500,
		}
	}

	return user, nil
}
