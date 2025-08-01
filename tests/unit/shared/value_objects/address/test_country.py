import pytest
from apps.shared.value_objects import Country


# Casos válidos com códigos ISO Alpha-2
@pytest.mark.parametrize(
    "valid_code", ["BR", "US", "CA", "DE", "FR", "JP", "CN", "IN", "ZA", "GB"]
)
def test_country_vo_accepts_valid_iso_codes(valid_code):
    vo = Country(valid_code)
    assert vo.value == valid_code.strip().upper()


# Casos inválidos
@pytest.mark.parametrize(
    "invalid_code",
    [
        "br",  # letras minúsculas
        "BRA",  # 3 letras
        "1A",  # número + letra
        "B1",  # letra + número
        "BRL",  # nome incorreto
        "BR ",  # espaço
        "",  # vazio
        None,  # não string
        123,  # tipo numérico
    ],
)
def test_country_vo_rejects_invalid_codes(invalid_code):
    with pytest.raises(ValueError):
        Country(invalid_code)
