import os
import ftplib

server = os.environ.get('FTP_SERVER')
username = os.environ.get('FTP_USERNAME')
password = os.environ.get('FTP_PASSWORD')

def upload_files():
    print(f"Connecting to {server}...")
    ftp = ftplib.FTP(server, username, password, timeout=30)
    print("Connected successfully!")
    
    try:
        ftp.cwd('/htdocs')
    except Exception as e:
        print("Folder /htdocs not found or error entering directory:", e)

    # Repository එකේ තියෙන upload කළ යුතු files ලැයිස්තුව
    files_to_upload = ['index.html', 'style.css', 'script.js', 'results.json']

    for filename in files_to_upload:
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                print(f"Uploading {filename}...")
                ftp.storbinary(f'STOR {filename}', f)
                print(f"{filename} uploaded successfully!")
        else:
            print(f"File {filename} not found locally, skipping.")

    ftp.quit()
    print("All deployments finished!")

if __name__ == '__main__':
    upload_files()
