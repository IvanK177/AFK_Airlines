import pytest
import main

def test_e2e_cli_menu_flow(monkeypatch, capsys):
    """
    Сквозной тест меню авиасистемы:
    1. Передаем неверный choice '9' (проверка валидации)
    2. Передаем choice '3' (просмотр)
       - Фильтр рейса: '' (Enter, без фильтра)
       - Фильтр статуса: '' (Enter, без фильтра)
    3. Передаем choice '5' (выход)
    """
   
    user_steps = iter(["9", "3", "", "", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_steps))

    with pytest.raises(SystemExit) as exit_info:
        main.main()

    assert exit_info.value.code == 0

    output = capsys.readouterr().out
    
    assert "[Ошибка] Команды '9' не существует" in output
    
    assert "ID Заказа" in output
    assert "SU1120" in output
    assert "Иванов Иван" in output
    assert "оформлен" in output
    
    assert "Работа завершена. До свидания!" in output
