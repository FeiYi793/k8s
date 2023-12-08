from prometheus_api_client import PrometheusConnect
from kubernetes import client,config

# Prometheus服务器的地址
prometheus_url = 'http://192.168.221.100:30003'

# 创建一个Prometheus连接
prometheus = PrometheusConnect(url=prometheus_url)

# 定义PromQL查询
query = 'irate(container_cpu_usage_seconds_total{namespace="sock-shop", container!="",pod=~"front-end.*"}[1m])'


# 获取指标数据
result = prometheus.custom_query(query=query)
#print("1")
# 打印结果
for data in result:
    #print("Type ",type(data['value'][1]))
    print(float(data['value'][1])*1000)



