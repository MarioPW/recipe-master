from fastapi import FastAPI
from src.api.routes import router
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(router, prefix="/api/v1")    
app.mount("/static", StaticFiles(directory="./src/utils/static_files"), name="main")

@app.get("/", response_class=HTMLResponse, tags=["API presentation"])
async def hello():
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>@Recipe Manager</title>
    </head>
    <body style="background-color: #04010d;  background-image: url('/static/scattered-forcefields.svg'); background-size: cover; background-repeat: no-repeat; text-align: center; font-family: sans-serif;">
        <div style="margin-top: 190px;">
             <h1 style="background: #121FCF;
        background: linear-gradient(to right, #128dcf 35%, #9da806 50%, #CF009F 70%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;">Wellcome to Recipe Manager API!</h1>
            <p style="color: aliceblue;">Save, Cost, and Manage all your recipes easily!.</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)