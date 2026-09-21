from labnote_voice.session import handle


def test_requires_final_turn():
    assert handle({"type": "transcript.user.delta", "text": "x"}) == "ignored"


def test_binds_final_turn():
    assert handle({"type": "transcript.user", "text": "x"}) == "dispatched"
    assert handle({"type": "reply.done", "status": "interrupted"}) == "cancelled"
