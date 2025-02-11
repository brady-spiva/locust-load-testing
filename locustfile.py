from locust import HttpUser, task, between, events

class TinesUser(HttpUser):
    wait_time = between(1, 3)  # Wait time between tasks
    # host = "https://solitary-star-4892.tines.com"

    def on_start(self):
        """Executed when a simulated user starts."""
        self.client.headers.update({
            'Authorization': 'Bearer <token>',
            'Content-Type': 'application/json'
        })
        self.team_id = ""
        self.story_id = ""

    @task
    def list_teams(self):
        """Retrieve a list of stories."""
        response = self.client.get("/api/v1/teams")
        # parse the first team_id, for use in later calls
        team_id = response.json()
        self.team_id = team_id.get("teams")[0].get("id")

    @task
    def list_stories(self):
        """Retrieve a list of stories."""
        self.client.get("/api/v1/stories")

    @task
    def create_update_delete_story(self):
        """Create, update, and delete a story."""
        # Create a new story, omitting the name to autogenerate
        response = self.client.post("/api/v1/stories", json={
            "description": "Fakedy Fake Fake. Phony. Not Real. Delete This!",
            "team_id": self.team_id
        })
        # print(response.json())
        if response.status_code == 201:
            self.story_id = response.json().get("id")
            # Update the story
            self.client.put(f"/api/v1/stories/{self.story_id}", json={
                "title": "Updated Load Test Story",
                "team_id": self.team_id
            })
            # Delete the story
            self.client.delete(f"/api/v1/stories/{self.story_id}")
    
    def on_stop(self):
        print("Test is ending, running cleanup!")
        # Delete any stories
        self.client.delete(f"/api/v1/stories/{self.story_id}")

