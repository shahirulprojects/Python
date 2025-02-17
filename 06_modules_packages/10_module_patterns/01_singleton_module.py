# singleton module pattern in python
# this pattern ensures only one instance of a module is created

class ConfigurationManager:
    """a singleton class to manage application configuration
    
    this demonstrates the singleton pattern where only one instance
    of the configuration manager exists throughout the application
    """
    _instance = None
    _initialized = False
    
    def __new__(cls):
        # ensures only one instance is created
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # initialize only once
        if not ConfigurationManager._initialized:
            self.settings = {}
            self._load_default_settings()
            ConfigurationManager._initialized = True
    
    def _load_default_settings(self):
        """loads default configuration settings"""
        self.settings = {
            'debug_mode': False,
            'max_connections': 100,
            'timeout': 30,
            'cache_enabled': True
        }
    
    def get_setting(self, key: str, default=None):
        """retrieves a setting value
        
        args:
            key: the setting key to retrieve
            default: value to return if key doesn't exist
        """
        return self.settings.get(key, default)
    
    def update_setting(self, key: str, value):
        """updates a setting
        
        args:
            key: the setting key to update
            value: the new value
        """
        self.settings[key] = value
        print(f"updated setting: {key} = {value}")

# practical usage example
def main():
    # first instance
    config1 = ConfigurationManager()
    print("\nfirst instance settings:")
    print(config1.settings)
    
    # update a setting
    config1.update_setting('debug_mode', True)
    
    # create another instance (will be the same instance)
    config2 = ConfigurationManager()
    print("\nsecond instance settings (same as first):")
    print(config2.settings)
    
    # prove it's the same instance
    print("\nproving singleton pattern:")
    print(f"are instances the same object? {config1 is config2}")
    
    # demonstrate settings retrieval
    print("\nretrieving settings:")
    print(f"debug_mode: {config2.get_setting('debug_mode')}")
    print(f"non-existent setting: {config2.get_setting('invalid_key', 'default_value')}")

if __name__ == "__main__":
    main() 