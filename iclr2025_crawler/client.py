import openreview
from typing import List, Dict, Any

class OpenReviewClient:
    def __init__(self, baseurl: str = 'https://api.openreview.net'):
        self.client = openreview.Client(baseurl=baseurl)

    def get_submissions(self, invitation: str, limit: int = 1000, offset: int = 0) -> List[openreview.Note]:
        return self.client.get_all_notes(invitation=invitation, details='replyCount')

    def get_notes(self, forum: str) -> List[openreview.Note]:
        return self.client.get_notes(forum=forum)
