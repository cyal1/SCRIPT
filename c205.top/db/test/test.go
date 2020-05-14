package main

// port tcp syn scan

import (
	"fmt"
	"sync"
	"time"
)

func main(){

	chanel:=make(chan int)

wg:=sync.WaitGroup{}
wg.Add(1)
go func ()  {
	defer wg.Done()
	for x:=range chanel{
		time.Sleep(time.Second*2)
		fmt.Println(x)
	}
}()


	chanel<-1
	chanel<-2
	chanel<-3
	close(chanel)
	wg.Wait()
}