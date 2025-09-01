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
