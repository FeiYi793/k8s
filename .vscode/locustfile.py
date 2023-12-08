import time
from locust import HttpUser, task, between

# 这里为所有虚拟用户定义了一个继承自HttpUser的类，每个虚拟用户都提供了一个client属性
# 该属性是HttpSession的实例，可以用于向我们需要测试的目标发起http请求
class QuickStartUser(HttpUser):
    wait_time = between(1, 5)  # 模拟用户在每个任务执行后等待1-5秒

    @task  # task 任务，对于每个正在运行的用户，locust都会创建一个greenlet（协程）
    def hello_world(self):  
        self.client.get("/hello")
        self.client.get("/world")

    @task(3)  # 这是第二个task，后面的3表示权重，运行QuickStartUser时，会从多个task任务中随机选择一个，权重增加了他的选择几率
    def view_items(self):
        for item_id in range(10):
            self.client.get(f"/item?id={item_id}", name="/item")  # 统计信息是按照URL来分组，这里是为了将这些链接都归于item组内
            time.sleep(1)

    def on_start(self):  # 每个用户启动都会调用此方法 on_stop则是每个用户停止时运行
        self.client.post("/login", json={"username": "root", "password": "root"})
