<!-- filepath: /Users/kuba/Documents/git/helceletka/ForrestHub/docs/api/index.md -->
# ForrestHub API Documentation

This document provides documentation for the ForrestHub HTTP API. All endpoints are prefixed with `/api`.

## Root

### `GET /api/`

Provides a basic health check or welcome message for the API.

**Curl Example:**
```bash
curl http://localhost:5000/api/
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/"
response = requests.get(url)
print(response.json())
# Expected output might be: {"status": "ok", "message": "ForrestHub API is running"}
```

---

## Admin Config

### `POST /api/admin/message`

Sends a message to all connected admin clients via SocketIO.

**Request Body:** JSON object
```json
{
  "message": "Your message here"
}
```

**Curl Example:**
```bash
curl -X POST -H "Content-Type: application/json" -d \'\'\'{"message": "Hello Admins"}\'\'\' http://localhost:5000/api/admin/message
```

**Python Example:**
```python
import requests
import json

url = "http://localhost:5000/api/admin/message"
payload = {"message": "Hello Admins"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
```

---

### `GET /api/clients/count`

Gets the current count of connected SocketIO clients.

**Curl Example:**
```bash
curl http://localhost:5000/api/clients/count
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/clients/count"
response = requests.get(url)
print(response.json())
```

---

### `GET /api/game/status`

Gets the current game status.

**Curl Example:**
```bash
curl http://localhost:5000/api/game/status
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/game/status"
response = requests.get(url)
print(response.json())
```

---

### `POST /api/game/status`

Sets the game status. The new status is broadcasted to connected clients via SocketIO.

**Request Body:** JSON object
```json
{
  "status": "new_game_status"
}
```

**Curl Example:**
```bash
curl -X POST -H "Content-Type: application/json" -d \'\'\'{"status": "paused"}\'\'\' http://localhost:5000/api/game/status
```

**Python Example:**
```python
import requests
import json

url = "http://localhost:5000/api/game/status"
payload = {"status": "paused"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
```

---

## Edit Mode

### `GET /api/edit_mode`

Gets the current state of the edit mode (on/off).

**Curl Example:**
```bash
curl http://localhost:5000/api/edit_mode
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/edit_mode"
response = requests.get(url)
print(response.json())
```

---

### `POST /api/edit_mode`

Sets the edit mode. If turned on, it may trigger actions like copying a default game. The new state is broadcasted via SocketIO.

**Request Body:** JSON object
```json
{
  "edit_mode_on": true
}
```

**Curl Example:**
```bash
curl -X POST -H "Content-Type: application/json" -d \'\'\'{"edit_mode_on": true}\'\'\' http://localhost:5000/api/edit_mode
```

**Python Example:**
```python
import requests
import json

url = "http://localhost:5000/api/edit_mode"
payload = {"edit_mode_on": True} # Or False
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
```

---

## Admin Access (Database)

### `GET /api/db/all_data`

Retrieves all data from the database.

**Curl Example:**
```bash
curl http://localhost:5000/api/db/all_data
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/db/all_data"
response = requests.get(url)
print(response.json())
# Note: The actual data structure will depend on your db.get_all_data() implementation.
```

---

### `POST /api/db/delete_all_data`

Clears all data from the database. (Note: Uses POST, but a DELETE method might be more semantically correct for a "delete all" operation if preferred).

**Curl Example:**
```bash
curl -X POST http://localhost:5000/api/db/delete_all_data
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/db/delete_all_data"
response = requests.post(url)
print(response.json())
```

---

## VAR (Variables)

### `POST /api/var`

Sets or updates a key-value pair for a given project. This corresponds to the `var_key_set` SocketIO event. The behavior is that it calls `db.var_key_get(project, key, value)`, which implies it might *get* if value is for default, or *set* if value is provided to change. The API endpoint name `var_key_set_http` suggests it's primarily for setting.

**Request Body:** JSON object
```json
{
  "project": "myProject",
  "key": "myKey",
  "value": "myValue"
}
```

**Curl Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d \'\'\'{"project": "game1", "key": "score", "value": 100}\'\'\' \
  http://localhost:5000/api/var
```

**Python Example:**
```python
import requests
import json

