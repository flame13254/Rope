from rope_edge.classifier import MockClassifier, make_classifier

def test_mock_alternate():
    m = MockClassifier(mode="alternate")
    assert m.predict(None) == (0, 0.9)
    assert m.predict(None) == (1, 0.9)
    assert m.predict(None) == (0, 0.9)

def test_mock_normal_mode():
    m = MockClassifier(mode="normal")
    assert m.predict(None)[0] == 0

def test_make_classifier_mock():
    c = make_classifier({"type": "mock", "path": "", "device": "auto"})
    assert isinstance(c, MockClassifier)
