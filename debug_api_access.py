import openreview

def debug_api():
    client = openreview.Client(baseurl='https://api.openreview.net')
    
    print("--- Searching for Invitations ---")
    # List invitations matching the conference pattern
    invitations = client.get_invitations(regex='ICLR.cc/2025/Conference/.*')
    
    submission_invitations = [i.id for i in invitations if 'Submission' in i.id]
    review_invitations = [i.id for i in invitations if 'Review' in i.id]
    decision_invitations = [i.id for i in invitations if 'Decision' in i.id]
    
    print(f"Found {len(submission_invitations)} Submission-related invitations:")
    for inv in submission_invitations[:10]:
        print(f"  - {inv}")

    print(f"\nFound {len(review_invitations)} Review-related invitations:")
    for inv in review_invitations[:10]:
        print(f"  - {inv}")

    print(f"\nFound {len(decision_invitations)} Decision-related invitations:")
    for inv in decision_invitations[:10]:
        print(f"  - {inv}")

    # Try to fetch one note from a likely submission invitation
    potential_submission_ids = [
        'ICLR.cc/2025/Conference/-/Submission',
        'ICLR.cc/2025/Conference/-/Blind_Submission'
    ]
    
    print("\n--- Testing Submission Fetching ---")
    for inv_id in potential_submission_ids:
        print(f"Trying to fetch from: {inv_id}")
        try:
            notes = client.get_all_notes(invitation=inv_id, limit=1)
            if notes:
                note = notes[0]
                print(f"  -> SUCCESS! Found {len(notes)} note(s). ID: {note.id}")
                print(f"  -> Object dir: {dir(note)}")
                # Check for invitations attribute (V2)
                if hasattr(note, 'invitations'):
                    print(f"  -> note.invitations: {note.invitations}")
                elif hasattr(note, 'invitation'):
                    print(f"  -> note.invitation: {note.invitation}")
                else:
                    print("  -> Neither 'invitation' nor 'invitations' attribute found directly.")
            else:
                print("  -> No notes found.")
        except Exception as e:
            print(f"  -> Error: {e}")

if __name__ == "__main__":
    debug_api()
