from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from filelock import FileLock
import json
import uuid

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
def show_form(request: Request):
    return templates.TemplateResponse("assign_group.html", {"request": request})

@app.post("/assign_group")
def assign_group_post():
    lock = FileLock("group_data.json.lock")

    with lock:
        try:
            with open('group_data.json', 'r') as file:
                data = json.load(file)
                last_group = data.get('last_group', 'B')
                if "Participants" not in data:
                    data['Participants'] = {}
        except FileNotFoundError:
            data = {
                'Participants': {},
                'last_group': 'B'
            }
            last_group = 'B'

        visitor_id = str(uuid.uuid4())
        new_group = 'A' if last_group == 'B' else 'B'

        next_page = "/video1" if new_group == 'A' else "/infographic1"

        data['Participants'][f'visitor {len(data["Participants"]) + 1}'] = {
            'ID': visitor_id,
            'Group': new_group
        }
        data['last_group'] = new_group

        with open('group_data.json', 'w') as file:
            json.dump(data, file, indent=4)

    return RedirectResponse(url=f"/show_group?group={new_group}&next_page={next_page}", status_code=303)

@app.get("/show_group")
def show_group(request: Request, group: str, next_page: str):
    return templates.TemplateResponse("assign_group.html", {
        "request": request,
        "group": group,
        "next_page": next_page
    })

# Routing for video content

@app.get("/video1")
def video1(request: Request):
    return templates.TemplateResponse("video1.html", {"request": request})

@app.get("/video2")
def video2(request: Request):
    return templates.TemplateResponse("video2.html", {"request": request})

@app.get("/video3")
def video3(request: Request):
    return templates.TemplateResponse("video3.html", {"request": request})

@app.get("/video4")
def video4(request: Request):
    return templates.TemplateResponse("video4.html", {"request": request})

# Routing for infographic content

@app.get("/infographic1")
def infographic1(request: Request):
    return templates.TemplateResponse("infographic1.html", {"request": request})

@app.get("/infographic2")
def infographic2(request: Request):
    return templates.TemplateResponse("infographic2.html", {"request": request})

@app.get("/infographic3")
def infographic3(request: Request):
    return templates.TemplateResponse("infographic3.html", {"request": request})

@app.get("/infographic4")
def infographic4(request: Request):
    return templates.TemplateResponse("infographic4.html", {"request": request})

@app.get("/infographic5")
def infographic5(request: Request):
    return templates.TemplateResponse("infographic5.html", {"request": request})

# Survey routing

@app.get("/pre_survey")
def pre_survey(request: Request):
    return templates.TemplateResponse("pre_survey.html", {"request": request})

@app.get("/post_survey_videos")
def post_survey_videos(request: Request):
    return templates.TemplateResponse("post_survey_videos.html", {"request": request})

@app.get("/post_survey_infographic")
def post_survey_infographic(request: Request):
    return templates.TemplateResponse("post_survey_infographic.html", {"request": request})

# Debrief

@app.get("/debrief")
def debrief(request: Request):
    return templates.TemplateResponse("debrief.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

