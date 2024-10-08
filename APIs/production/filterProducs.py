class MyClass(GeneratedClass):
    def _init_(self):
        GeneratedClass._init_(self)

    def onLoad(self):
        self.tts = ALProxy("ALTextToSpeech")  # Use TTS to speak messages

        # Product database for localization
        self.products_data = [
              {
                "name": "Rice",
                "price": 2.5,
                "ingredients": ["Rice"],
                "allergens": [],
                "location": {"aisle": 7, "section": "Left"}
              },
              {
                "name": "Almond Milk",
                "price": 3.0,
                "ingredients": ["Water", "Almonds"],
                "allergens": ["Nuts"],
                "location": {"aisle": 5, "section": "Right"}
              },
              # Additional product entries...
              {
                "name": "Chickpeas",
                "price": 1.6,
                "ingredients": ["Chickpeas", "Water", "Salt"],
                "allergens": [],
                "location": {"aisle": 8, "section": "Right"}
              }           
        ]

    def onUnload(self):
        # Clean-up code here
        pass

    def onInput_onStart(self, product):
        # Example product received
        product = str(product)
        self.tts.say("Product received from previous box" + product)

        # Fetch location from database
        response = self.find_product_location(product)
        
        self.tts.say(response)

        # Start of execution
        self.onStopped()  # Activate the output of the box

    def onInput_onStop(self):
        self.onUnload()  # Clean-up when the box is stopped
        self.onStopped()  # Activate the output of the box

    def find_product_location(self, product_name):
        # Convert product name to lowercase for case-insensitive matching
        product_name_lower = product_name.lower()

        # Iterate through the products to find a match
        for product in self.products_data:
            if product['name'].lower() == product_name_lower:

                # Retrieve location details
                aisle = product['location']['aisle']
                section = product['location']['section']

                return ("the product " + product_name_lower + " is located in aisle " + str(aisle) + " and in section " + section)
        
        return "Product not found."

    def onInput_input_1(self, p):
        # Receive the product name from input
        product_name = str(p)

        # Find the product location
        result = self.find_product_location(product_name)
        
        # Output the result
        self.tts = ALProxy("ALTextToSpeech")
        self.tts.say(result)
        
        self.onStopped()  # Activate the output of the box