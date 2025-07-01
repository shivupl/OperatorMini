import json

class TaskContext:
    def __init__(self, goal):
        self.goal = goal
        self.current_url = ""
        self.current_title = ""
        self.step_history = []
        self.last_dom = []
        self.complete = False
    
    def update_state(self, url, title, dom):
        self.current_url = url
        self.current_title = title
        self.last_dom = dom

    def add_step(self, step):
        self.step_history.append(step)

