import httpx

url = "https://www.facebook.com/marketplace/item/598793553293483/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3A4da1fadb-da6f-4541-8032-3a9071b74616"
response = httpx.get(url)
print(response.text)

# Example: find if a keyword exists
if "2018 Kawasaki z" in response.text:
    print("Keyword found!")
else:
    print("Keyword not found!")
