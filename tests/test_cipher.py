from src.agent import CipherAgent
def test_cipher_requires_ci():
    p = CipherAgent().plan("p95 latency high")
    assert p.requires_ci is True
