# FastAPI-Project

This is a simple FastAPI project demonstrating CRUD operations.

**Setup**

1. **Clone the repository:**
git clone https://github.com/yourusername/fastapi-project.git

2. **Navigate to the project directory:**
cd fastapi-project

3. **Install dependencies:**
pip install -r requirements.txt

4. Run the application:
uvicorn main:app --reload

5. **Open your web browser and go to http://localhost:8000/docs to view the API documentation.**

**Usage**

**Create Record:** Send a POST request to /records endpoint with JSON payload containing name and value fields.
**Read Records:** Send a GET request to /records endpoint to retrieve all records.
**Update Record:** Send a PUT request to /records/{record_id} endpoint with JSON payload containing updated name and value fields.
**Delete Record:** Send a DELETE request to /records/{record_id} endpoint to delete a record by its ID.

Refer to the API documentation for more detailed usage instructions and examples.

**Project Structure**

**app.py:** Contains the FastAPI application instance.
**main.py:** Defines the FastAPI routes and CRUD operations.
**requirements.txt:** Lists all Python dependencies required for the project.
