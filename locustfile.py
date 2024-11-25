from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task(1)  # La probabilidad relativa de ejecutar esta tarea es 1
    def view_page(self):
        self.client.get("/")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]  # Conjunto de tareas que el usuario ejecutará
    wait_time = between(1, 5)  # Tiempo de espera entre tareas, entre 1 y 5 segundos
