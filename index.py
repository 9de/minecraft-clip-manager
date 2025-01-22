import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import requests
from pathlib import Path
import base64
import subprocess
from moviepy.editor import VideoFileClip

class VideoHandler(FileSystemEventHandler):
    def __init__(self, watch_paths, destination_path, streamable_email, streamable_password):
        self.watch_paths = watch_paths if isinstance(watch_paths, list) else [watch_paths]
        self.destination_path = destination_path
        self.processed_files = set()
        self.streamable_email = streamable_email
        self.streamable_password = streamable_password
        
    def get_streamable_auth(self):
        credentials = f"{self.streamable_email}:{self.streamable_password}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        return {
            'Authorization': f'Basic {encoded_credentials}',
            'User-Agent': 'Mozilla/5.0'
        }

    def quick_trim_and_DESTINATION(self, file_path):
        try:
            with VideoFileClip(file_path) as video:
                duration = video.duration
                # Get last 15 seconds
                start_time = max(0, duration - 15)
                trimmed = video.subclip(start_time, duration)
                
                # Get original name and create output name
                original_name = os.path.basename(file_path)
                name_without_ext = os.path.splitext(original_name)[0]
                file_ext = os.path.splitext(original_name)[1]
                
                # Ask for custom name
                print(f"Original video name: {original_name}")
                custom_name = input("Enter name for the trimmed video (press Enter to use original name): ").strip()
                
                # Create the output name based on user input
                if custom_name:
                    custom_name = custom_name.replace("Username: ","")
                    if not custom_name.lower().endswith('.mp4'):
                        output_name = f"{custom_name}+cuttedauto.mp4"
                    else:
                        output_name = custom_name.replace('.mp4', '+cuttedauto.mp4')
                else:
                    output_name = f"{name_without_ext}+cuttedauto{file_ext}"
                
                # Ensure DESTINATION folder exists
                if not os.path.exists(self.destination_path):
                    os.makedirs(self.destination_path)
                
                # Save trimmed video directly to DESTINATION folder
                temp_path = os.path.join(self.destination_path, output_name)
                print("Trimming last 15 seconds of video...")
                trimmed.write_videofile(temp_path, codec='libx264')
                print(f"Clip saved to DESTINATION folder")
        except Exception as e:
            print(f"Error in quick trim and upload: {e}")
            return None
    def quick_trim_and_upload(self, file_path):
        try:
            with VideoFileClip(file_path) as video:
                duration = video.duration
                # Get last 15 seconds
                start_time = max(0, duration - 15)
                trimmed = video.subclip(start_time, duration)
                
                # Get original name and create output name
                original_name = os.path.basename(file_path)
                name_without_ext = os.path.splitext(original_name)[0]
                file_ext = os.path.splitext(original_name)[1]
                
                # Ask for custom name
                print(f"Original video name: {original_name}")
                custom_name = input("Enter name for the trimmed video (press Enter to use original name): ").strip()
                
                # Create the output name based on user input
                if custom_name:
                    custom_name = custom_name.replace("Username: ","")
                    if not custom_name.lower().endswith('.mp4'):
                        output_name = f"{custom_name}+cuttedauto.mp4"
                    else:
                        output_name = custom_name.replace('.mp4', '+cuttedauto.mp4')
                else:
                    output_name = f"{name_without_ext}+cuttedauto{file_ext}"
                
                # Ensure DESTINATION folder exists
                if not os.path.exists(self.destination_path):
                    os.makedirs(self.destination_path)
                
                # Save trimmed video directly to DESTINATION folder
                temp_path = os.path.join(self.destination_path, output_name)
                print("Trimming last 15 seconds of video...")
                trimmed.write_videofile(temp_path, codec='libx264')
                print(f"Clip saved to DESTINATION folder")
                
                # Upload to Streamable
                print("Uploading to Streamable...")
                upload_url = "https://api.streamable.com/upload"
                with open(temp_path, 'rb') as f:
                    files = {'file': (os.path.basename(temp_path), f, 'video/mp4')}
                    response = requests.post(
                        upload_url,
                        files=files,
                        auth=(self.streamable_email, self.streamable_password),
                        headers={'User-Agent': 'Mozilla/5.0'}
                    )
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'shortcode' in data:
                            return data['shortcode']
                        else:
                            print(f"No shortcode in response. Response data: {data}")
                            return None
                    except ValueError as e:
                        print(f"Failed to parse JSON response: {response.text}")
                        return None
                else:
                    print(f"Upload failed. Status code: {response.status_code}")
                    print(f"Response: {response.text}")
                    return None
                    
        except Exception as e:
            print(f"Error in quick trim and upload: {e}")
            return None

    def trim_video(self, file_path):
        try:
            with VideoFileClip(file_path) as video:
                duration = video.duration
                print(f"\nVideo duration: {duration:.2f} seconds")
                
                # Get original name without extension
                original_name = os.path.basename(file_path)
                name_without_ext = os.path.splitext(original_name)[0]
                file_ext = os.path.splitext(original_name)[1]
                
                print(f"Current video name: {original_name}")
                custom_name = input("Enter name for the trimmed video (press Enter to keep current name): ").strip()
                if not custom_name:
                    output_name = f"{name_without_ext}_cutted_auto{file_ext}"
                else:
                    output_name = f"{custom_name}_cutted_auto{file_ext}"
                
                while True:
                    print("\nTrim options:")
                    print("1 - Keep last N seconds")
                    print("2 - Custom trim (start and end time)")
                    print("3 - Upload without trimming")
                    choice = input("Enter your choice: ")

                    if choice == "1":
                        try:
                            seconds = float(input("Enter number of seconds to keep from the end: "))
                            if seconds > duration:
                                print("Error: Trim duration longer than video duration")
                                continue
                            
                            start_time = max(0, duration - seconds)
                            trimmed = video.subclip(start_time, duration)
                            
                            temp_path = os.path.join(os.path.dirname(file_path), output_name)
                            print("Trimming video...")
                            trimmed.write_videofile(temp_path, codec='libx264')
                            return temp_path
                            
                        except ValueError:
                            print("Please enter a valid number of seconds")
                            continue

                    elif choice == "2":
                        try:
                            print(f"\nVideo duration is {duration:.2f} seconds")
                            start = float(input("Enter start time (in seconds): "))
                            end = float(input("Enter end time (in seconds): "))
                            
                            if start < 0 or end > duration or start >= end:
                                print("Invalid time range")
                                continue
                            
                            trimmed = video.subclip(start, end)
                            temp_path = os.path.join(os.path.dirname(file_path), "temp_trimmed.mp4")
                            print("Trimming video...")
                            trimmed.write_videofile(temp_path, codec='libx264')
                            return temp_path
                            
                        except ValueError:
                            print("Please enter valid numbers for start and end times")
                            continue

                    elif choice == "3":
                        return file_path

                    else:
                        print("Invalid choice")
                        continue

        except Exception as e:
            print(f"Error trimming video: {e}")
            return file_path

    def upload_to_streamable(self, file_path):
        try:
            # First, handle trimming
            print("\nWould you like to trim the video before uploading?")
            if input("Enter 'y' for yes, any other key for no: ").lower() == 'y':
                trimmed_path = self.trim_video(file_path)
                if trimmed_path != file_path:
                    upload_path = trimmed_path
                    print("Using trimmed video for upload...")
                else:
                    upload_path = file_path
                    print("Using original video for upload...")
            else:
                upload_path = file_path

            # Now upload the file
            print("Uploading to Streamable...")
            upload_url = "https://api.streamable.com/upload"
            with open(upload_path, 'rb') as f:
                files = {'file': (os.path.basename(upload_path), f, 'video/mp4')}
                response = requests.post(
                    upload_url,
                    files=files,
                    auth=(self.streamable_email, self.streamable_password),
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
            
            # Clean up temporary file if it exists
            if upload_path != file_path:
                try:
                    os.remove(upload_path)
                except Exception as e:
                    print(f"Warning: Could not remove temporary file: {e}")
                
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'shortcode' in data:
                        return data['shortcode']
                    else:
                        print(f"No shortcode in response. Response data: {data}")
                        return None
                except ValueError as e:
                    print(f"Failed to parse JSON response: {response.text}")
                    return None
            else:
                print(f"Upload failed. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Network error during upload: {e}")
            return None
        except Exception as e:
            print(f"Error uploading to Streamable: {e}")
            return None

    def open_folder_in_explorer(self, path):
        try:
            subprocess.Popen(f'explorer "{path}"')
            print(f"Opened folder: {path}")
        except Exception as e:
            print(f"Error opening folder: {e}")

    def show_menu(self):
        print("\nChoose an action:")
        print("0 - Quick Clip last 15s to folder")
        print("1 - Save clip with new name")
        print("2 - Save clip to DESTINATION folder")
        print("3 - Share clip on Streamable (with trim options)")
        print("4 - Quick upload last 15s to Streamable")
        print("5 - Skip this clip")
        print("6 - Open folders")
        print("7 - Play video")
        print("9909 - Remove clip")
        return input("Enter your choice: ")

    def handle_new_video(self, file_path):
        if file_path in self.processed_files:
            return
        
        print(f"\nNew video detected: {file_path}")
        
        while True:
            choice = self.show_menu()
            
            try:
                if choice == "0":
                    shortcode = self.quick_trim_and_DESTINATION(file_path)
                elif choice == "1":
                    while True:
                        new_name = input("Enter new filename: ")
                        if not new_name.lower().endswith('.mp4'):
                            new_name += '.mp4'
                        new_path = os.path.join(os.path.dirname(file_path), new_name)
                        try:
                            os.rename(file_path, new_path)
                            print(f"File renamed to: {new_name}")
                            file_path = new_path
                            break
                        except Exception as e:
                            print(f"Error renaming file: {e}")
                            if input("Would you like to try renaming again? (y/n): ").lower() != 'y':
                                break
                    
                elif choice == "2":
                    if not os.path.exists(self.destination_path):
                        os.makedirs(self.destination_path)
                    new_path = os.path.join(self.destination_path, os.path.basename(file_path))
                    shutil.move(file_path, new_path)
                    print(f"Clip saved to DESTINATION folder")
                    file_path = new_path
                    
                elif choice == "3":
                    shortcode = self.upload_to_streamable(file_path)
                    if shortcode:
                        print(f"Upload successful! Video available at: https://streamable.com/{shortcode}")
                    else:
                        print("Upload failed.")

                elif choice == "4":
                    # Quick upload last 15s to Streamable
                    shortcode = self.quick_trim_and_upload(file_path)
                    if shortcode:
                        print(f"Upload successful! Video available at: https://streamable.com/{shortcode}")
                    else:
                        print("Upload failed.")
                    
                elif choice == "5":
                    print("Skipped clip.")
                    break
                    
                elif choice == "6":
                    print("\nWhich folder would you like to open?")
                    print("0 - DESTINATION destination folder")
                    for i, path in enumerate(self.watch_paths, 1):
                        print(f"{i} - {path}")
                    
                    folder_choice = input(f"Enter your choice (0-{len(self.watch_paths)}): ")
                    
                    try:
                        choice_num = int(folder_choice)
                        if choice_num == 0:
                            self.open_folder_in_explorer(self.destination_path)
                        elif 1 <= choice_num <= len(self.watch_paths):
                            self.open_folder_in_explorer(self.watch_paths[choice_num - 1])
                        else:
                            print("Invalid choice.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                    continue
                    
                elif choice == "7":
                    if os.path.exists(file_path):
                        try:
                            os.startfile(file_path)
                            print("Opening video in default player...")
                        except Exception as e:
                            print(f"Error playing video: {e}")
                    else:
                        print("Cannot find the video file.")
                    
                elif choice == "9909":
                    os.remove(file_path)
                    print("Clip removed.")
                    self.processed_files.add(file_path)
                    break
                    
                else:
                    print("Invalid choice. Please try again.")
                    continue
                
                if choice == "4":
                    self.processed_files.add(file_path)
                    break
                    
                if choice != "5":
                    self.processed_files.add(file_path)
                    
            except Exception as e:
                print(f"Error processing file: {e}")
                if input("\nWould you like to try again? (y/n): ").lower() != 'y':
                    break

    def on_created(self, event):
        if not event.is_directory:
            file_ext = Path(event.src_path).suffix.lower()
            if file_ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv']:
                self.handle_new_video(event.src_path)

def start_watchdog(watch_paths, destination_path, streamable_email, streamable_password):
    if isinstance(watch_paths, str):
        watch_paths = [watch_paths]
    
    event_handler = VideoHandler(watch_paths, destination_path, streamable_email, streamable_password)
    observers = []
    
    for path in watch_paths:
        if os.path.exists(path):
            observer = Observer()
            observer.schedule(event_handler, path, recursive=False)
            observer.start()
            observers.append(observer)
            print(f"Started watching directory: {path}")
        else:
            print(f"Warning: Directory does not exist: {path}")
    
    if not observers:
        print("No valid directories to watch. Exiting...")
        return
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()
        print("\nWatchdog stopped.")
    
    for observer in observers:
        observer.join()

if __name__ == "__main__":
    # List of paths to watch
    WATCH_PATHS = [
        r"C:\Users\Tareq\Videos\Minecraft",
    ]
    DESTINATION_PATH = r"PATH HERE"
    
    # Streamable credentials
    STREAMABLE_EMAIL = "EMAIL_HERE"
    STREAMABLE_PASSWORD = "PASSWORD_HERE"
    
    print("\nStarting watchdog for multiple directories:")
    for path in WATCH_PATHS:
        print(f"- {path}")
    print("\nPress Ctrl+C to stop the watchdog")
    
    start_watchdog(WATCH_PATHS, DESTINATION_PATH, STREAMABLE_EMAIL, STREAMABLE_PASSWORD)
