from prometheus_api_client import PrometheusConnect
from kubernetes import client,config

config.load_kube_config(config_file="kubeconfig.yaml")
api_instance = client.AppsV1Api()

prometheus_url = 'http://192.168.221.100:30003'

# 创建一个Prometheus连接
prometheus = PrometheusConnect(url=prometheus_url)

def current_cpu_usage():
    query = 'irate(container_cpu_usage_seconds_total{namespace="sock-shop", container!="",pod=~"front-end.*"}[1m])'
    # 获取指标数据
    result = prometheus.custom_query(query=query)
    for data in result:
        if float(data['value'][1])!=0:
            return data['value'][1]

def scale_deployment(namespace, deployment_name, replicas):

    # 获取 Deployment 的当前状态
    deployment = api_instance.read_namespaced_deployment(name=deployment_name, namespace=namespace)
    now_replicas = deployment.spec.replicas
    # 更新 Deployment 的副本数
    deployment.spec.replicas = replicas

    # 应用更新
    api_instance.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=deployment)

    print(f"Deployment {deployment_name} in namespace {namespace} scaled to {replicas} replicas.")


while True:
    try:
        current_cpu_usage = current_cpu_usage()
        cpu_usage = (float(current_cpu_usage) * 1000)/300
        #预测cpu的使用率
        #predicted_cpu_usage = predict_cpu_usage()
        print(cpu_usage)
        if cpu_usage > 0.6:
            scale_deployment('sock-shop','front-end',2)
            print("Scaling up:predicted CPU usage is high.")
        elif cpu_usage < 0.2:
            scale_deployment('sock-shop','front-end',1)
            print("Scaling down: predicted CPU usage is low.")
    except Exception as error:
        print("error")




