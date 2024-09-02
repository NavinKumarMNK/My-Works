// An example of REST API
package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"time"

	"github.com/go-chi/chi"
	chimiddle "github.com/go-chi/chi/middleware"
	"github.com/gorilla/schema"
	log "github.com/sirupsen/logrus"
)

// ~/api - we will have specs like parameters & response types for our endpoint & put our yaml spec file
// ~/api/api.go
// This represetns the parameters our API endpoint take
type CoinBalanceParams struct {
	Username string
}

type CoinBalanceResponse struct {
	Code    int
	Balance int64
}

type Error struct {
	Code    int
	Message string
}

func writeError(w http.ResponseWriter, message string, code int) {
	resp := Error{
		Code:    code,
		Message: message,
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)

	json.NewEncoder(w).Encode(resp) // Create a json with Response Writer and encode error response
}

var (
	RequestErrorHandler = func(w http.ResponseWriter, err error) {
		writeError(w, err.Error(), http.StatusBadRequest) // Error Raised because of incorrect request
	}
	InternalErrorHandler = func(w http.ResponseWriter) {
		writeError(w, "An Unexpected Error Occurred", http.StatusInternalServerError) // Error in the code
	}
)

// ~/internal - contains most of the code for the api
// ~/internal/handler/get_coin_balance.go
func GetCoinBalance(w http.ResponseWriter, r *http.Request) {
	var params = CoinBalanceParams{}
	var decoder *schema.Decoder = schema.NewDecoder()
	var err error

	err = decoder.Decode(&params, r.URL.Query())
	if err != nil {
		log.Error(err)
		InternalErrorHandler(w)
		return
	}

	var database *DatabaseInterface
	database, err = NewDatabase()
	if err != nil {
		InternalErrorHandler(w)
		return
	}

	var tokenDetails *CoinDetails
	tokenDetails = (*database).GetUserCoins(params.Username)
	if tokenDetails == nil {
		log.Error(err)
		InternalErrorHandler(w)
		return
	}

	var response = CoinBalanceResponse{
		Balance: (*tokenDetails).Coins,
		Code:    http.StatusOK,
	}

	w.Header().Set("Content-Type", "application/json")
	err = json.NewEncoder(w).Encode(response)
	if err != nil {
		log.Error(err)
		InternalErrorHandler(w)
		return
	}
}

// ~/internal/handler/api.go
func Handler(r *chi.Mux) {
	// middleware
	r.Use(chimiddle.StripSlashes)

	// routes
	r.Route("/account", func(router chi.Router) {
		router.Use(Authorization)
		router.Get("/coins", GetCoinBalance)
	})
}

// ~/internal/tools/mockdb.go
type mockDB struct{}

var mockLoginDetails = map[string]LoginDetails{
	"alex": {
		AuthToken: "123ABC",
		Username:  "alex",
	},
	"jason": {
		AuthToken: "456DEF",
		Username:  "jason",
	},
	"marie": {
		AuthToken: "789GHI",
		Username:  "marie",
	},
}

var mockCoinDetails = map[string]CoinDetails{
	"alex": {
		Coins:    100,
		Username: "alex",
	},
	"jason": {
		Coins:    200,
		Username: "jason",
	},
	"marie": {
		Coins:    300,
		Username: "marie",
	},
}

func (d *mockDB) GetUserLoginDetails(username string) *LoginDetails {
	// Simulate DB call
	time.Sleep(time.Second * 1)

	var clientData = LoginDetails{}
	clientData, ok := mockLoginDetails[username]
	if !ok {
		return nil
	}

	return &clientData
}

func (d *mockDB) GetUserCoins(username string) *CoinDetails {
	// Simulate DB call
	time.Sleep(time.Second * 1)

	var clientData = CoinDetails{}
	clientData, ok := mockCoinDetails[username]
	if !ok {
		return nil
	}

	return &clientData
}

func (d *mockDB) SetupDatabase() error {
	return nil
}

// ~/internal/tools/database.go
type LoginDetails struct {
	AuthToken string
	Username  string
}

type CoinDetails struct {
	Coins    int64
	Username string
}

type DatabaseInterface interface {
	GetUserLoginDetails(username string) *LoginDetails
	GetUserCoins(usernmae string) *CoinDetails
	SetupDatabase() error
}

func NewDatabase() (*DatabaseInterface, error) {
	var database DatabaseInterface = &mockDB{}
	var err error = database.SetupDatabase()
	if err != nil {
		log.Error(err)
		return nil, err
	}

	return &database, nil
}

// ~/internal/middleware/authorization.go
var UnAuthorizedError = errors.New("Invalid username or token.")

// middleware should look like this, takes in http.Handler and returns the http.Handler
func Authorization(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var username string = r.URL.Query().Get("username")
		var token = r.Header.Get("Authorization")
		var err error

		if username == "" || token == "" {
			log.Error(UnAuthorizedError)
			RequestErrorHandler(w, UnAuthorizedError)
			return
		}

		var database *DatabaseInterface
		database, err = NewDatabase()
		if err != nil {
			InternalErrorHandler(w)
			return
		}

		var loginDetails *LoginDetails
		loginDetails = (*database).GetUserLoginDetails(username)
		if loginDetails == nil || token != (*loginDetails).AuthToken {
			log.Error(UnAuthorizedError)
			RequestErrorHandler(w, UnAuthorizedError)
			return
		}

		next.ServeHTTP(w, r) // Calls next middleware / handler func

	})
}

// ~/cmd/api - contains our main.go file
// ~/cmd/api/main.go
func main() {
	log.SetReportCaller(true)
	var router *chi.Mux = chi.NewRouter()
	Handler(router)
	fmt.Println("Starting GO API Service...")
	err := http.ListenAndServe("localhost:8000", router)
	if err != nil {
		log.Error(err)
	}

}
