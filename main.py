from app.api_service import app
import uvicorn

if __name__ == "__main__":
    print("\n🚀 Smart Document AI is starting up...")
    print("Visit http://127.0.0.1:8000 to access the API.\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
