
def test_index(testapp):
    res = testapp.get("/")
    assert res.status_code == 200
