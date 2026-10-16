from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_tokenise_returns_dictionary_form():
    # 1. Send the request
    response = client.post(
        "/tokenise", json={"text": "昨日、友達と映画を見に行きました。"}
    )

    # 2. Check it worked
    assert response.status_code == 200

    # 3. Find the token for 見
    tokens = response.json()
    mi = None
    for token in tokens:
        if token["surface"] == "見":
            mi = token

    # 4. Check what Sudachi said about it
    assert mi is not None
    assert mi["lemma"] == "見る"
    assert mi["pos"] == "動詞"
