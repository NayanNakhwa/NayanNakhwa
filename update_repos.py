import requests
import os
import re

# Configuration
USERNAME = "NayanNakhwa"
# Fetch 5 most recently updated public repos
URL = f"https://api.github.com/users/{USERNAME}/repos?sort=updated&per_page=5&type=public"

def fetch_repos():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching repos: {e}")
        return []

def generate_markdown(repos):
    md_content = ""
    for repo in repos:
        name = repo['name']
        desc = repo['description'] if repo['description'] else "No description provided."
        url = repo['html_url']
        language = repo['language'] if repo['language'] else "Markdown"
        stars = repo['stargazers_count']
        
        # Clean formatting
        md_content += f"- **[{name}]({url})** `({language})`: {desc}\n"
    return md_content

def update_readme(new_content):
    with open("README.md", "r", encoding="utf-8") as file:
        readme = file.read()

    # Regex to find the block between markers
    pattern = r"(<!-- REPO-LIST-START -->)(.*?)(<!-- REPO-LIST-END -->)"
    replacement = f"\\1\n{new_content}\n\\3"
    
    # Replace content
    new_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
    
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(new_readme)

if __name__ == "__main__":
    repos = fetch_repos()
    if repos:
        content = generate_markdown(repos)
        update_readme(content)
        print("README updated successfully.")
    else:
        print("No repositories found.")
