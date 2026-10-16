from fastapi import FastAPI
from pydantic import BaseModel
from sudachipy import dictionary, tokenizer

app = FastAPI(title="Sentence Miner API")

# Load the dictionary ONCE, when the server starts.
# Loading it is slow, so we don't want to do it on every request.
_tokenizer = dictionary.Dictionary().tokenizer()
_MODE = tokenizer.Tokenizer.SplitMode.C


class TokeniseRequest(BaseModel):
    text: str


class Token(BaseModel):
    surface: str
    lemma: str
    reading: str
    pos: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tokenise")
def tokenise(req: TokeniseRequest) -> list[Token]:
    tokens = []
    for m in _tokenizer.tokenize(req.text, _MODE):
        token = Token(
            surface=m.surface(),
            lemma=m.dictionary_form(),
            reading=m.reading_form(),
            pos=m.part_of_speech()[0],
        )
        tokens.append(token)
    return tokens