import os
from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["pages"])

# TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
# templates = Jinja2Templates(directory=TEMPLATES_DIR)
_CURRENT_DIR = Path(__file__).parent
_WEB_UI_PATH = _CURRENT_DIR / "web_ui.html"

@router.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    # return templates.TemplateResponse("web_ui.html", {"request": request})
    
    with open(_WEB_UI_PATH, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())