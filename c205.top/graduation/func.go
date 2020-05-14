package graduation

import (
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/gookit/color"
	"github.com/miekg/dns"
	yaml "gopkg.in/yaml.v3"
)

// Set ...
type Set []string

// WaitGroupWithCount ...
type WaitGroupWithCount struct {
	sync.WaitGroup
	Count int
}

// HTML ...
type HTML struct {
	url    string
	Status string
	Length int
	Title  string
	Banner struct {
		Server      string
		Language    string
		Cache       string
		ContentType string
	}
}

// Uniq 内存换时间，速度较快
func Uniq(r Set) (ret Set) {
	m := make(map[string]bool, len(r)>>1)
	ret = make(Set, 0, len(r)>>1)
	for _, v := range r {
		if _, ok := m[v]; !ok {
			m[v] = true
			ret = append(ret, v)
		}
	}
	return ret
}

// Contains ...
func (set *Set) Contains(domain string) bool {
	// build-in
	// if !sort.StringsAreSorted(*s) {
	// 	sort.Strings(*s)
	// }
	// fmt.Println(sort.SearchStrings(*s, domain))
	// fmt.Println(*s)
	// if index := sort.SearchStrings(*s, domain); len(*s) != 0 && index < len(*s)-1 && (*s)[index] == domain {
	// 	return true
	// }
	// return false

	// 二分法查找
	if !sort.StringsAreSorted(*set) {
		sort.Strings(*set)
	}
	start, end := 0, len(*set)-1
	for start <= end {
		m := (start + end) >> 1
		if (*set)[m] > domain {
			end = m - 1
		} else if (*set)[m] < domain {
			start = m + 1
		} else {
			return true
		}
	}
	return false
}

// Add ...
func (set *Set) Add(s ...string) {
	if len(s) == 0 {
		return
	}
	*set = append(*set, s...)
	*set = Uniq(*set)
}

// GetApikey ...
func GetApikey(apiName string) interface{} {
	yamlFileName := "keys.yaml"
	fileStream, err := ioutil.ReadFile(yamlFileName)
	// fmt.Println(os.Getwd())
	if err != nil {
		// fmt.Println(err)
		panic(err)
	}
	var keyMap map[string]interface{}
	e := yaml.Unmarshal(fileStream, &keyMap)
	if e != nil {
		panic("apikeyFile format error")
	}
	// fmt.Println(keyMap[apiName])
	return keyMap[apiName]
}

// Host ...
type Host struct {
	Domain string
	CNAME  []string
	IP     []string
	Err    error
}

// Dig ...
func Dig(domain string, dnsServer []string, proto string, timeout time.Duration) Host {
	var host Host
	host.Domain = domain
	client := dns.Client{
		Net:     proto,
		Timeout: timeout * time.Second,
	}
	msg := dns.Msg{}
	msg.SetQuestion(domain+".", dns.TypeA)
	for i := 0; i < len(dnsServer); i++ {
		dig, _, err := client.Exchange(&msg, dnsServer[i]+":53")
		if err != nil {
			// color.Notice.Tips("lookup %s %s", domain, err) // 后期取消
			continue
		}
		if len(dig.Answer) != 0 {
			// odm-builds.builder.pt.xiaomi.com. 60 IN CNAME   odm-builds.builder.pt.xiaomi.com.v.mi-dun.com.
			// 判断最终解析是否是 cname,并且以srv.结尾
			if v, ok := dig.Answer[len(dig.Answer)-1].(*dns.CNAME); ok && strings.HasSuffix(v.Target, "srv.") {
				host.Err = fmt.Errorf("lookup %s on %s:53: no such host", domain, dnsServer[i])
				return host
			}
			// 遍历域名解析列表
			for _, ans := range dig.Answer {
				if recordCNAME, isCNAMEType := ans.(*dns.CNAME); isCNAMEType {
					host.CNAME = append(host.CNAME, recordCNAME.Target[:len(recordCNAME.Target)-1])
				}
				if recordA, isAType := ans.(*dns.A); isAType {
					host.IP = append(host.IP, recordA.A.String())
				}
			}
			return host
		}
		// no Answer, no such host
		host.Err = fmt.Errorf("lookup %s on %s:53: no such host", domain, dnsServer[i])
		return host
	}
	host.IP, host.Err = net.LookupHost(domain)
	if host.Err != nil {
		color.Error.Tips("%v", host.Err)
	}
	return host
}

