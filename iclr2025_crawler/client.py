import openreview
from typing import List, Dict, Any

class OpenReviewClient:
    def __init__(self, baseurl: str = 'https://api2.openreview.net'):
        # Use the V2 client
        self.client = openreview.api.OpenReviewClient(baseurl=baseurl)

    def get_submissions(self, invitation: str, limit: int = 1000, offset: int = 0) -> List[openreview.api.Note]:
        # V2 client get_all_notes works similarly
        return self.client.get_all_notes(invitation=invitation, details='replyCount')

    def get_notes(self, forum: str) -> List[openreview.api.Note]:
        return self.client.get_notes(forum=forum)
