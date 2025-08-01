import pytest
from apps.shared.value_objects import PostalCode

# Válidos (nacionais e internacionais)
@pytest.mark.parametrize("valid_code", [
    "01001-000",    # Brasil
    "90210",        # EUA (ZIP)
    "12345-6789",   # EUA (ZIP+4)
    "K1A 0B1",      # Canadá
    "75008",        # França
    "EC1A1BB",      # Reino Unido
])
def test_postal_code_vo_accepts_valid_codes(valid_code):
    vo = PostalCode(valid_code)
    assert vo.value == valid_code.strip()


# Inválidos
@pytest.mark.parametrize("invalid_code", [
    "12",           # Muito curto
    "A",            # Muito curto
    "12345678910",  # Muito longo
    "1234!",        # Caractere inválido
    "@90210",       # Caractere inválido
    "AB#123",       # Caractere inválido
])
def test_postal_code_vo_rejects_invalid_codes(invalid_code):
    with pytest.raises(ValueError):
        PostalCode(invalid_code)
