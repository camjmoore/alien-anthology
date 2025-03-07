from fastapi import FastAPI

app = FastAPI(
    title="Alien Anthology API",
    description="Serves data about the characters that inhabit the Alien Anthology universe",
    version="1.0.0"
)

@app.get("/characters")
def get_characters():
    pass
