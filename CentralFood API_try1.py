import requests
def get_recipe(api_key, food_items):
    base_url = 'https://api.nal.usda.gov/fdc/v1/food/search?api_key=dsaRLxRdS5QoBK7YeGc6SLxbEu9G6eH7ryiaztnU}' #paste in link

    params = {
        'api_key': api_key,
        'food_items': ','.join(food_items),
    }

    try:
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            recipe_data = response.json()
            return recipe_data
        elif response.status_code == 403:
            print("API key issue. Check if your API key is valid and authorized.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None


api_key = 'dsaRLxRdS5QoBK7YeGc6SLxbEu9G6eH7ryiaztnU'

# Example food items
food_items = ['chicken', 'broccoli', 'rice']

recipe_data = get_recipe(api_key, food_items)

if recipe_data:
    print("Recipe:")
    print(f"Title: {recipe_data.get('title', 'N/A')}")
    print("Ingredients:")
    for ingredient in recipe_data.get('ingredients', []):
        print(f"- {ingredient}")
    print("Instructions:")
    print(recipe_data.get('instructions', 'N/A'))
else:
    print("Failed to retrieve recipe.")
