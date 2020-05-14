import requests
from urllib import parse
import json
import os
import subprocess

# phantomjs 版
def getDomain(url):
	print(url)
	# stdout = os.system(f"D:\\phantomjs\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe D:\\phantomjs\\test.js {url}")
	res = subprocess.Popen([ "D:\\phantomjs\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe", "D:\\phantomjs\\test.js", url ], stdout=subprocess.PIPE)
	json_data = parse.unquote(res.stdout.read().decode())[36:]
	print(json_data)
	include_domain = json.loads(json_data)['target']['scope']['include']
	# print(include_domain)
	for host in include_domain:
		# print(host)
		print(host['host'])


api_url = 'https://hackerone.com/graphql'
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
data = '{"operationName":"DirectoryQuery","variables":{"where":{"_and":[{"_or":[{"offers_bounties":{"_eq":true}},\
		{"external_program":{"offers_rewards":{"_eq":true}}}]},{"response_efficiency_percentage":{"_gt":80}},\
		{"triage_subscriptions":{"is_active":true}},{"structured_scopes":{"_and":[{"asset_type":{"_eq":"URL"}},{"is_archived":false}]}},\
		{"_or":[{"submission_state":{"_eq":"open"}},{"submission_state":{"_eq":"api_only"}},{"external_program":{"id":{"_is_null":false}}}]},\
		{"external_program":{"id":{"_is_null":true}}},{"_or":[{"_and":[{"state":{"_neq":"sandboxed"}},{"state":{"_neq":"soft_launched"}}]},\
		{"external_program":{"id":{"_is_null":false}}}]}]},"first":25,"secureOrderBy":{"started_accepting_at":{"_direction":"DESC"}}\
		},"query":"query DirectoryQuery($cursor: String, $secureOrderBy: FiltersTeamFilterOrder, $where: FiltersTeamFilterInput) {\\n  me {\\n    id\\n    edit_unclaimed_profiles\\n    h1_pentester\\n    __typename\\n  }\\n  teams(first: 9999, after: $cursor, secure_order_by: $secureOrderBy, where: $where) {\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n      __typename\\n    }\\n    edges {\\n      node {\\n        id\\n        bookmarked\\n        ...TeamTableResolvedReports\\n        ...TeamTableAvatarAndTitle\\n        ...TeamTableLaunchDate\\n        ...TeamTableMinimumBounty\\n        ...TeamTableAverageBounty\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment TeamTableResolvedReports on Team {\\n  id\\n  resolved_report_count\\n  __typename\\n}\\n\\nfragment TeamTableAvatarAndTitle on Team {\\n  id\\n  profile_picture(size: medium)\\n  name\\n  handle\\n  submission_state\\n  triage_active\\n  state\\n  external_program {\\n    id\\n    __typename\\n  }\\n  ...TeamLinkWithMiniProfile\\n  __typename\\n}\\n\\nfragment TeamLinkWithMiniProfile on Team {\\n  id\\n  handle\\n  name\\n  __typename\\n}\\n\\nfragment TeamTableLaunchDate on Team {\\n  id\\n  started_accepting_at\\n  __typename\\n}\\n\\nfragment TeamTableMinimumBounty on Team {\\n  id\\n  currency\\n  base_bounty\\n  __typename\\n}\\n\\nfragment TeamTableAverageBounty on Team {\\n  id\\n  currency\\n  average_bounty_lower_amount\\n  average_bounty_upper_amount\\n  __typename\\n}\\n"}'
res = requests.post(api_url,json = json.loads(data))
json_data = json.loads(res.text)
list_data = json_data['data']['teams']['edges']
for path in list_data:
	hackerone_url = 'https://hackerone.com/' + path['node']['handle']
	getDomain(hackerone_url)
