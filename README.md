# iemap-module

This module provides simple functions to interact with the iemap API. 

## Quickstart
1. Create a virtual environment and install the module in it:
    ```bash
    pip install iemap
    ```

2. In your script or notebook, import the module:
    ```python
    from iemap import IEMAP
    ```

3. Create an instance of the `IEMAP` class, using your `user` and `password`:
    ```python
    api = IEMAP(user, password)
    ```

4. Use the `login()` method for API login:
    ```python
    api.login()
    ```

5. Use the `my_projects()` method to get a list of your projects:
    ```python
    api.my_projects()
    ```