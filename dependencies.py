from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
load = load_dotenv()
templates = Jinja2Templates(directory="templates")