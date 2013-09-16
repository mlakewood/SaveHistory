package main

import (
    "fmt"
    "github.com/ActiveState/tail"
    "net/http"
    "encoding/json"
    "time"
    "bytes"
    "strconv"
)


type HistoryRecord struct{
    Command string
    Time time.Time
}

func main() {
    t, err := tail.TailFile("/Users/mlakewood/.bash_history", tail.Config{Follow: true})
    if err != nil {
        fmt.Println("we have an error: %s", err)
    }
    var timestamp = time.Time{}
    for line := range t.Lines {
        if(line.Text[0] == '#'){
            fmt.Println("We got a hash!")
            timestamp, err := strconv.ParseInt(line.Text[1:], 10, 64)
            if err != nil {
                fmt.Println("error0:", err)
            }
            fmt.Println("Timestamp: ", time.Unix(timestamp, 0))
            continue;
        }else if(timestamp.IsZero()){
            timestamp = time.Now();
        }

        command := HistoryRecord{line.Text, timestamp}
        fmt.Println(command)
        output, err := json.Marshal(command)
        if err != nil{
            fmt.Println("error1:", err)
        }

        b := bytes.NewBufferString(string(output))
        resp, err := http.Post("http://127.0.0.1:5000/history", "text/json", b)
        if err != nil {
            fmt.Println("error2", err)
        }
        resp.Body.Close()
        timestamp = time.Time{}
    }
}
