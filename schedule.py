import requests



def scale_deployment(namespace, deployment_name, replicas):
    # 加载 kubeconfig 文件或者使用集群内部配置
    config.load_kube_config()

    # 创建 Kubernetes API 客户端
    api_instance = client.AppsV1Api()

    # 获取 Deployment 的当前状态
    deployment = api_instance.read_namespaced_deployment(name=deployment_name, namespace=namespace)

    # 更新 Deployment 的副本数
    deployment.spec.replicas = replicas

    # 应用更新
    api_instance.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=deployment)

    print(f"Deployment {deployment_name} in namespace {namespace} scaled to {replicas} replicas.")

def get_container_cpu_usage(api_server, namespace, pod_name, container_name):
    # 构建 Metrics API URL
    metrics_url = f"{api_server}/apis/metrics.k8s.io/v1beta1/namespaces/{namespace}/pods/{pod_name}"

    # 发送 GET 请求获取 Metrics 数据
    response = requests.get(metrics_url)

    if response.status_code == 200:
        # 解析响应数据
        metrics_data = response.json()

        # 找到特定容器的 CPU 使用率
        for container in metrics_data['containers']:
            if container['name'] == container_name:
                cpu_usage = container['usage']['cpu']
                return cpu_usage

        print(f"Container '{container_name}' not found in pod '{pod_name}'.")
        return None
    else:
        print(f"Error fetching metrics. Status code: {response.status_code}")
        return None

# 示例用法
api_server = "http://192.168.221.100:30003"
namespace = "sock-shop"
pod_name = "your-pod-name"
container_name = "your-container-name"

cpu_usage = get_container_cpu_usage(api_server, namespace, pod_name, container_name)

if cpu_usage is not None:
    print(f"CPU usage for container '{container_name}' in pod '{pod_name}': {cpu_usage}")
