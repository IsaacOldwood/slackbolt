"""Mock database."""


class Database:
    def fetch_client_list(self) -> list[str]:
        return [
            "Client 1",
            "A long client name",
            "Test client",
            "PyCon UK 2025",
            "PyCon UK 2024",
        ]

    def fetch_project_list(self) -> list[str]:
        return [
            "Project 1",
            "A long project name",
            "Test project",
            "PyCon UK 2025 project",
            "PyCon UK 2024 project",
        ]

    def grant_user_access(self, client: str, user_id) -> None:
        sp = "EXEC grant_user_access"

        # execute(sp).with_parameters(client=client, user_id=user_id)

    def refresh_client_data(self, client: str) -> None:
        sp = "EXEC refresh_client_data"

        # execute(sp).with_parameters(client)
