from utils.rag import generate_answer_with_rag

response = generate_answer_with_rag("What is the tire pressure for Tiago?", "tiago_manual")
print(response)