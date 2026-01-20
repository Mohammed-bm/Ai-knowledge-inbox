from utils import fetch_and_clean_url
text = fetch_and_clean_url("https://en.wikipedia.org/wiki/FastAPI")
print(len(text))
print(text[:500])
