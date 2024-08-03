from .add import router as add_router
from .edit import router as edit_router
from .list import router as list_router
from .start import router as start_router
from .upload import router as upload_router

routers = [
    add_router,
    edit_router,
    list_router,
    start_router,
    upload_router,
]
