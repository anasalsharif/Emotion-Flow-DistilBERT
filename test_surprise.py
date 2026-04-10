import requests

tests = [
  "I am completely shocked by this sudden news!",
  "I can't believe it, this is so unexpected!",
  "What a massive surprise, I am stunned!",
  "This is incredible, I cannot believe my eyes!"
]

for t in tests:
    res = requests.post("http://localhost:8000/predict", json={"text": t}).json()
    print(f"'{t}' => {res['label']} ({res['score']})")
    if 'all_scores' in res:
        print("  Surprise:", res['all_scores'].get('surprise', 0))

