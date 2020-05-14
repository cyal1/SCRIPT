package graduation

import (
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"math/rand"
	"net/http"
	"net/url"
	"os"
	"regexp"
	"strings"
	"sync"
	"time"

	"github.com/gookit/color"
)

// SubPassivetotal ...
func SubPassivetotal(domain string) (s []string, err error) {
	color.Info.Prompt("Passivetotal Start...")
	// Authorization: Basic admin:admin
	req, _ := http.NewRequest(http.MethodGet, "https://api.passivetotal.org/v2/enrichment/subdomains?query="+domain, nil)
	keyMap := GetApikey("passivetotal").([]interface{})
	// 随机取一个key
	rand.Seed(time.Now().Unix())
	randomKey := keyMap[rand.Intn(len(keyMap))].(map[string]interface{})
	key, value := randomKey["username"].(string), randomKey["password"].(string)
	req.Header.Add("Authorization", "Basic "+base64.StdEncoding.EncodeToString([]byte(key+":"+value)))
	// fmt.Println(req.Header)
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return s, err
	}
	defer resp.Body.Close()
	respByte, _ := ioutil.ReadAll(resp.Body)
	// fmt.Println(string(respByte))
	var html map[string]interface{}
	json.Unmarshal(respByte, &html)
	if elem, ok := html["message"]; ok {
		color.Error.Println("Passivetotal: ", elem)
		return s, err
	}
	for _, v := range html["subdomains"].([]interface{}) {
		s = append(s, fmt.Sprintf("%s.%s", v.(string), domain))
	}
	color.Info.Prompt("Passivetotal Result: %d", len(s))
	return s, nil
}

// SubCrt ...
func SubCrt(s string) (r []string, err error) {
	color.Info.Prompt("crt.sh Start...")
	req, _ := http.NewRequest(http.MethodGet, "https://crt.sh/?q="+s, nil)
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return r, err
	}
	reader, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return r, err
	}
	defer resp.Body.Close()
	// color.Warn.Printf("%s", reader)
	reg, _ := regexp.Compile("(?i)(?:<TD>)([\\.\\w\\d\\-_\\*<>]+)(?:</TD>)")
	match := reg.FindAllSubmatch(reader, -1)
	if match != nil {
		for _, v := range match {
			// fmt.Printf("%s\n", v[1])
			for _, sp := range strings.Split(fmt.Sprintf("%s", v[1]), "<BR>") {
				if ok, _ := regexp.MatchString(`^(?i:([\d\w-_]+\.)+\w+)$`, sp); ok {
					r = append(r, sp)
				}
			}

		}

	}
	color.Info.Prompt("crt.sh Result: %d", len(r))
	return r, nil
}

// SubVirustotal ...
func SubVirustotal(s string) (r []string, err error) {
	color.Info.Prompt("Virustotal Start...")
	keyList := GetApikey("virustotal").([]interface{})
	rand.Seed(time.Now().Unix())
	key := keyList[rand.Intn(len(keyList))].(string)
	resp, err := http.Get("https://www.virustotal.com/vtapi/v2/domain/report?apikey=" + key + "&domain=" + s)
	if err != nil {
		return r, err
	}
	defer resp.Body.Close()
	reader, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return r, err
	}
	var subdomains map[string]interface{}
	json.Unmarshal(reader, &subdomains)
	if subdomains["subdomains"] == nil {
		color.Notice.Prompt("Virustotal: %s", reader)
		return r, nil
	}
	for _, v := range subdomains["subdomains"].([]interface{}) {
		r = append(r, v.(string))
	}
	color.Info.Prompt("Virustotal Result: %d", len(r))
	return r, nil
}

// SubBaidu ...
func SubBaidu(s string) (r []string, err error) {
	color.Info.Prompt("Baidu Start...")
	resp, err := http.Get("https://ce.baidu.com/index/getRelatedSites?site_address=" + s)
	if err != nil {
		return r, err
	}
	defer resp.Body.Close()
	reader, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return r, err
	}
	var subdomains map[string]interface{}
	json.Unmarshal(reader, &subdomains)
	if subdomains["data"] == nil {
		return r, nil
	}
	for _, data := range subdomains["data"].([]interface{}) {
		r = append(r, data.(map[string]interface{})["domain"].(string))
	}
	color.Info.Prompt("Baidu Result: %d", len(r))
	return r, nil
}

