
# ============================================================
# IMPORTA TODOS OS MODELS
#
# Isso garante que o SQLAlchemy conheça todos os relacionamentos
# antes de inicializar os mappers.
# ============================================================

from backend.models.usuario import Usuario
from backend.models.token import Token
from backend.models.participante import Participante

from backend.models.especie import Especie
from backend.models.animal import Animal
from backend.models.planta import Planta
from backend.models.bioma import Bioma
from backend.models.especie_bioma import EspecieBioma

