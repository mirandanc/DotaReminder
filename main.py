import requests
import time

class DotaGSIClient:
    def __init__(self, host='localhost', port=3030):
        self.base_url = f'http://{host}:{port}'
    
    def get_clock_time(self):
        try:
            response = requests.get(f'{self.base_url}/gsi')
            
            if response.status_code == 200:
                data = response.json()
                clock_time = data.get('map', {}).get('clock_time', 0)
                return clock_time
            else:
                print(f"Error: HTTP {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to GSI server: {e}")
            return None

def main():
    gsi_client = DotaGSIClient()
    
    print("Starting Dota 2 GSI Clock Monitor...")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            clock_time = gsi_client.get_clock_time()
            
            if clock_time is not None:
                print(f"Current game clock time: {clock_time}")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        input("\nPress Enter to close...")

if __name__ == "__main__":
    main()