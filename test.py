import requests
import time
import json
import pandas as pd # Added this so we can format the final output!

def fetch_movie_batch(api_key, max_pages=5):
    """Loops through multiple pages to build a master list of movies."""
    
    url = "https://api.themoviedb.org/3/discover/movie"
    master_movie_list = []
    
    print(f"Starting extraction for {max_pages} pages...\n")
    
    for page_num in range(1, max_pages + 1):
        params = {
            "api_key": api_key,
            "language": "en-US",
            "primary_release_date.gte": "2025-01-01",
            "primary_release_date.lte": "2026-12-31",
            "sort_by": "popularity.desc",
            "page": page_num 
        }
        
        print(f"Fetching Page {page_num}...")
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            movies_on_page = data.get("results", [])
            master_movie_list.extend(movies_on_page)
            time.sleep(0.2) # Being polite to the server
        else:
            print(f"❌ Failed on page {page_num}. Status code: {response.status_code}")
            break 
            
    print("\n" + "="*40)
    print(f"✅ Extraction Complete!")
    print(f"📦 Total movies collected: {len(master_movie_list)}")
    print("="*40 + "\n")
    
    return master_movie_list



if __name__ == "__main__":
    # Paste your actual TMDB API Key here
    MY_API_KEY = "b1226c092017b0e621e6833ede71c80d" 
    
    # 1. Run the function to get the 100 movies
    my_movies = fetch_movie_batch(MY_API_KEY, max_pages=5)
    
    # 2. Let's look inside the box! Print the FIRST movie in the list perfectly formatted.
    if len(my_movies) > 0:
        print("🍿 Here is the exact JSON structure for ONE movie in our list:")
        print(json.dumps(my_movies[0], indent=4))

pd.set_option('display.max_columns', None) 
movies = pd.DataFrame(my_movies)
print(movies)