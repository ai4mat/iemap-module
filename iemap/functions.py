from pathlib import Path
from io import open
import time
from functools import wraps
from requests_toolbelt import MultipartEncoder
from requests.exceptions import ConnectionError
import requests
from os.path import dirname
from os import getcwd
import mimetypes
import json
from bson import ObjectId
from iemap.helpers import get_file_size, endpoints
from iemap.models import newProject





class IEMAP:
    # additional MIME_types
    mimetypes.types_map[".dat"] = "application/octet-stream"
    mimetypes.types_map[".out"] = "text/plain"
    mimetypes.types_map[".in"] = "text/plain"
    mimetypes.types_map[".cif"] = "text/plain"  # "chemical/x-cif"  #

    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        self.__payload = {"username": self.user, "password": self.pwd}
        self.__token = None
        self.__id = None
        self.metadata = None
        self.project_file = []
        self.property_file = None

    def check_metadata(self):
        try:
            newProject(**self.metadata)
            return False
        except Exception as e:
            print("The metadata provided does note have a valid schema.")
            print("Please check the error details below:\n", e)
            return True

    def get_path_file(self, file_path):
        if "~" in file_path:
            file_abspath = Path(file_path).expanduser()
        else:
            file_abspath = Path(getcwd()) / file_path
        return file_abspath

    def get_id(self):
        if self.__id == None:
            print(
                "No project id was yet set. Please provide one using `set_id` or `save` a new project!"
            )
        else:
            print(f"Current project id is {self.__id}")

    def set_id(self, id):
        if ObjectId.is_valid(id):
            self.__id = id
            print(f"Updated current project id to {self.__id}!!")
        else:
            print(
                f"{id} is not a valid project id!! unable to update, current project id is {self.__id}"
            )

    def get_token(self):
        try:
            response = requests.post(
                endpoints.get_token.value,
                data=self.__payload,
                # verify=False
            )
            if response.status_code == 200:
                token = json.loads(response.text).get("access_token")
                self.__token = token

            else:
                print(
                    f"An error occured!! Server response status code :{response.status_code}"
                )
                return False
        except ConnectionError as e:
            print("Unable to connect to server. Check your connectivity and try again.")
            return False
        return True

    def login(self):
        if self.__token != None:
            print("User already logged in!")
        else:
            try:
                response = requests.post(
                    endpoints.get_token.value,
                    data=self.__payload,
                    # verify=False
                )
                if response.status_code == 200:
                    token = json.loads(response.text).get("access_token")
                    self.__token = token
                    print("User successfully logged in!")
                else:
                    return f"An error occured!! Server response status code :{response.status_code}"
            except ConnectionError as e:
                print(
                    "Can't Login, unable to connect to server! Check your connectivity and try again."
                )

    def show_token(self):
        print("Current token value is:\n" + self.__token)

    def _load_metadata(self, file_path):
        json.load(file_path)

    def timeit(func):
        @wraps(func)
        def timeit_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            msg = f"Operation {func.__name__}"
            if func.__name__ == "save":
                msg = "Saving metadata (and files)"
            if func.__name__ == "save_project_files":
                msg = "Saving project file"
            if func.__name__ == "download_file":
                msg = "Download"
            if result != None:
                print(
                    f"{msg} took {total_time:.4f} seconds"
                    # f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds"
                )
            return result

        return timeit_wrapper

    def save(self, metadata, list_proj_files=[], show_debug_info=False):
        if type(metadata) == dict:
            self.metadata = metadata
        elif self.get_path_file(metadata).is_file():
            with open(self.get_path_file(metadata), "r", encoding="utf-8") as f:
                metadata_from_file = f.read()
            self.metadata = json.loads(metadata_from_file)
        else:
            print("Unable to read metadata!! Check the path of the provided file.")
            print("Provided file path file is ", metadata)
            print("Current working directory is: ", getcwd())
            print("Current file path is:    ", __file__)
            return
        # if metadata does not hav a valid schema then exit method
        if self.check_metadata():
            return
        isAuthenticated = False
        if self.__token == None:
            isAuthenticated = self.get_token()
            if not isAuthenticated:
                return
        try:
            response = requests.post(
                endpoints.post_metadata.value,
                json=self.metadata,
                headers={"Authorization": f"Bearer {self.__token}"},
            )
            if response.status_code == 200:
                self.__id = json.loads(response.text).get("inserted_id")
                print(f"Document correctly inserted with ObjectID = {self.__id}")
                if list_proj_files != []:
                    self.save_project_files(list_proj_files)
            else:
                print(
                    f"Unable to save data on DB!! Server response status code :{response.status_code}"
                )
                if show_debug_info:
                    print(response.text)
        except Exception as e:
            print("An error occurred! ", e)

    def upload_file(
        self,
        file_to_upload,
        file_name,
        mtype,
        endpoint,
        file_size=None,
        file_unit=None,
        show_debug_info=False,
    ):
        m = MultipartEncoder(fields={"file": (file_name, file_to_upload, mtype)})
        msg = (
            f"Adding file {file_name}"
            if (file_size is None) and (file_unit is None)
            else f"Adding file {file_name} ({round(file_size,2)}{file_unit})"
        )
        print(msg, end="...")
        if self.__token == None:
            self.get_token()
        # endpoint to save data use query parameters (project_id obtained after saving metadata)
        # ep = endpoints.post_project_file.value + "?project_id=" + str(self.__id)
        try:
            response_f = requests.post(
                endpoint,
                data=m,
                headers={
                    "Content-Type": m.content_type,
                    "Authorization": f"Bearer {self.__token}",
                },
            )
            if response_f.status_code == 200:
                if json.loads(response_f.text)["uploaded"]:
                    print(f"Done!")
                else:
                    print(f"Done! (File already present on File System)")
            else:
                print(f"Error! ...file not saved.")
                if show_debug_info:
                    print(response_f.text)
            return True
        except ConnectionError as e:
            print(
                f"Error while uploading file {file_name}! unable to connect to server."
            )
        except Exception as e:
            print(f"Error while uploading file {file_name}! Error:\n", e)

    @timeit
    def save_project_files(self, project_files, show_debug_info=False):
        if self.__id == None:
            print(
                """No project id is currently set. Unable to save files!
Please Provide a valid id (e.g. using `set_id`)"""
            )
            return
        for f in project_files:
            file_abspath = self.get_path_file(f)
            if file_abspath.is_file() == True:
                # open file as stream
                file_to_upload = open(file_abspath, "rb")
                # retrieve mime type from file
                mtype, encoding = mimetypes.guess_type(file_abspath)
                file_name = file_abspath.name
                size, unit = get_file_size(file_abspath)
                ep = endpoints.post_project_file.value + "?project_id=" + str(self.__id)
                self.upload_file(
                    file_to_upload, file_name, mtype, ep, size, unit, show_debug_info
                )
            else:
                print(f"{f} IS NOT A VALID PATH FILE!")
        return True

    def save_property_files(self, props_files, show_debug_info=False):
        if self.__id == None:
            print(
                "No project id is currently set. Unable to save files!\nPlease Provide a valid id (e.g. using `set_id`)"
            )
            return
        for prop, file in props_files.items():
            file_abspath= self.get_path_file(file)

            mtype, encoding = mimetypes.guess_type(Path(file))

            # multiencoder to upload files (one at time)
            if file_abspath.is_file() == True:
                # open file as stream
                file_to_upload = open(file_abspath, "rb")
                # retrieve mime type from file
                mtype, encoding = mimetypes.guess_type(file_abspath)
                file_name = file_abspath.name
                size, unit = get_file_size(file_abspath)
                ep = (
                    endpoints.post_property_file.value
                    + "?project_id="
                    + str(self.__id)
                    + "&name="
                    + str(prop)
                )
                self.upload_file(
                    file_to_upload, file_name, mtype, ep, size, unit, show_debug_info
                )
            else:
                print(f"{file} IS NOT A VALID PATH FILE!")

    def query(self, doc_id):
        ep = endpoints.get_query_db.value + "?id=" + str(doc_id)
        # "?iemap_id=" + str(iemap_id) e.g ?iemap_id=iemap-6EB98D
        try:
            response = requests.get(
                ep,
                # verify=False
                # headers={"Authorization": f"Bearer {self.__token}"},
            )
            if response.status_code == 200:
                docs = json.loads(response.text)
                return docs
            else:
                print(f"Unable to find a document with iemap_id={doc_id} on DB!!")
        except ConnectionError as e:
            print("Error while querying DataBase! Unable to contact server!")
        except Exception as e:
            print("Error while querying DataBase!\nError: ", e)

    def my_projects(self):
        if self.__token == None:
            self.get_token()
        try:
            ep = endpoints.get_user_projects_info.value
            response = requests.get(
                ep,
                headers={"Authorization": f"Bearer {self.__token}"},
            )
            if response.status_code == 200:
                docs = json.loads(response.content)
                return docs
            else:
                print(f"An error occurred!")
        except ConnectionError as e:
            print(
                "Error while trying to get list user's projects! Unable to contact server!"
            )
        except Exception as e:
            print("Error while trying to get list user's projects!\nError: ", e)

    @timeit
    def download_file(self, hash_file, local_file_name=None):
        if self.__token == None:
            self.get_token()
        ep = endpoints.get_file.value + "/" + hash_file
        print("Download started, please wait....", end="")
        try:
            response = requests.get(
                ep,
                headers={"Authorization": f"Bearer {self.__token}"},
                allow_redirects=True,
            )
            if response.status_code == 200:
                mtype = response.headers.get("content-type")
                filename = (
                    f"./{hash_file}" if local_file_name == None else local_file_name
                )
                open(filename, "wb").write(response.content)
                print("Done!")
            else:
                print("The requested file is not available on server!")
        except Exception as e:
            print("Error downloading file! Error: ", e)

    def delete_project_file(self, hash_file):
        if self.__token == None:
            self.get_token()
        ep = endpoints.delete_project_file.value + hash_file
        try:
            print(f"Deleting file {hash_file}")
            response = requests.delete(
                ep,
                headers={"Authorization": f"Bearer {self.__token}"},
                allow_redirects=True,
            )
            if response.status_code == 200:
                print(json.loads(response.text)["status"])
            else:
                print("The requested file is not available on server!")
        except Exception as e:
            print("Error downloading file! Error: ", e)
