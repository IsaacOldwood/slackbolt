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

    def refresh_client_data(self, client: str) -> None:
        sp = "EXEC refresh_client_data"

        # execute(sp).with_parameters(client)