url = "http://localhost:5000/api/var"
payload = {"project": "game1", "key": "score", "value": 100}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
```

---

### `GET /api/var/exists`

Checks if a specific key exists for a given project.

**Query Parameters:**
*   `project` (string, required): The name of the project.
*   `key` (string, required): The key to check.

**Curl Example:**
```bash
curl "http://localhost:5000/api/var/exists?project=game1&key=score"
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/var/exists"
params = {"project": "game1", "key": "score"}

response = requests.get(url, params=params)
print(response.json())
```

---

### `GET /api/var`

Gets the value of a key for a given project. A default value can be provided if the key is not found.

**Query Parameters:**
*   `project` (string, required): The name of the project.
*   `key` (string, required): The key whose value is to be retrieved.
*   `defaultValue` (string, optional): The value to return if the key is not found. Defaults to an empty string.

**Curl Example:**
```bash
curl "http://localhost:5000/api/var?project=game1&key=playerName&defaultValue=Guest"
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/var"
params = {"project": "game1", "key": "playerName", "defaultValue": "Guest"}

response = requests.get(url, params=params)
print(response.json())
```

---

### `DELETE /api/var`

Deletes a key-value pair for a given project.

**Query Parameters (can also be in JSON body):**
*   `project` (string, required): The name of the project.
*   `key` (string, required): The key to delete.

**Curl Example (using query parameters):**
```bash
curl -X DELETE "http://localhost:5000/api/var?project=game1&key=score"
```

**Curl Example (using JSON body):**
```bash
curl -X DELETE -H "Content-Type: application/json" \
  -d \'\'\'{"project": "game1", "key": "score"}\'\'\' \
  http://localhost:5000/api/var
```

**Python Example (using query parameters):**
```python
import requests

url = "http://localhost:5000/api/var"
params = {"project": "game1", "key": "score"}

response = requests.delete(url, params=params)
print(response.json())
```

**Python Example (using JSON body):**
```python
import requests
import json

url = "http://localhost:5000/api/var"
payload = {"project": "game1", "key": "score"}
headers = {"Content-Type": "application/json"}

response = requests.delete(url, data=json.dumps(payload), headers=headers)
print(response.json())
```

---

## Array

### `POST /api/array/record`

Adds a record to an array within a specific project. A `recordId` can optionally be provided.

**Request Body:** JSON object
```json
{
  "project": "myProject",
  "arrayName": "myArray",
  "value": {"data": "some_value"},
  "recordId": "optionalRecordId"
}
```

**Curl Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d \'\'\'{"project": "leaderboard", "arrayName": "scores", "value": {"user": "player1", "points": 1500}, "recordId": "player1_score"}\'\'\' \
  http://localhost:5000/api/array/record
```

**Python Example:**
```python
import requests
import json

url = "http://localhost:5000/api/array/record"
payload = {
    "project": "leaderboard",
    "arrayName": "scores",
    "value": {"user": "player1", "points": 1500},
    "recordId": "player1_score" # Optional
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
```

---

### `DELETE /api/array/record`

Removes a record from an array within a specific project using its `recordId`.

**Query Parameters (can also be in JSON body):**
*   `project` (string, required): The name of the project.
*   `arrayName` (string, required): The name of the array.
*   `recordId` (string, required): The ID of the record to remove.

**Curl Example (using query parameters):**
```bash
curl -X DELETE "http://localhost:5000/api/array/record?project=leaderboard&arrayName=scores&recordId=player1_score"
```

**Python Example (using query parameters):**
```python
import requests

url = "http://localhost:5000/api/array/record"
params = {
    "project": "leaderboard",
    "arrayName": "scores",
    "recordId": "player1_score"
}
response = requests.delete(url, params=params)
print(response.json())
```

---

### `GET /api/array/record`

Retrieves a specific record from an array within a project using its `recordId`.

**Query Parameters:**
*   `project` (string, required): The name of the project.
*   `arrayName` (string, required): The name of the array.
*   `recordId` (string, required): The ID of the record to retrieve.

**Curl Example:**
```bash
curl "http://localhost:5000/api/array/record?project=leaderboard&arrayName=scores&recordId=player1_score"
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/array/record"
params = {
    "project": "leaderboard",
    "arrayName": "scores",
    "recordId": "player1_score"
}
response = requests.get(url, params=params)
print(response.json())
```

---

### `PUT /api/array/record`

Updates an existing record in an array within a project.

**Request Body:** JSON object
```json
{
  "project": "myProject",
  "arrayName": "myArray",
  "recordId": "existingRecordId",
  "value": {"newData": "updated_value"}
}
```

