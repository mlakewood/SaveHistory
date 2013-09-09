package main

import (
    "fmt"
    "net/http"
    "time"
    "encoding/json"
)

type HistoryRecord struct{
    Command string
    Time time.Time
}

func history(w http.ResponseWriter, req *http.Request) {
    decoder := json.NewDecoder(req.Body)
    var t HistoryRecord   
    err := decoder.Decode(&t)
    if err != nil {
        fmt.Println("Error:", err)
    }
    fmt.Println(t)
    fmt.Fprintf(w, "Hi there, I love %s!", req.URL.Path[1:])
}

func main() {
    http.HandleFunc("/history", handler)
    http.ListenAndServe(":5000", nil)
}