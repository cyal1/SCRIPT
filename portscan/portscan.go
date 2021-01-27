package main

import (
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"sync"
	"time"
)

func Ulimit() int64 {
	out, err := exec.Command("ulimit", "-n").Output()
	if err != nil {
		panic(err)
	}
	s := strings.TrimSpace(string(out))
	//log.Println("Open Files limit: ",s)
	i, err := strconv.ParseInt(s, 10, 64)
	if err != nil {
		panic(err)
	}
	return i
}

func ScanPort(ip string, port int, timeout time.Duration) {

	target := fmt.Sprintf("%s:%d", ip, port)
	conn, err := net.DialTimeout("tcp", target, timeout)
	if err != nil {
		e := err.Error()
		if strings.Contains(e, "too many open files") {
			//fmt.Println(e)
			mu.Lock()
			Count.fileCount += 1
			mu.Unlock()
			time.Sleep(500*time.Millisecond)
			ScanPort(ip, port, timeout) // TODO
		} else if strings.Contains(e, "i/o timeout") {
			mu.Lock()
			Count.timoutCount += 1
			mu.Unlock()
			//fmt.Println("timeout",e)
			if options.TimeoutRetry{
				time.Sleep(200*time.Millisecond)
				ScanPort(ip, port, timeout) // TODO
			}
		} else if strings.Contains(e, "connection refused"){
			mu.Lock()
			Count.refusedCount += 1
			mu.Unlock()
		}else{
			mu.Lock()
			Count.anotherErrCount += 1
			mu.Unlock()
			fmt.Println("Error: ",e)
			if options.OtherRetry{
				time.Sleep(200*time.Millisecond)
				ScanPort(ip, port, timeout) // TODO
			}
		}
		return
	}
	mu.Lock()
	Count.openCount += 1
	mu.Unlock()
	openList = append(openList, port)
	fmt.Println(port,"Open")
	conn.Close()
}


var Count struct {
	openCount int
	fileCount int
	timoutCount int
	refusedCount int
	anotherErrCount int
}
var mu sync.RWMutex

type Options struct {
	Threads int
	TimeoutRetry bool
	OtherRetry bool
	Timeout int
	IP string
}
var options = &Options{}

var openList[] int

func main() {
	Count.openCount = 0
	Count.fileCount = 0
	Count.timoutCount = 0
	Count.refusedCount = 0
	Count.anotherErrCount = 0

	wg:=&sync.WaitGroup{}

	flag.IntVar(&options.Threads, "t", 10240, "Number of threads")
	flag.BoolVar(&options.TimeoutRetry, "tretry", false, "Time out port retries (endless loop)")
	flag.BoolVar(&options.OtherRetry, "oretry", true, "Other error retries")
	flag.IntVar(&options.Timeout, "timeout", 2, "Timeout in seconds")
	flag.StringVar(&options.IP, "ip", "", "Target IP")
	flag.Parse()

	if options.IP == ""{
		fmt.Printf("Useage: %s -ip 127.0.0.1\n",os.Args[0])
		os.Exit(0)
	}
	log.Println("Open Files limit: ",Ulimit())
	fmt.Print("Tips: Increase the timeout while increasing the threads is better\n")
	workers := make(chan bool,options.Threads)

	for i:=1;i<=65535;i++{
		wg.Add(1)
		workers <- true
		go func (port int ,ip string, timeout time.Duration)  {
			defer func() {
				<- workers
				wg.Done()
			}()
			ScanPort(ip,port,timeout)

		}(i,options.IP,time.Duration(options.Timeout) * time.Second)
	}
	wg.Wait()
	fmt.Printf("\nOpen Count: %d\nTooManyFile Count: %d\nTimeout Count: %d\nRefuse Count: %d\nOther Error Count: %d\n\n",
		Count.openCount,Count.fileCount,Count.timoutCount,Count.refusedCount,Count.anotherErrCount)

	fmt.Printf("Nmap Command:\nsudo nmap --open -sS -sV -sC -p%s %s\n",strings.Replace(strings.Trim(fmt.Sprint(openList), "[]"), " ", ",", -1),options.IP)
}


