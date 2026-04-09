import os
from dotenv import load_dotenv
from packages.rag.service import RagChatService
from pathlib import Path

# Load .env
load_dotenv()

def test_gemini_integration():
    seed_path = Path("data/seed.json")
    # Mock seed file if it doesn't exist or just use it
    if not seed_path.exists():
        print("Seed file not found, creating a dummy one.")
        seed_path.parent.mkdir(parents=True, exist_ok=True)
        with open(seed_path, "w") as f:
            f.write('{"items": [{"id": "1", "role": "freshman_student", "unit": "CAS", "intent": "orientation", "category": "academic", "question": "When is orientation?", "answer": "Orientation is on August 15th."}]}')

    service = RagChatService(seed_path)
    
    question = "When is the orientation?"
    print(f"Question: {question}")
    
    response = service.chat(question)
    print(f"Answer: {response['answer']}")
    print(f"Citations: {response['citations']}")
    
    if "August 15th" in response['answer']:
        print("SUCCESS: Gemini generated a response using the context!")
    else:
        print("FAILURE: Gemini did not use the context or failed.")

if __name__ == "__main__":
    test_gemini_integration()
