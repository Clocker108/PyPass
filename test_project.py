from project import menu, reset, decrypt

def test_menu():
    assert menu('1') == '1'
    assert menu('3') == '3'
    assert menu('menu') == 'Wrong'

def test_reset(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'new_password')
    assert reset() == 1

def test_decrypt(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'new_password')
    assert decrypt() == 0