# https://www.cnblogs.com/cheyunhua/p/11238489.html
# install  curl 
# useradd -m elastic && su elastic
# mv *.tar.gz /home/elastic/ && chown elastic:elastic *.tar.gz

### 系统配置 root 用户执行 ###
cat <<EOF >>/etc/security/limits.conf
soft nofile 65536
hard nofile 65536
soft nproc 65536
hard nproc 65536
EOF

chmod 766 /var/log/secure
# su elastic
### elatic 用户执行 ###

ES="/home/elastic/elasticsearch-7.11.2-linux-x86_64.tar.gz"
LS="/home/elastic/logstash-7.11.2-linux-x86_64.tar.gz"
KB="/home/elastic/kibana-7.11.2-linux-x86_64.tar.gz"
tar -zxf $ES
tar -zxf $LS
tar -zxf $KB


### 安装elasticsearch ###
# 修改配置文件
sed -i "s/#network.host: 192.168.0.1/network.host: 127.0.0.1/" elasticsearch-7.11.2/config/elasticsearch.yml
sed -i "s/#http.port: 9200/http.port: 9200/" elasticsearch-7.11.2/config/elasticsearch.yml

# 添加用户认证
# https://www.elastic.co/guide/en/elasticsearch/reference/7.11/get-started-enable-security.html

# 启动elasticsearch
elasticsearch-7.11.2/bin/elasticsearch -d


# 检查健康状态
# curl "http://127.0.0.1:9200/_cluster/health?pretty"


### 安装logstash ###
sed -i "s/# pipeline.workers: 2/pipeline.workers: 12/" logstash-7.11.2/config/logstash.yml
sed -i "s/# pipeline.batch.size: 125/pipeline.batch.size: 3000/" logstash-7.11.2/config/logstash.yml
sed -i "s/# pipeline.batch.delay: 50/pipeline.batch.delay: 5/" logstash-7.11.2/config/logstash.yml
sed -i "s/# path.config:/path.config: \/home\/elastic\/logstash-7.11.2\/config\//" logstash-7.11.2/config/logstash.yml
# 修改 jvm.options配置
sed -i "s/-Xms1g/-Xms16g/" logstash-7.11.2/config/jvm.options
sed -i "s/-Xmx1g/-Xmx24g/" logstash-7.11.2/config/jvm.options

# 创建logstash处理数据的自定义配置文件

cat <<EOF > logstash-7.11.2/config/logstash.conf

input{
	file{
		path => "/var/log/secure"
	}
}

output{
	elasticsearch{
		hosts => ["http://127.0.0.1:9200"]
		index => "secure-syslog"
		user => "elastic"
		password => "test123456"
	}
}

EOF
# https://www.elastic.co/guide/en/logstash/current/config-examples.html
# llogstash-7.11.2/bin/logstash -f logstash-7.11.2/config/logstash.conf -t # 测试配置

# 启动logstash
logstash-7.11.2/bin/logstash -f logstash-7.11.2/config/logstash.conf  --config.reload.automatic &



### install Kibana ###
sed -i "s/#server.host: \"localhost\"/server.host: \"localhost\"/" kibana-7.11.2-linux-x86_64/config/kibana.yml # option
sed -i "s/#elasticsearch.hosts: \[\"http:\/\/localhost:9200\"\]/elasticsearch.hosts: \[\"http:\/\/localhost:9200\"\]/" kibana-7.11.2-linux-x86_64/config/kibana.yml # option
sed -i "s/#i18n.locale: \"en\"/i18n.locale: \"zh-CN\"/" kibana-7.11.2-linux-x86_64/config/kibana.yml # option
#elasticsearch.username: "kibana_system"
#elasticsearch.password: "pass"

nohup kibana-7.11.2-linux-x86_64//bin/kibana & 





