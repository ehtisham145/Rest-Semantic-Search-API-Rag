from fastapi import FastAPI,HTTPException,APIRouter,status,UploadFile,File
from pypdf import PdfReader
from dotenv import load_dotenv
from model import extract_text_chunks,get_embeddings
load_dotenv()
import uuid 
from uuid import UUID
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance,VectorParams
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import os
from qdrant_client.http.models import PointStruct

import shutil
from vector_db import setup_qdrant_database
embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#--------------------Creating a Query Router-----------------------------------
pdf_router=APIRouter()

#-----------------Directory where uploaded pdf will be saved---------------------
UPLOAD_DIR="uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)
#----------------Endpoint for Uploading PDF---------------------------------------
@pdf_router.post("/Upload_PDF_Here",status_code=status.HTTP_200_OK)
async def upload_pdf(file:UploadFile=File(...)):
    try:
    #check whether the file uploaded is pdf or not
        if file.content_type!="application/pdf":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User can Upload pdf files only")
        #Saving File in the Uploaded Dir
        file_path=os.path.join(UPLOAD_DIR,file.filename)
        #Saving the File in System
        with open(file_path,"wb") as f: # Here we are opening file in write mode
#binary mode is used when the data in file is audio vedio format
#shutil.copyfileobj actually take a file data from source path and copy it to the destination here the destination is f
#here file.file is giving you to the file
            shutil.copyfileobj(file.file,f)
        #Loading file data
        with open(file_path,"rb") as f:
            data=f.read()
        
        #Text Chunking
        chunk_text=extract_text_chunks(data)
        if not chunk_text:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Unable to Extract Text from PDF")
        
        #Creating Embedding
        embeddings=get_embeddings(embedding_model,chunk_text)

        #Storing your Embeddings in Vector DataBase
        client,collection_name=setup_qdrant_database()
        if client is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Vector Database Connection has been failed")
        else:
                                points=[]

                                for i,vector in enumerate(embeddings):
                                    points.append(
                                        PointStruct(
                                            id=str(uuid.uuid4()),
                                            vector=vector,
                                            payload={
                                                "file_name":file.filename,
                                                "text":chunk_text[i]
                                            }
                                        )
                                    )
                                #8.Uploading Data in Database
                                client.upsert(
                                    collection_name=collection_name,
                                    points=points
                                )
                                return {"message": f"PDF '{file.filename}' uploaded and indexed successfully.", "chunks": len(points)}

    except Exception as e:
        print(f"An Error Occured : {e}")

@pdf_router.get("/Enter your query/{query}",status_code=status.HTTP_200_OK)
def enter_your_query(query:str):
    try:
        #Creating Embedding of Query
        q_embedding=get_embeddings(embedding_model,[query])[0]
        #Setting Database
        client,collection_name=setup_qdrant_database()
        if client is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Vector DataBase Connection has been Failed")
        #Finding Similar Vectors
        search_result=client.query_points(
                collection_name=collection_name,
                query=q_embedding,
                limit=5
            ).points

        #check if search result is not empty
        if  not search_result:
               return {"mesaage":"No Relevant Answer found !"}
                
        else:
            results=[]
            for i,hit in enumerate(search_result):
                results.append({
                "rank": i + 1,
                "score": round(hit.score, 2),
                "text": hit.payload.get("text"),
                "file": hit.payload.get("file_name"),
            })

        return {"results": results}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
