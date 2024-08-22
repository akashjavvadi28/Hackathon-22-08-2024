import random
import datetime
import threading
import logging
from cryptography.fernet import Fernet

# Generate encryption key for votes
key = Fernet.generate_key()
cipher = Fernet(key)

# Configure logging
logging.basicConfig(filename='voting_system.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Voter registration with unique ID generation
def generate_voter_id():
    return str(random.randint(1000, 9999))

voters = {}
candidates = {}
voting_enabled = False
voting_start_time = None
voting_end_time = None

def register_voter():
    name = input("Enter voter's full name: ")
    age = int(input("Enter voter's age: "))
    
    if age < 18:
        print("Registration failed: Voter must be at least 18 years old.")
        return
    
    id_number = input("Enter voter's ID number (e.g., driver's license or passport number): ")
    
    for voter in voters.values():
        if voter['id_number'] == id_number:
            print("Registration failed: ID number already registered.")
            return
    
    voter_id = generate_voter_id()
    voters[voter_id] = {
        'name': name,
        'age': age,
        'id_number': id_number,
        'vote': None,
        'blocked': False
    }
    logging.info(f"Voter {name} registered successfully with Voter ID: {voter_id}")
    print(f"Voter {name} registered successfully with Voter ID: {voter_id}")

def register_candidate():
    name = input("Enter candidate's full name: ")
    age = int(input("Enter candidate's age: "))
    
    if age < 25:  # Assuming the minimum age to stand for election is 25
        print("Nomination failed: Candidate must be at least 25 years old.")
        return
    
    id_number = input("Enter candidate's ID number (e.g., driver's license or passport number): ")
    
    if id_number in candidates:
        print("Nomination failed: ID number already registered.")
        return
    
    candidates[id_number] = {
        'name': name,
        'age': age,
        'votes': 0,
        'blocked': False
    }
    logging.info(f"Candidate {name} has been successfully nominated.")
    print(f"Candidate {name} has been successfully nominated.")

def cast_vote(voter_id):
    global voting_enabled
    
    if not voting_enabled:
        print("Voting is currently disabled or not active!")
        return
    
    if voter_id not in voters:
        print("Invalid Voter ID!")
        return
    
    if voters[voter_id]['blocked']:
        print("You are blocked from voting!")
        return

    if voters[voter_id]['vote'] is not None:
        print("You have already voted!")
        return

    print("Candidates:")
    for idx, (id_number, candidate) in enumerate(candidates.items(), start=1):
        if not candidate['blocked']:
            print(f"{idx}. {candidate['name']}")
    
    choice = int(input("Enter the number of your choice: ")) - 1
    selected_candidate_id = list(candidates.keys())[choice]
    
    # Encrypt the vote
    encrypted_vote = cipher.encrypt(selected_candidate_id.encode())
    voters[voter_id]['vote'] = encrypted_vote
    logging.info(f"Voter {voter_id} cast their vote for candidate {selected_candidate_id}.")
    print("Your vote has been cast successfully!")

def count_votes():
    # Decrypt and count votes
    for voter_id, info in voters.items():
        if info['vote'] is not None:
            decrypted_vote = cipher.decrypt(info['vote']).decode()
            candidates[decrypted_vote]['votes'] += 1
    
    print("\nElection Results:")
    for candidate in candidates.values():
        print(f"{candidate['name']}: {candidate['votes']} votes")

    winner = max(candidates.values(), key=lambda x: x['votes'])
    print(f"\nThe winner is: {winner['name']}")
    logging.info(f"Election winner is: {winner['name']}")

def official_login():
    global voting_start_time, voting_end_time

    official_code = input("Enter the Official Code: ")
    if official_code == "SECURE123":  # Example secure code for officials
        while True:
            print("\n1. Count Votes\n2. Delete Candidate\n3. Block Voter\n4. Block Candidate\n5. Enable/Disable Voting\n6. Schedule Voting\n7. Exit Official Panel")
            choice = input("Enter your choice: ")

            if choice == '1':
                count_votes()

            elif choice == '2':
                id_number = input("Enter the ID number of the candidate to delete: ")
                if id_number in candidates:
                    del candidates[id_number]
                    logging.info(f"Candidate with ID {id_number} has been deleted.")
                    print("Candidate has been deleted.")
                else:
                    print("Candidate not found.")

            elif choice == '3':
                voter_id = input("Enter the Voter ID to block: ")
                if voter_id in voters:
                    voters[voter_id]['blocked'] = True
                    logging.info(f"Voter with ID {voter_id} has been blocked.")
                    print("Voter has been blocked.")
                else:
                    print("Voter not found.")

            elif choice == '4':
                id_number = input("Enter the ID number of the candidate to block: ")
                if id_number in candidates:
                    candidates[id_number]['blocked'] = True
                    logging.info(f"Candidate with ID {id_number} has been blocked.")
                    print("Candidate has been blocked.")
                else:
                    print("Candidate not found.")

            elif choice == '5':
                global voting_enabled
                voting_enabled = not voting_enabled
                status = "enabled" if voting_enabled else "disabled"
                logging.info(f"Voting has been {status}.")
                print(f"Voting has been {status}.")

            elif choice == '6':
                start_time = input("Enter the voting start time (YYYY-MM-DD HH:MM:SS): ")
                end_time = input("Enter the voting end time (YYYY-MM-DD HH:MM:SS): ")
                
                try:
                    voting_start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                    voting_end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                    logging.info(f"Voting scheduled from {voting_start_time} to {voting_end_time}")
                    print(f"Voting scheduled from {voting_start_time} to {voting_end_time}")
                    
                    # Start a thread to handle voting schedule
                    threading.Thread(target=schedule_voting).start()
                    
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD HH:MM:SS")

            elif choice == '7':
                print("Exiting the official panel.")
                break

            else:
                print("Invalid choice! Please try again.")
    else:
        print("Access Denied: Invalid Official Code!")

def schedule_voting():
    while True:
        now = datetime.datetime.now()
        
        if voting_start_time and voting_end_time:
            if now >= voting_start_time and now <= voting_end_time:
                global voting_enabled
                if not voting_enabled:
                    voting_enabled = True
                    print("Voting has been enabled.")
            elif now > voting_end_time:
                if voting_enabled:
                    voting_enabled = False
                    print("Voting has been disabled.")
                    break
        
        # Sleep for a minute before checking again
        threading.Event().wait(60)

# Main program execution
if __name__ == "__main__":
    print("Welcome to the Electronic Voting System!\n")

    while True:
        print("\n1. Register Voter\n2. Nominate Candidate\n3. Cast Vote\n4. Official Login (Admin Panel)\n5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register_voter()

        elif choice == '2':
            register_candidate()

        elif choice == '3':
            voter_id = input("Enter your Voter ID: ")
            cast_vote(voter_id)

        elif choice == '4':
            official_login()

        elif choice == '5':
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice! Please give the correct choice")
