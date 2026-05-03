from fastapi import FastAPI,Depends,HTTPException,status
import uvicorn
from route import pdf_router
#=======================Creating your App==================================
app=FastAPI()

app.include_router(pdf_router,prefix="/pdf",tags=["PDF Search"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)