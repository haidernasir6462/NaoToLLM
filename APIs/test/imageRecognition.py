def upload_image_to_imgbb( image_path):
        """Upload the image to ImgBB and return the image URL."""
        url = "https://api.imgbb.com/1/upload"

        try:
            # Open the image file in binary mode
            with open(image_path, 'rb') as image_file:
                # Prepare the payload for the API request
                payload = {
                    'key': self.imgbb_api_key,
                    'image': image_file.read()
                }

                # Make the POST request to ImgBB API
                response = requests.post(url, data=payload)

            # Parse the JSON response
            response_json = response.json()

            if response.status_code == 200:
                # Get the image URL
                image_url = response_json['data']['url']
                return image_url
            else:
                raise Exception("Error uploading image: {}".format(response_json['error']['message']))

        except Exception as e:
            print("Error uploading image to ImgBB: {}".format(e))
            return None
def send_image_to_skybiometry(image_url):
        """Send the image URL to SkyBiometry API and get the response."""
        url = "https://api.skybiometry.com/fc/faces/detect.json"

        params = {
            'api_key': self.api_key,
            'api_secret': self.api_secret,
            'urls': image_url,
            'attributes': 'gender,age,mood,liveness'  # Only requesting these specific attributes
        }

        try:
            # Make the request to SkyBiometry API
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print("Error in SkyBiometry API response: {}".format(response.status_code))
                return None
        except Exception as e:
            print("Error while calling SkyBiometry API: {}".format(e))
            return None

def extract_relevant_data(response):