import requests
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from integrations.graph_api import Microsoft

class OneDrive(Microsoft):
    
    def __init__(self):
        super(OneDrive, self).__init__()
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        
    def upload(self, file="./database/test.db") -> None:
        # Endpoint to upload the file
        endpoint = self._GRAPH_API_ENDPOINT + f"/me/drive/items/root:/{os.path.basename(file)}:/content"
        
        # Initialize variable to hold the binary byte strings of the file
        data: None or bytes
        
        # Read the data in the file to the data variable
        with open(file, "rb") as upload:
            data = upload.read()
        
        # Make a PUT request to upload the file
        request: requests.Response = requests.put(endpoint, headers=self.headers, data=data)
        
        # Get the response
        response = request.json()
        
        # Save the file id in a text file so it can be saved in the database after the thread has finished
        # This file is nested two layers deep which pyinstaller can't bundle if you import a module from the main directory
        # returning a value from a thread is too complicated to this is the best solution
        with open("id.txt", "w") as file:
            file.write(response['id'])
        
        # Return the file id to the onedrive worker to save in the database
        return response['id']

    def download(self, file_id):
        
        # file_id = "2EFAE4DC031AAE4E!18648"
        endpoint = self._GRAPH_API_ENDPOINT + f"/me/drive/items/{file_id}/content"
        
        response_file: requests.Response = requests.get(endpoint, headers=self.headers)
        
        if response_file.status_code == 200:
            with open("test.db", "wb") as file:
                file.write(response_file.content)
            return self.get_file_name(file_id)
        else:
            print("response file get request failed")
            print(response_file.status_code)
            # print(response_file.headers)
            return None
            
    def get_file_name(self, file_id) -> str:
 
        file_name_request = requests.get(
            self._GRAPH_API_ENDPOINT + f"/me/drive/items/{file_id}",
            headers=self.headers,
            params={'select': 'name'}
        )
        file_name = file_name_request.json().get('name')
        
        return file_name
            
           
# onedrive = OneDrive()
# onedrive.upload()
# onedrive.download()
        
        
    