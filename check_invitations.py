import openreview

def check_invitations():
    try:
        client = openreview.Client(baseurl='https://api.openreview.net')
        # Get one submission
        submissions = client.get_all_notes(invitation='ICLR.cc/2025/Conference/-/Submission', limit=1, details='directReplies')
        if not submissions:
            print("No submissions found.")
            return

        submission = submissions[0]
        print(f"Submission ID: {submission.id}")
        
        # Check direct replies to see if decision is there
        print("\nDirect Replies Invitations:")
        for reply in submission.details['directReplies']:
            print(f"- {reply['invitation']}")
            if 'Decision' in reply['invitation']:
                print(f"  -> FOUND DECISION NOTE! Content: {reply['content']}")

        # Also search for invitations matching the submission
        print("\nSearching for invitations related to this submission...")
        invitations = client.get_invitations(regex='ICLR.cc/2025/Conference/.*')
        for inv in invitations[:20]:
            if 'Decision' in inv.id:
                print(f"Possible Decision Invitation: {inv.id}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_invitations()