// SubHackertarget ...
func SubHackertarget(s string) (r []string, err error) {
	color.Info.Prompt("Hackertarget Start...")
	resp, err := http.Get("https://api.hackertarget.com/hostsearch/?q=" + s)
	if err != nil {
		return r, err
	}
	defer resp.Body.Close()
	reader, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return r, err
	}
	html := fmt.Sprintf("%q", reader)
	html = html[1 : len(html)-1]
	if strings.HasPrefix(html, "API count exceeded") || strings.HasPrefix(html, "error check your search parameter") {
		color.Notice.Prompt("Hackertarget: %s", html)
		return r, nil
	}
	item := strings.Split(html, "\\n")
	for _, v := range item {
		r = append(r, strings.Split(v, ",")[0])
	}
	color.Info.Prompt("Hackertarget Result: %d", len(r))
	return r, nil
}

// SubSpyse spyse.com ... cname findsubdomains.com
func SubSpyse(s string) (r []string, err error) {
	color.Info.Prompt("Spyse Start...")
	// Authorization: Bearer 7e9c6a2b-046c-4fb2-a2a6-c8a2686e71c5
	// authority: spyse.com
	// https://api.spyse.com/v2/data/domain/subdomain?limit=99999999&domain=baidu.com
	// https://spyse.com/api/data/domain/subdomain?limit=100&offset=0&domain=google.com
	keyList := GetApikey("spyse").([]interface{})
	rand.Seed(time.Now().Unix())
	key := keyList[rand.Intn(len(keyList))].(string)
	req, _ := http.NewRequest(http.MethodGet, "https://api.spyse.com/v2/data/domain/subdomain?limit=99999999&domain="+s, nil)
	req.Header.Add("Authorization", "Bearer "+key)
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return r, err
	}
	defer resp.Body.Close()
	respByte, _ := ioutil.ReadAll(resp.Body)
	fmt.Println(string(respByte))
	// 停止施工，rpc error

	// var html map[string]interface{}
	// json.Unmarshal(respByte, &html)
	// if elem, ok := html["message"]; ok {
	// 	color.Error.Println("Passivetotal: ", elem)
	// 	return r, err
	// }
	// for _, v := range html["subdomains"].([]interface{}) {
	// 	s = append(r, fmt.Sprintf("%s.%s", v.(string), s))
	// }
	// color.Info.Prompt("Passivetotal Result: %d", len(s))
	return r, nil
}

// SubRiddler ...
func SubRiddler(s string) (r []string, err error) {
	rand.Seed(time.Now().Unix())
	keyMap := GetApikey("riddler").([]interface{})
	randomKey := keyMap[rand.Intn(len(keyMap))].(map[string]interface{})
	key, value := randomKey["email"].(string), randomKey["password"].(string)
	body := strings.NewReader(fmt.Sprintf(`{"email": "%s", "password": "%s"}`, key, value))
	// req, _ := http.NewRequest(http.MethodPost, "https://riddler.io/auth/login", body)
	// req.Header.Add("Content-Type", "application/json")
	resp, err := http.DefaultClient.Post("https://riddler.io/auth/login", "application/json", body)
	// resp, err := http.DefaultClient.Do(req)
	if err != nil {
		color.Notice.Prompt("%v", err)
		return r, err
	}
	reader, _ := ioutil.ReadAll(resp.Body)
	defer resp.Body.Close()
	var data map[string]interface{}
	json.Unmarshal(reader, &data)
	// fmt.Println(data)
	token := data["response"].(map[string]interface{})["user"].(map[string]interface{})["authentication_token"].(string)
	body = strings.NewReader(fmt.Sprintf(`{"query": "pld:%s"}`, s))
	req, _ := http.NewRequest(http.MethodPost, "https://riddler.io/api/search", body)
	req.Header.Add("Content-Type", "application/json")
	req.Header.Add("Authentication-Token", token)
	// resp, err = http.DefaultClient.Post("https://riddler.io/api/search", "application/json", body)
	resp1, err := http.DefaultClient.Do(req)
	if err != nil {
		color.Notice.Prompt("%v", err)
		return r, err
	}
	reader, _ = ioutil.ReadAll(resp1.Body)
	defer resp1.Body.Close()
	// fmt.Printf("%s", reader)
	var host []interface{}
	json.Unmarshal(reader, &host)
	for _, v := range host {
		r = append(r, v.(map[string]interface{})["host"].(string))
	}
	return r, nil
}

// Fofa ...
func Fofa(s string) (r []string, err error) {
	// https://fofa.so/api/v1/search/all?email=${FOFA_EMAIL}&key=${FOFA_KEY}&qbase64={}
	// domain="qq.com"
	qbase64 := base64.StdEncoding.EncodeToString([]byte("domain=\"" + s + "\""))
	rand.Seed(time.Now().Unix())
	keyMap := GetApikey("fofa").([]interface{})
	randomKey := keyMap[rand.Intn(len(keyMap))].(map[string]interface{})
	key, value := randomKey["email"].(string), randomKey["key"].(string)
	url := fmt.Sprintf("https://fofa.so/api/v1/search/all?email=%s&key=%s&qbase64=%s", key, value, qbase64)
	resp, err := http.DefaultClient.Get(url)
	if err != nil {
		color.Notice.Prompt("%v", err)
		return r, err
	}
	data, _ := ioutil.ReadAll(resp.Body)
	defer resp.Body.Close()
	fmt.Printf("%s", data)
	// 停止施工，fofa coins 不足

	return r, nil
}

