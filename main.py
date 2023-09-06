from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


import json

app = FastAPI()

# Serve static files
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ethics")
def ethics(request: Request):
    return templates.TemplateResponse("ethics.html", {"request": request})

@app.get("/assign_group")
def assign_group(request: Request):
    with open('group_data.json', 'r') as file:
        data = json.load(file)
        last_group = data['last_group']

    # Alternate group assignment
    if last_group == 'A':
        new_group = 'B'
        next_page = "/infographic1"  # This can be the link to the first page of Group B content
    else:
        new_group = 'A'
        next_page = "/video1"  # This can be the link to the first page of Group A content

    # Update the JSON file on the disk
    with open('group_data.json', 'w') as file:
        json.dump({'last_group': new_group}, file)

    return templates.TemplateResponse("assign_group.html", {
        "request": request,
        "group": new_group,
        "next_page": next_page  # Pass the next_page variable to the template
    })

@app.get("/video1")
def video1(request: Request):
    return templates.TemplateResponse("video1.html", {"request": request})

@app.get("/video2")
def video2(request: Request):
    return templates.TemplateResponse("video2.html", {"request": request})

@app.get("/video3")
def video1(request: Request):
    return templates.TemplateResponse("video3.html", {"request": request})

@app.get("/video4")
def video2(request: Request):
    return templates.TemplateResponse("video4.html", {"request": request})

@app.get("/infographic1")
def video1(request: Request):
    return templates.TemplateResponse("infographic1.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

