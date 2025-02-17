#!/usr/bin/env python3

# multiple inheritance and method resolution order (mro) in python
# this demonstrates how python handles inheritance from multiple parent classes
# and how it resolves method calls when the same method exists in multiple parent classes

class Device:
    def __init__(self, name, connected=False):
        # base class for all devices
        print(f"initializing Device with name: {name}")
        self.name = name
        self.connected = connected
    
    def connect(self):
        # connect the device
        if not self.connected:
            print(f"connecting {self.name}")
            self.connected = True
        return self.connected
    
    def disconnect(self):
        # disconnect the device
        if self.connected:
            print(f"disconnecting {self.name}")
            self.connected = False
        return not self.connected

class AudioDevice:
    def __init__(self, volume=50):
        # base class for audio-capable devices
        print("initializing AudioDevice")
        self.volume = volume
    
    def set_volume(self, volume):
        # set the volume level
        self.volume = max(0, min(100, volume))
        print(f"setting volume to {self.volume}")
    
    def play_audio(self):
        # play audio on the device
        if hasattr(self, 'connected') and not self.connected:
            print("can't play audio: device not connected")
            return False
        print(f"playing audio at volume {self.volume}")
        return True

class DisplayDevice:
    def __init__(self, brightness=70):
        # base class for display-capable devices
        print("initializing DisplayDevice")
        self.brightness = brightness
    
    def set_brightness(self, brightness):
        # set the brightness level
        self.brightness = max(0, min(100, brightness))
        print(f"setting brightness to {self.brightness}")
    
    def display_image(self):
        # display an image on the device
        if hasattr(self, 'connected') and not self.connected:
            print("can't display image: device not connected")
            return False
        print(f"displaying image at brightness {self.brightness}")
        return True

class SmartTV(Device, AudioDevice, DisplayDevice):
    def __init__(self, name):
        # initialize a smart tv with multiple inheritance
        print(f"initializing SmartTV: {name}")
        # call all parent class initializers
        Device.__init__(self, name)
        AudioDevice.__init__(self)
        DisplayDevice.__init__(self)
        # add smart tv specific attributes
        self.channel = 1
    
    def change_channel(self, channel):
        # change the tv channel
        if not self.connected:
            print("can't change channel: tv not connected")
            return False
        self.channel = channel
        print(f"changed to channel {self.channel}")
        return True

class Smartphone(Device, AudioDevice, DisplayDevice):
    def __init__(self, name):
        # initialize a smartphone using super() with multiple inheritance
        print(f"initializing Smartphone: {name}")
        # using super() with multiple inheritance
        super().__init__(name)
        # explicitly call other parent initializers
        AudioDevice.__init__(self)
        DisplayDevice.__init__(self)
        # add smartphone specific attributes
        self.apps = []
    
    def install_app(self, app_name):
        # install an app on the smartphone
        if not self.connected:
            print("can't install app: phone not connected")
            return False
        self.apps.append(app_name)
        print(f"installed app: {app_name}")
        return True

def demonstrate_multiple_inheritance():
    # demonstrate method resolution order (mro)
    print("method resolution order for SmartTV:")
    print(SmartTV.mro())
    
    print("\nmethod resolution order for Smartphone:")
    print(Smartphone.mro())
    
    # create and use a smart tv
    print("\ncreating a smart tv:")
    tv = SmartTV("living room tv")
    
    print("\nusing smart tv features:")
    tv.connect()
    tv.set_volume(75)
    tv.set_brightness(80)
    tv.play_audio()
    tv.display_image()
    tv.change_channel(5)
    
    # create and use a smartphone
    print("\ncreating a smartphone:")
    phone = Smartphone("my phone")
    
    print("\nusing smartphone features:")
    phone.connect()
    phone.set_volume(50)
    phone.set_brightness(60)
    phone.install_app("social media")
    phone.play_audio()
    phone.display_image()

if __name__ == "__main__":
    demonstrate_multiple_inheritance() 