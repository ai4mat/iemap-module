# How to login using the IEMAP module

After the IEMAP module has been installed ed imported, you can use it to login just by defining the `user` and `password` variables:

```python
user = "your_user"
password = "your_password"
```

Then you can use them to create an instance of the `IEMAP` class:
   
```python
api = IEMAP(user, password)
```
Finally, you can use the `login()` method to login to the server:
   
```python
api.login()
```

## Check your login

You can check if the login has been worked by using the `get_token()` method:

```python
api.get_token()
```
If the login has been successful, you'll get `True` as response. Otherwise, an error will be raised.