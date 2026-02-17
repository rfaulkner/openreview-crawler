import openreview

def research_iclr_2025():
    try:
        client = openreview.Client(baseurl='https://api.openreview.net')
        print("Client initialized successfully.")
        
        # Try to get submissions
        submissions = client.get_all_notes(invitation='ICLR.cc/2025/Conference/-/Submission', details='replyCount')
        print(f"Found {len(submissions)} submissions.")
        
        if submissions:
            first_submission = submissions[0]
            print(f"\nFirst Submission ID: {first_submission.id}")
            print(f"Title: {first_submission.content.get('title', 'N/A')}")
            
            # Try to get reviews for the first submission
            # Usually reviews are replies with a specific invitation or just replies
            reviews = client.get_notes(forum=first_submission.id)
            print(f"Found {len(reviews)} replies/reviews for the first submission.")
            for review in reviews[:3]:
                print(f"Review ID: {review.id}, Invitation: {review.invitation}")
                
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    research_iclr_2025()
