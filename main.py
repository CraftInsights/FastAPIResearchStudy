from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, StreamingResponse, Response
from filelock import FileLock
import mimetypes
import json
import uuid
import os

'''
 *Important Note*
 Special thanks to my wife Chloe for keeping me
 on track and helping me out with some tasks to 
 complete this project. 
'''

app = FastAPI()

# Serve static files
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Import the templates from the templates folder for Jinja2 to use
templates = Jinja2Templates(directory="templates")

# ---------------------------------------------------------------------------------------------------------------

# Function to serve video with support for range requests
def serve_video(video_path: str, request: Request) -> Response:
    '''
    Serve a video file with support for range requests.
    This allows seeking, pausing, and fast forwarding in video playback.
    '''
    
    range_header = request.headers.get("range", None)
    
    if not os.path.isfile(video_path) or not range_header:
        # If the video doesn't exist or there's no range request, return the whole file
        with open(video_path, "rb") as file:
            return StreamingResponse(file, media_type=mimetypes.guess_type(video_path)[0])

    file_size = os.path.getsize(video_path)
    
    # Parse the range header
    start, end = range_header.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else file_size - 1
    
    # Create the content for the specified range
    with open(video_path, "rb") as file:
        file.seek(start)
        video_data = file.read(end - start + 1)
    
    # Create the response headers
    response_headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(end - start + 1),
        "Content-Type": mimetypes.guess_type(video_path)[0],
    }
    
    return Response(video_data, status_code=206, headers=response_headers)

@app.get("/videos/{video_name}")
async def video_endpoint(request: Request, video_name: str):
    video_path = os.path.join("assets", "videos", video_name)
    return serve_video(video_path, request)

# ---------------------------------------------------------------------------------------------------------------

# Routing for the basic pages

# Homepage
@app.get("/")
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ethics + Consent page

@app.get("/ethics")
def ethics(request: Request):
    participant_id = str(uuid.uuid4())  # Generate a unique participant ID
    return templates.TemplateResponse("ethics.html", {"request": request, "participantID": participant_id})

# Debrief

@app.get("/debrief")
def debrief(request: Request):
    return templates.TemplateResponse("debrief.html", {"request": request})

# ---------------------------------------------------------------------------------------------------------------

# Group Assignment page - A or B

# Route for displaying the group assignment form
@app.get("/assign_group")
def show_form(request: Request, participantID: str = None):
    return templates.TemplateResponse("assign_group.html", {"request": request, "participantID": participantID})

# Route for handling the submission of the group assignment form
@app.post("/assign_group")
def assign_group_post(participantID: str):
    # Use a file lock to ensure safe concurrent access to the JSON data file
    lock = FileLock("group_data.json.lock")

    with lock:
        try:
            # Attempt to read the existing JSON data
            with open('group_data.json', 'r') as file:
                data = json.load(file)
                last_group = data.get('last_group', 'B')
                if "Participants" not in data:
                    data['Participants'] = {}
        except FileNotFoundError:
            # If the data file doesn't exist, create a new data structure
            data = {
                'Participants': {},
                'last_group': 'B'
            }
            last_group = 'B'

        # Determine the new group based on the last group assigned
        new_group = 'A' if last_group == 'B' else 'B'

        # Determine the next page and activity based on the new group
        next_page = f"/video1" if new_group == 'A' else f"/infographic1"
        activity = "This activity consists of 4 videos totaling roughly 10 min in length." if new_group == 'A' else "This activity consists of 7 infographics."

        # Add the participant to the data structure and update the last group
        data['Participants'][f'visitor {len(data["Participants"]) + 1}'] = {
            'ID': participantID,
            'Group': new_group
        }
        data['last_group'] = new_group

        # Write the updated data back to the JSON file
        with open('group_data.json', 'w') as file:
            json.dump(data, file, indent=4)

    # Redirect the user to the group information page
    return RedirectResponse(url=f"/show_group?group={new_group}&next_page={next_page}&activity={activity}&participantID={participantID}", status_code=303)

# Route for displaying the group information page
@app.get("/show_group")
def show_group(request: Request, group: str, next_page: str, activity: str, participantID: str):
    return templates.TemplateResponse("assign_group.html", {
        "request": request,
        "group": group,
        "next_page": next_page,
        "activity": activity,
        "participantID": participantID
    })

# ---------------------------------------------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------------------------------------------




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

