import requests
import json
from selenium import webdriver
from urllib import parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor


def getProgram(api, endCursor=''):
    header = {
     "authority":"hackerone.com",
     "accept":"*/*",
     "x-auth-token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODMyOTY1MzB9.ZbkhHLp_XP8Xe4JPHGpigKibeF5rsXe576JKc_ostuY----4398899",
     "sec-fetch-dest":"empty",
     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
     "content-type":"application/json",
     "origin":"https://hackerone.com",
     "sec-fetch-site":"same-origin",
     "sec-fetch-mode":"cors",
     "referer":"https://hackerone.com/directory/programs?offers_bounties=true&high_response_efficiency=true&managed=true&asset_type=URL&order_direction=DESC&order_field=started_accepting_at",
     "accept-language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
     "cookie":""
    }
    data = """{"operationName":"DirectoryQuery","variables":{\
    "where":{"_and":[{"_or":[{"offers_bounties":{"_eq":true}},\
    {"external_program":{"offers_rewards":{"_eq":true}}}]},\
    {"structured_scopes":{"_and":[{"asset_type":{"_eq":"URL"}},{"is_archived":false}]}},\
    {"_or":[{"submission_state":{"_eq":"open"}},{"submission_state":{"_eq":"api_only"}},\
    {"external_program":{"id":{"_is_null":false}}}]},{"external_program":{"id":{"_is_null":true}}},\
    {"_or":[{"_and":[{"state":{"_neq":"sandboxed"}},{"state":{"_neq":"soft_launched"}}]},\
    {"external_program":{"id":{"_is_null":false}}}]}]},\
    "first":25,"secureOrderBy":{"started_accepting_at":{"_direction":"DESC"}},"cursor":"%s"},\
    "query":"query DirectoryQuery($cursor: String, $secureOrderBy: FiltersTeamFilterOrder, \
    $where: FiltersTeamFilterInput) {\\n  me {\\n id\\n edit_unclaimed_profiles\\n h1_pentester\\n __typename\\n  }\\n  \
    teams(first: 999, after: $cursor, secure_order_by: $secureOrderBy, where: $where) \
    {\\n pageInfo {\\n endCursor\\n hasNextPage\\n __typename\\n }\\n \
    edges {\\n node {\\n id\\n bookmarked\\n ...TeamTableResolvedReports\\n ...TeamTableAvatarAndTitle\\n ...TeamTableLaunchDate\\n ...TeamTableMinimumBounty\\n ...TeamTableAverageBounty\\n __typename\\n }\\n \
    __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment TeamTableResolvedReports on Team \
    {\\n  id\\n  resolved_report_count\\n  __typename\\n}\\n\\nfragment TeamTableAvatarAndTitle on Team \
    {\\n  id\\n  profile_picture(size: medium)\\n  name\\n  handle\\n  submission_state\\n  triage_active\\n  state\\n  external_program {\\n id\\n __typename\\n  }\\n  \
    ...TeamLinkWithMiniProfile\\n  __typename\\n}\\n\\nfragment TeamLinkWithMiniProfile on Team \
    {\\n  id\\n  handle\\n  name\\n  __typename\\n}\\n\\nfragment TeamTableLaunchDate on Team \
    {\\n  id\\n  started_accepting_at\\n  __typename\\n}\\n\\nfragment TeamTableMinimumBounty on Team \
    {\\n  id\\n  currency\\n  base_bounty\\n  __typename\\n}\\n\\nfragment TeamTableAverageBounty on Team \
    {\\n  id\\n  currency\\n  average_bounty_lower_amount\\n  average_bounty_upper_amount\\n  __typename\\n}\\n"}
    """%endCursor
    res = requests.post(api,json = json.loads(data))
    return json.loads(res.text)

# selenium 版
def getDomain(url):

    chrome_options = webdriver.ChromeOptions()
    # 使用headless无界面浏览器模式
    chrome_options.add_argument('--headless')  
    chrome_options.add_argument('--disable-gpu')  
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    try:
        element = WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[@class='js-application-root full-size']/div/div/div/div/div/div/div/div/div/ul[@class='daisy-list daisy-list--horizontal']/li[1]/span/a[@class='daisy-link spec-download-burp-suite-project-file']"))
        )
    except Exception as e:
        print('-'*100)
        print(url)
        print('Do not have burp suite project file!')
    else:
        print('-'*100)
        print(url)
        res = element.get_attribute('href')
        json_data = parse.unquote(res)[36:]
        # print(json_data)
        include_domain = json.loads(json_data)['target']['scope']['include']
        # print(json.dumps(include_domain,indent=4))
        for host in include_domain:
            print(host['host'])
    finally:
        browser.quit()

def main():

    api = 'https://hackerone.com/graphql'
    programsList = []
    hasNextPage = True
    endCursor = ''

    while hasNextPage:
        json_data = getProgram(api,endCursor)
        item = json_data['data']['teams']['edges']
        for path in item:
            url = 'https://hackerone.com/' + path['node']['handle']
            programsList.append(url)
        hasNextPage = json_data['data']['teams']['pageInfo']['hasNextPage']
        endCursor = json_data['data']['teams']['pageInfo']['endCursor']

    with ThreadPoolExecutor(max_workers = 20) as executor:
        for url in programsList:
            executor.submit(getDomain,url)
            # break

if __name__ == '__main__':
    main()