// GetHTML ...
func GetHTML(client *http.Client, host string) (HTML, error) {
	var html HTML
	html.url = host
	t, err := net.ResolveTCPAddr("tcp", host+":443")
	if err != nil {
		color.Error.Println("ResolveTCPAddr: ", err)
		return html, err
	}
	conn, err := net.DialTimeout("tcp", t.String(), time.Second*5)
	if err != nil {
		conn, err = net.DialTimeout("tcp", t.IP.String()+":80", time.Second*5)
		if err != nil {
			// need scan port
			color.Notice.Tips("%s's 443 port Closed! %v", host, err)
			color.Notice.Tips("%s's 80 port Closed! %v", host, err)
			color.Comment.Prompt("%s need to scan port", host)
			return html, err
		}
		defer conn.Close()
		color.Notice.Tips("%s's 443 port Closed! %v", host, err)
		html.url = "http://" + host + "/"
	} else {
		defer conn.Close()
		html.url = "https://" + host + "/"
	}
	req, _ := http.NewRequest(http.MethodGet, html.url, nil)
	req.Header.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36")
	req.Close = true
	resp, err := client.Do(req)
	if err != nil {
		// 请求失败
		color.Error.Prompt("%v", err)
		return html, err
	}
	defer resp.Body.Close()
	html.Status = resp.Status
	if resp.Header.Has("Server") {
		html.Banner.Server = strings.Join(resp.Header["Server"], ";")
	}
	if resp.Header.Has("Language") {
		html.Banner.Language = strings.Join(resp.Header["Language"], ";")
	}
	if resp.Header.Has("Content-Type") {
		html.Banner.ContentType = strings.Join(resp.Header["Content-Type"], ";")
	}
	if resp.Header.Has("X-Cache") || resp.Header.Has("Cache-Control") {
		html.Banner.Cache = "Has Cache"
	}
	// X-Powered-By
	if resp.Header.Has("X-Powered-By") {
		html.Banner.Server = html.Banner.Server + ";" + strings.Join(resp.Header["X-Powered-By"], ";")
	}
	respByte, _ := ioutil.ReadAll(resp.Body)
	if resp.Header.Has("Content-Length") {
		html.Length, _ = strconv.Atoi(resp.Header["Content-Length"][0])
	} else {
		html.Length = len(string(respByte))
	}
	r, _ := regexp.Compile(`(?Ui:<title>[\s ]*([\s\S]*)[\s ]*</?title>)`)
	test := r.FindStringSubmatch(string(respByte))
	if len(test) != 0 {
		html.Title = strings.Replace(test[1], "\n", "", -1)
	}
	return html, nil
}

// PortScan ...
func PortScan(ip string, ports []string) []string {
	var openPorts []string
	var wg sync.WaitGroup
	for _, v := range ports[0:100] {
		wg.Add(1)
		go func(v string) {
			conn, err := net.DialTimeout("tcp", ip+":"+v, time.Second*5)
			if err == nil {
				openPorts = append(openPorts, v)
				conn.Close()
			}
			wg.Done()
		}(v)
	}
	wg.Wait()
	return openPorts
}

// OutputTerm ...
func OutputTerm(html HTML) {
	fmt.Println(html)
}

// OutputJSON ...
func OutputJSON(html HTML) {
	fmt.Println(html)
}

// OutputHTML ...
func OutputHTML(filename string, html HTML) {
	elem := `</td><td>`
	var build strings.Builder
	build.Grow(150)
	build.WriteString(`<tr><td><a href="`)
	build.WriteString(html.url)
	build.WriteString(`" target="_blank">`)
	build.WriteString(html.url)
	build.WriteString(`</a></td><td>`)
	build.WriteString(html.Status)
	build.WriteString(elem)
	build.WriteString(strconv.Itoa(html.Length))
	build.WriteString(elem)
	build.WriteString(html.Title)
	build.WriteString(elem)
	build.WriteString("Server: ")
	build.WriteString(html.Banner.Server)
	build.WriteString(" Language: ")
	build.WriteString(html.Banner.Language)
	build.WriteString(" ContentType: ")
	build.WriteString(html.Banner.ContentType)
	build.WriteString(" Cache: ")
	build.WriteString(html.Banner.Cache)
	build.WriteString("</td></tr>\n")
	s := build.String()
	// fmt.Print(s)
	fp, err := os.OpenFile(filename, os.O_WRONLY|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		color.Error.Println("open ", filename, " error")
		os.Exit(-1)
	}
	defer fp.Close()
	fp.WriteString(s)
}

// SliceEqual ...
func SliceEqual(a, b []string) bool {
	if len(a) != len(b) {
		return false
	}
	if (a == nil) != (b == nil) {
		return false
	}
	for i, v := range a {
		if v != b[i] {
			return false
		}
	}
	return true
}
