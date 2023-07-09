
print("name : Varshini Kaithapuram")
print(f"blazerId : varsh123")



import requests
import json

url = "https://michaelgathara.com/api/python-challenge"

response = requests.get(url)
challenges = response.json()
print("\n Challenge :\n" , challenges, end=" ")

print("\n")

for challenge in challenges:
    ProblemId = challenge['id']
    expr = challenge['problem'].replace('?', '')  
    
    try:
        solution = eval(expr)
        print(f"Solution for Problem {ProblemId} : {expr} = {solution}")
    except ValueError:
        print(f"Problem {ProblemId}'s expression is invalid : {expr}")
        
        