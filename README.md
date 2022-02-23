# A Simple Account System implemented in FastAPI and SQLite

# To Run the FastAPI Application on Port 8000

```python
python main.py

```

# Viewing Auto-Gen FastAPI Documentation

The Documentation is auto-generated at :

http://localhost:8000/docs 
or
http://0.0.0.0:8000/docs


## APIS Available

There are 3 APIS :

### Create User
```http
curl -X POST "http://host:8000/users/" 

-H  "accept: application/json" 
-H  "Content-Type: application/json" 
-d "{\"name\":\"string\",\"email\":\"string\",\"password\":\"string\"}"
```

| Parameters | Type | Description |
| :--- | :--- | :--- |
| `name, email, password` | `string` | **Required** |

#### Response
```http
	{
	  "success": true,
	  "message": "User Account Created",
 	 "code": 200
	}
```



### Login | Returns a JWT Token

```http
curl -X PUT "http://host:8000/users/" 
-H  "accept: application/json" 
-H  "Content-Type: application/json" 
-d "{\"email\":\"string\",\"password\":\"string\"}"
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `email, password` | `string` | **Required**. |

#### Response
```http
	{
	  "success": true,
       "token": “token_string”,
	  "message": “Log in Successful",
	}
```


### Get Users | Requires JWT Authentication

```http
curl -X GET "http://lhost:8000/users/" 
-H  "accept: application/json" 
-H  "Authorization: JWT Token
```
#### Response
```http
	{
  	"success": true,
  	"message": {
    "hashed_password": 	“hashed_string",
	"name": "string",
    	"email": "string"
 	 },
  	"code": 200
	}
```

