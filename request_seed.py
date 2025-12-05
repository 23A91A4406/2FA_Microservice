# Step 1: Import libraries
# 'requests' is used to make HTTP requests to the API
import requests
import json

# Step 2: Read your student public key
# Open the file 'student_public.pem' and read its content
with open("student_public.pem", "r") as f:
    public_key = f.read()

# Step 3: Prepare the data to send to the instructor API
payload = {
    "student_id": "23A91A4406",  # <-- Replace with your actual student ID
    "github_repo_url": "https://github.com/23A91A4406/2FA_Microservice.git",  # <-- Replace with your repo URL
    "public_key": public_key  # This is the content of your student public key
}

# Step 4: Make the POST request to the instructor API
# timeout=10 ensures it won't wait forever if server is slow
response = requests.post(
    "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/",  # API endpoint
    headers={"Content-Type": "application/json"},  # Tell server we're sending JSON
    data=json.dumps(payload),  # Convert Python dictionary to JSON string
    timeout=10
)

# Step 5: Extract the encrypted seed from the response
data = response.json()  # Convert JSON response to Python dictionary
encrypted_seed = data.get("encrypted_seed")  # Get the encrypted_seed value

# Step 6: Save the encrypted seed to a file
# This file should NOT be committed to GitHub
with open("encrypted_seed.txt", "w") as f:
    f.write(encrypted_seed)

# Step 7: Print confirmation
print("Encrypted seed saved to encrypted_seed.txt")