import requests

# Replace with your own API keys
IMGBB_API_KEY = '74e4ae4b51c99547b60866c0bdba460c'
SKYBIOMETRY_API_KEY = 'a3fsh17ltdatvm8k8ibj8b4ubn'
SKYBIOMETRY_API_SECRET = '9g88omeu34bqj1jbjgr7eu7ng0'

def upload_to_imgbb(image_path):
    """Upload image to ImgBB and return the image URL."""
    with open(image_path, 'rb') as image_file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            'key': IMGBB_API_KEY,
        }
        files = {
            'image': image_file,
        }
        response = requests.post(url, data=payload, files=files)
        if response.status_code == 200:
            result = response.json()
            return result['data']['url']
        else:
            raise Exception(f"Failed to upload to ImgBB: {response.text}")

def analyze_image_skybiometry(image_url):
    """Analyze the image URL using SkyBiometry API."""
    url = 'https://api.skybiometry.com/fc/faces/detect.json'
    params = {
        'api_key': SKYBIOMETRY_API_KEY,
        'api_secret': SKYBIOMETRY_API_SECRET,
        'urls': image_url,
        'attributes': 'all',  # This will get emotions, age, gender, etc.
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to analyze image with SkyBiometry: {response.text}")


def extract_relevant_data(response):
    """Extract gender, age_est, mood, and liveness from the response."""
    try:
        # Extract the first face data from the response
        faces = response.get('photos', [])[0].get('tags', [])
        if faces:
            face = faces[0]
            gender = face.get('attributes', {}).get('gender', {}).get('value', 'Unknown')
            age_est = face.get('attributes', {}).get('age_est', {}).get('value', 'Unknown')
            mood = face.get('attributes', {}).get('mood', {}).get('value', 'Unknown')
            liveness = face.get('attributes', {}).get('liveness', {}).get('value', 'Unknown')
            
            # Print the extracted values
            print("Gender: {}".format(gender))
            print("Estimated Age: {}".format(age_est))
            print("Mood: {}".format(mood))
            print("Liveness: {}".format(liveness))
    except Exception as e:
        print("Error extracting relevant data: {}".format(e))


def main(image_path):
    print(image_path)
    try:
        # Step 1: Upload the image to ImgBB
        imgbb_url = upload_to_imgbb(image_path)
        print(f"Image uploaded to ImgBB: {imgbb_url}")
        
        # Step 2: Analyze the image using SkyBiometry
        analysis_result = analyze_image_skybiometry(imgbb_url)
        # print(f"SkyBiometry Analysis Result: {analysis_result}")

        characteristics = extract_relevant_data(analysis_result)
        print(characteristics)
    except Exception as e:
        print(f"Error: {e}")

# Replace 'your_image_path.jpg' with the actual path to your image
image_path = 'C:/Users/Wajahat/Desktop/NaoToLLM/test.png'
main(image_path)