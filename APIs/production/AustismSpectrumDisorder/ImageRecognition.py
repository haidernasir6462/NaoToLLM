import requests
from naoqi import ALProxy

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.image_path = ""
        self.imgbb_api_key = '74e4ae4b51c99547b60866c0bdba460c'
        self.api_key = 'a3fsh17ltdatvm8k8ibj8b4ubn'
        self.api_secret = '9g88omeu34bqj1jbjgr7eu7ng0'

    def onLoad(self):
        # Put initialization code here
        self.tts = ALProxy("ALTextToSpeech")  # Use TTS to speak messages
        pass

    def onUnload(self):
        # Put clean-up code here
        pass

    def onInput_onStart(self):
#        print(str(p))
#        self.tts.say(str(p))
#        image_path = str(p)
#        self.tts.say("I am in on start")
        try:
            # Upload the image and analyze
            image_url = self.upload_to_imgbb("/home/nao/recordings/cameras/photo.jpg")
            print("image url is " + str(image_url))
            if image_url:
                response = self.analyze_image_skybiometry(str(image_url))
                print("i am final data" + str(response))
                if response:
                    self.extract_relevant_data(response)
        except Exception as e:
            print("Error in onInput_onStart:", e)

    def onInput_onStop(self):
        """Stop the process and clean up resources."""
        self.onUnload()  # Reuse clean-up as the box is stopped
        self.onStopped()  # Activate the output of the box

    def upload_to_imgbb(self, image_path):
        try:
            with open(image_path, 'rb') as image_file:
                url = "https://api.imgbb.com/1/upload"
                payload = {
                    'key': self.imgbb_api_key,
                }
                files = {
                    'image': image_file,  # Correct variable name here
                }
                response = requests.post(url, data=payload, files=files)
                result = response.json()
                return result['data']['url']

#                if response.status_code == 200:
#                    result = response.json()
#                    return result['data']['url']
#                else:
#                    raise Exception("Failed to upload to ImgBB: " + response.text)
        except Exception as e:
            print("Error in upload_to_imgbb:" + e)

    def analyze_image_skybiometry(self, image_url):
        """Analyze the image URL using SkyBiometry API."""
        try:
            url = 'https://api.skybiometry.com/fc/faces/detect.json'
            params = {
                'api_key': self.api_key,  # Use self.api_key
                'api_secret': self.api_secret,  # Use self.api_secret
                'urls': image_url,
                'attributes': 'all',  # Get emotions, age, gender, etc.
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception("Failed to analyze image with SkyBiometry: " + response.text)
        except Exception as e:
            print("Error in analyze_image_skybiometry:" + e)

    def extract_relevant_data(self, response):
        try:
            # Confirm the response has the expected structure

            # Safely extract the 'photos' and 'tags' fields
            photos = response.get('photos', [])
            if not photos:
                raise ValueError("No photos found in the response")

            tags = photos[0].get('tags', [])
            if not tags:
                raise ValueError("No tags found for the photo")

            # Extract the first face data from the tags
            face = tags[0]

            # Extract relevant attributes safely
            attributes = face.get('attributes', {})
            gender = attributes.get('gender', {}).get('value', 'Unknown')
            age_est = attributes.get('age_est', {}).get('value', 'Unknown')
            mood = attributes.get('mood', {}).get('value', 'Unknown')
            liveness = attributes.get('liveness', {}).get('value', 'Unknown')

#            self.tts.say("Information extracted successfully")


            # Check if all required attributes are present
            if gender != 'Unknown' and age_est != 'Unknown' and mood != 'Unknown' and liveness != 'Unknown':
                # Create the final attributes string
                attributes_str = (
                    "the gender is " + str(gender) + ", estimated age is " + str(age_est) + ", the mood is " + str(mood) +               ", and the liveliness is " + str(liveness) + "."
                )

                print(attributes_str)
                self.output_1(attributes_str)
            else:
                # Handle the case where some attributes are missing
                self.tts.say("Missing some attributes in the picture.")
                print("Missing attributes in the picture: Gender: {}, Age: {}, Mood: {}, Liveness: {}".format(
                    gender, age_est, mood, liveness
                ))
                self.output_1("None")

        except Exception as e:
            # Catch and log any errors
            error_message = "Error extracting relevant data: " + str(e)
            print(error_message)
            self.tts.say(error_message)


    def onInput_onStop(self):
        """Stop the process and clean up resources."""
        self.onUnload()  # Reuse clean-up as the box is stopped
        self.onStopped()  # Activate the output of the box