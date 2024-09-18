class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.prompt = ""  # Initialize an empty string for the prompt

    def onLoad(self):
        pass  # Initialization code if needed

    def onUnload(self):
        pass  # Cleanup code if needed

    def onInput_onStart(self):
        # Store a prompt and send it to the next box
        self.prompt = "why is sky blue? give me one line answer"  # Replace with your desired prompt
        self.output_1(self.prompt)  # Send the prompt to the next box through output_1
        self.onStopped(self)  # Notify that the box has finished its task

    def onInput_onStop(self):
        self.onUnload()  # Clean up when stopping
        self.onStopped()