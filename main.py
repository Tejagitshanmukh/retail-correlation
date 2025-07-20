from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract

app = FastAPI()

EMAIL = "22f2001007@ds.study.iitm.ac.in"

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file)
        text = pytesseract.image_to_string(image)

        # Extract numbers from text
        import re
        numbers = list(map(int, re.findall(r'\d+', text)))

        if len(numbers) != 2:
            return JSONResponse(content={"error": "Could not extract two numbers"}, status_code=400)

        result = numbers[0] * numbers[1]
        return {"answer": result, "email": EMAIL}
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
