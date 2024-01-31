from fastapi import FastAPI
from src.api.routes import router
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(router, prefix="/api/v1")    
app.mount("/static", StaticFiles(directory="./src/utils/static_files"), name="main")

origins = [
    "http://localhost.mario.com",
    "https://localhost.mario.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TO_DO: Render the DB_Documentation.md document to the HTML here

@app.get("/", response_class=HTMLResponse, tags=["API presentation"])
async def hello():
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>@Recipe Manager</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism.min.css" integrity="sha384-dxV5n507Ym1BNL/pW3RqQ7dE6sDRCXOJYNXI5rR1L9Rn8zQ8r2BE9ELzcrYqVIhF" crossorigin="anonymous">
    </head>
    <body style="background-color: #04010d;  background-image: url('/static/scattered-forcefields.svg'); background-size: cover; background-repeat: no-repeat; text-align: center; font-family: sans-serif;">
        <div style="margin-top: 190px;">
             <h1 style="background: #121FCF;
        background: linear-gradient(to right, #128dcf 35%, #9da806 50%, #CF009F 70%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;">Wellcome to Recipe Manager API!</h1>
            <p style="color: aliceblue;">Save, Cost, and Manage all your recipes easily!.</p>
        <img src='DB_Documentation.md'></img>
        </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/prism.min.js" integrity="sha384-HnZ9HEVj01htz7ZxhqfFH1RKAu7x3jj6XW9l3W4B4vPUGjrnppq6RvfbtErS5NqD" crossorigin="anonymous"></script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)