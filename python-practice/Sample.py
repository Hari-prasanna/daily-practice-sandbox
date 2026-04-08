import requests
import json

def fetch_popular_movies(api_key):
    """Fetches the current most popular movies from TMDB."""
    
    # 1. The Base URL
    url = "https://api.themoviedb.org/3/Awards"
    
    # 2. The Parameters (Our specific instructions)
    params = {
        "api_key": api_key,
        "language": "en-US",
        "page": 1
    }
    
    print("Knocking on TMDB's door...")
    
    # 3. Make the GET request
    response = requests.get(url, params=params)
    
    # 4. Check if the door was opened (Status Code 200)
    if response.status_code == 200:
        # Convert the raw text into a Python Dictionary (JSON)
        data = response.json()
        
        # TMDB stores the actual movies inside a list called "results"
        movies = data.get("results", [])
        print(f"✅ Successfully fetched {len(movies)} movies!\n")
        
        # Print the very first movie in the list to inspect the structure
        print("🍿 The #1 Popular Movie Right Now:")
        print(json.dumps(movies[1], indent=4))
        
    else:
        print(f"❌ Failed to fetch data. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # TODO: Paste your real TMDB API Key inside the quotes below
    MY_API_KEY = "b1226c092017b0e621e6833ede71c80d" 
    
    fetch_popular_movies(MY_API_KEY)