**Curl Example:**
```bash
curl -X PUT -H "Content-Type: application/json" \
  -d \'\'\'{"project": "leaderboard", "arrayName": "scores", "recordId": "player1_score", "value": {"user": "player1", "points": 1600}}\'\'\' \
  http://localhost:5000/api/array/record
```

**Python Example:**
```python
import requests
import json

url = "http://localhost:5000/api/array/record"
payload = {
    "project": "leaderboard",
    "arrayName": "scores",
    "recordId": "player1_score",
    "value": {"user": "player1", "points": 1600}
}
headers = {"Content-Type": "application/json"}

response = requests.put(url, data=json.dumps(payload), headers=headers)
print(response.json())
```

---

### `GET /api/array/all_records`

Retrieves all records from a specific array within a project.

**Query Parameters:**
*   `project` (string, required): The name of the project.
*   `arrayName` (string, required): The name of the array.

**Curl Example:**
```bash
curl "http://localhost:5000/api/array/all_records?project=leaderboard&arrayName=scores"
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/array/all_records"
params = {"project": "leaderboard", "arrayName": "scores"}
response = requests.get(url, params=params)
print(response.json())
```

---

### `GET /api/array/record/exists`

Checks if a specific record exists in an array within a project.

**Query Parameters:**
*   `project` (string, required): The name of the project.
*   `arrayName` (string, required): The name of the array.
*   `recordId` (string, required): The ID of the record to check.

**Curl Example:**
```bash
curl "http://localhost:5000/api/array/record/exists?project=leaderboard&arrayName=scores&recordId=player1_score"
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/array/record/exists"
params = {
    "project": "leaderboard",
    "arrayName": "scores",
    "recordId": "player1_score"
}
response = requests.get(url, params=params)
print(response.json())
```

---

### `POST /api/array/clear_records`

Clears all records from a specific array within a project.

**Request Body:** JSON object
```json
{
  "project": "myProject",
  "arrayName": "myArray"
}
```

**Curl Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d \'\'\'{"project": "leaderboard", "arrayName": "scores"}\'\'\' \
  http://localhost:5000/api/array/clear_records
```

**Python Example:**
```python
import requests
import json

url = "http://localhost:5000/api/array/clear_records"
payload = {"project": "leaderboard", "arrayName": "scores"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
```

---

### `GET /api/array/projects`

Lists all projects that have arrays.

**Curl Example:**
```bash
curl http://localhost:5000/api/array/projects
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/array/projects"
response = requests.get(url)
print(response.json())
```

---

## Edit Game

### `POST /api/game/new`

Creates a new game folder.

**Request Body:** JSON object
```json
{
  "game_name": "newGameName"
}
```

**Curl Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d \'\'\'{"game_name": "MyAwesomeGame"}\'\'\' \
  http://localhost:5000/api/game/new
```

**Python Example:**
```python
import requests
import json

url = "http://localhost:5000/api/game/new"
payload = {"game_name": "MyAwesomeGame"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
```

---

### `POST /api/game/page_html`

Sets the HTML content of a specific page within a game. Creates the game folder or page if it doesn't exist.

**Request Body:** JSON object
```json
{
  "game_name": "myGame",
  "game_page": "mainPage",
  "game_content": "<h1>Hello World!</h1>"
}
```
*   `game_page`: Name of the page without the `.html` extension.

**Curl Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d \'\'\'{"game_name": "MyAwesomeGame", "game_page": "index", "game_content": "<html><body><h1>Welcome!</h1></body></html>"}\'\'\' \
  http://localhost:5000/api/game/page_html
```

**Python Example:**
```python
import requests
import json

url = "http://localhost:5000/api/game/page_html"
payload = {
    "game_name": "MyAwesomeGame",
    "game_page": "index", # page name without .html
    "game_content": "<html><body><h1>Welcome!</h1></body></html>"
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
```

---

### `GET /api/game/page_html`

Retrieves the HTML content of a specific page within a game.

**Query Parameters:**
*   `game_name` (string, required): The name of the game.
*   `game_page` (string, required): The name of the page (without `.html` extension).

**Curl Example:**
```bash
curl "http://localhost:5000/api/game/page_html?game_name=MyAwesomeGame&game_page=index"
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/api/game/page_html"
params = {"game_name": "MyAwesomeGame", "game_page": "index"}
response = requests.get(url, params=params)
print(response.json())
# The HTML content will be in response.json().get("content")
```
