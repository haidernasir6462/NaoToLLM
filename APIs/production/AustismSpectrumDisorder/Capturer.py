from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        # Initialize proxies in the constructor
        self.tts = None
        self.photoCaptureProxy = None

    def onLoad(self):
        # Initialization code here
        self.tts = ALProxy("ALTextToSpeech", "127.0.0.1", 9559)
        self.photoCaptureProxy = ALProxy("ALPhotoCapture", "127.0.0.1", 9559)

    def onUnload(self):
        # Clean-up code here
        pass

    def onInput_onStart(self):
        # When this method is triggered, the robot will take a photo and speak
        image_path = self.take_photo_and_speak()

        # Send the image path to the next box
        self.output_image_path(image_path)

        self.onStopped()  # Signal that the box's action has finished

    def onInput_onStop(self):
        self.onUnload()  # It is recommended to reuse the clean-up as the box is stopped
        self.onStopped()  # Activate the output of the box

    def take_photo_and_speak(self):
        try:
            
            time.sleep(2)

            # Set camera parameters
            self.photoCaptureProxy.setResolution(2)  # 2 is 640x480 resolution
            self.photoCaptureProxy.setPictureFormat("jpg")  # Save format in jpg

            # Define the folder and filename
            folder_path = "/home/nao/recordings/cameras/"
            file_name = "photo"

            # Take the photo and save it
            self.photoCaptureProxy.takePicture(folder_path, file_name)

            # The complete path of the saved image
            image_path = folder_path + file_name + ".jpg"

            # Wait for a moment to ensure everything is saved
            time.sleep(1)

            # Robot speaks the path of the saved photo
            # Return the image path
            return image_path

        except Exception as e:
            # Print the error if any occurs
            print("Error while taking photo: ", str(e))
            return None

    def output_image_path(self, image_path):
        if image_path:
            # This method sends the image path to the next connected box
            self.output_1(image_path)