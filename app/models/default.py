from pydantic import BaseModel, Field

class Model404(BaseModel):
    errormessage : str = Field(..., example="Not found or invalid path")
    errorcode : int = Field(..., example=404)

class Model422(BaseModel):
    errormessage : str = Field(..., example="Invalid input")
    errorcode : int = Field(..., example=422)