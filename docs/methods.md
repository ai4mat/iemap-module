# Full list of IEMAP methods

`check_metadata()`: Check metadata schema for validation.

`get_id()` : Get the id of the current object.

`set_id(id)` : Set the id of the current object.

`get_token()` : Get the token of the current object.

`login()` : Login to the server.

`show_token()`: Show the token of the current object.

`_load_metadata(file_path)`: Load metadata from a file.

`save(metadata, list_proj_files=[], show_debug_info=False)`: Save the current object to the server.

`save_project_files(project_files, show_debug_info=False)`: Save project files to the server.

`save_property_files(props_files, show_debug_info=False)`: Save property files to the server.

`query(doc_id)`: Query the server for a document.

`my_projects()`: Get the list of projects owned by the current user.

`download_file(hash_file, local_file_name=None)` : Download a file from the server.

`delete_project_file(hash_file)`: Delete a project file from the server.