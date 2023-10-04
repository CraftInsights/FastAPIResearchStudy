from fastapi import FastAPI, Request
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

# Homepage
@app.get("/")
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ethics + Consent page

@app.get("/ethics")
def ethics(request: Request):
    participant_id = str(uuid.uuid4())  # Generate a unique participant ID
    return templates.TemplateResponse("ethics.html", {"request": request, "participantID": participant_id})


# Group Assignment page - A or B

@app.get("/assign_group")
def show_form(request: Request, participantID: str = None):
    return templates.TemplateResponse("assign_group.html", {"request": request, "participantID": participantID})

@app.post("/assign_group")
def assign_group_post(participantID: str):
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

        new_group = 'A' if last_group == 'B' else 'B'

        next_page = f"/video1" if new_group == 'A' else f"/infographic1"

        activity = "This activity consists of 4 videos totaling roughly 10 min in length." if new_group == 'A' else "This activity consists of 7 infographics."

        data['Participants'][f'visitor {len(data["Participants"]) + 1}'] = {
            'ID': participantID,
            'Group': new_group
        }
        data['last_group'] = new_group

        with open('group_data.json', 'w') as file:
            json.dump(data, file, indent=4)

    return RedirectResponse(url=f"/show_group?group={new_group}&next_page={next_page}&activity={activity}&participantID={participantID}", status_code=303)

@app.get("/show_group")
def show_group(request: Request, group: str, next_page: str, activity: str, participantID: str):
    return templates.TemplateResponse("assign_group.html", {
        "request": request,
        "group": group,
        "next_page": next_page,
        "activity": activity,
        "participantID": participantID
    })

# Routing for video content

@app.get("/video1")
def video1(request: Request, participantID: str):
    return templates.TemplateResponse("video1.html", {"request": request, "participantID": participantID})

@app.get("/video2")
def video2(request: Request, participantID: str):
    return templates.TemplateResponse("video2.html", {"request": request, "participantID": participantID})

@app.get("/video3")
def video3(request: Request, participantID: str):
    return templates.TemplateResponse("video3.html", {"request": request, "participantID": participantID})

@app.get("/video4")
def video4(request: Request, participantID: str):
    return templates.TemplateResponse("video4.html", {"request": request, "participantID": participantID})

# Routing for infographic content

@app.get("/infographic1")
def infographic1(request: Request, participantID: str):
    return templates.TemplateResponse("infographic1.html", {"request": request, "participantID": participantID})

@app.get("/infographic2")
def infographic2(request: Request, participantID: str):
    return templates.TemplateResponse("infographic2.html", {"request": request, "participantID": participantID})

@app.get("/infographic3")
def infographic3(request: Request, participantID: str):
    return templates.TemplateResponse("infographic3.html", {"request": request, "participantID": participantID})

@app.get("/infographic4")
def infographic4(request: Request, participantID: str):
    return templates.TemplateResponse("infographic4.html", {"request": request, "participantID": participantID})

@app.get("/infographic5")
def infographic5(request: Request, participantID: str):
    return templates.TemplateResponse("infographic5.html", {"request": request, "participantID": participantID})

# Survey routing

@app.get("/pre_survey")
def pre_survey(request: Request, participantID: str = None):
    return templates.TemplateResponse("pre_survey.html", {"request": request, "participantID": participantID})


@app.get("/post_survey_videos")
def post_survey_videos(participantID: str):
    post_survey_url = f"https://yorkufoh.ca1.qualtrics.com/jfe/form/SV_2rzqeitqJa1ZWpU?participantID={participantID}"
    return RedirectResponse(url=post_survey_url, status_code=303)

@app.get("/post_survey_infographic")
def post_survey_infographic(participantID: str):
    post_survey_url = f"https://yorkufoh.ca1.qualtrics.com/jfe/form/SV_cMhhfU5fF7pXHJI?participantID={participantID}"
    return RedirectResponse(url=post_survey_url, status_code=303)

# Debrief

@app.get("/debrief")
def debrief(request: Request):
    return templates.TemplateResponse("debrief.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

