# Gopher Social


## Libraries Used
- chi - Used for Routing 
`go get github.com/go-chi/chi/v5`
- air - Used for auto reloading
`go install github.com/air-verse/air@latest`
- `pq` - postgres driver
`go get github.com/lib/pq`

## Directory Structure
- go.mod -> 
- bin -> contains the compiled application
- cmd -> contains the executables or entry points of the applications 
    - api -> anything related to http, middlewares, routes.
    - migrate -> implement our owm migration 
- internal -> contains all our internal packages which is not to be exported for API Server
    - will contain storage layers (postgres), data validation, sending emails, rate limitations etc.,
- docs -> auto generated documentation lives here
- scripts -> scripts for setting up our server