// Google ...
func Google(domain string) (r []string, err error) {
	color.Info.Prompt("Google start...")
	chanel := make(chan []string)
	getPage := func(reader []byte) (info []string, nextPage interface{}) {
		var data [][]interface{}
		json.Unmarshal(reader, &data)
		arr1 := data[0][1]
		if arr1 == nil {
			color.Notice.Prompt("%s", reader)
			return r, nil
		}
		if len(arr1.([]interface{})) == 0 {
			return r, nil
		}

		for _, v := range arr1.([]interface{}) {
			info = append(info, v.([]interface{})[5].(string))
		}
		color.Info.Printf("\rINFO: currentPage: %v total: %v\n", data[0][3].([]interface{})[3], data[0][3].([]interface{})[4])
		return info, data[0][3].([]interface{})[1]
	}
	urli := url.URL{}
	urlproxy, _ := urli.Parse("socks5://127.0.0.1:1081")
	client := http.Client{
		Transport: &http.Transport{
			Proxy: http.ProxyURL(urlproxy),
		},
	}
	getPageInfo := func(s []string) (res []string) {
		fmt.Println(s)
		wg := sync.WaitGroup{}
		wg.Add(len(s))
		// https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct/certbyhash?hash=AMrcRRmEh/tSmiAw7Mr%2BxQ1kz9iMU0JU%2B8IYbnPznKc=
		for _, v := range s {
			go func(v string) {
				defer wg.Done()
				v = url.QueryEscape(v)
				url := "https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct/certbyhash?hash=" + v
				fmt.Println(url)
				resp, err := client.Get(url)
				if err != nil {
					color.Notice.Prompt("%v", err)
					os.Exit(1)
					return
				}
				reader, _ := ioutil.ReadAll(resp.Body)
				defer resp.Body.Close()
				var data [][]interface{}
				json.Unmarshal(reader[5:], &data)
				if data[0][1] == nil {
					return
				}
				for _, v := range data[0][1].([]interface{})[7].([]interface{}) {
					// fmt.Println("", v.(string)) // 获取资产
					subdomain := v.(string)
					if strings.HasPrefix(subdomain, "*.") {
						subdomain = subdomain[2:]
					}
					if strings.HasSuffix(subdomain, domain) {
						res = append(res, subdomain)
					}
				}
			}(v)
		}
		wg.Wait()
		return res
	}
	wg := sync.WaitGroup{}
	wg.Add(1)
	go func() {
		defer wg.Done()
		for v := range chanel {
			t := getPageInfo(v)
			r = append(r, t...)
		}
	}()
	resp, err := client.Get("https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct/certsearch?include_subdomains=true&domain=" + domain)
	if err != nil {
		color.Notice.Println(err)
		return r, errors.New("connect google error")
	}
	reader, _ := ioutil.ReadAll(resp.Body)
	defer resp.Body.Close()
	pageList, nextPage := getPage(reader[5:])
	chanel <- pageList
	for nextPage != nil {
		resp, err = client.Get("https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct/certsearch/page?p=" + nextPage.(string))
		if err != nil {
			color.Notice.Prompt("%v", err)
			break
		}
		reader, _ := ioutil.ReadAll(resp.Body)
		defer resp.Body.Close()
		pageList, nextPage = getPage(reader[5:])
		chanel <- pageList
	}
	close(chanel)
	wg.Wait()
	color.Info.Prompt("Google Result: %d", len(r))
	return r, nil
}

// GetSubdomains ...
func GetSubdomains(domain string) ([]string, error) {
	var r []string
	wg := sync.WaitGroup{}
	if ok, _ := regexp.MatchString(`^(?i:([\d\w-_]+\.)+\w+)$`, domain); !ok {
		return nil, fmt.Errorf("%s Format Error", domain)
	}
	domain = strings.ToLower(domain)
	type fun func(string) ([]string, error)
	// funcs := []fun{SubHackertarget, SubCrt, SubBaidu, SubPassivetotal, SubRiddler, SubVirustotal, Google}
	funcs := []fun{Google}
	for _, f := range funcs {
		wg.Add(1)
		go func(f fun) {
			defer wg.Done()
			a, err := f(domain)
			if err != nil {
				color.Error.Prompt("%v", err)
				return
			}
			r = append(r, a...)
		}(f)
	}
	wg.Wait()
	r = Uniq(r)
	color.Comment.Prompt("After Deduplication, Remaining alive: %d", len(r))
	return r, nil
}
