from sqlmodel import Session, select
from modelos.modelos import Generacion
from modelos.modelos_de_la_db import GeneracionTabla


class GeneracionRepositorio:
    """Repositorio para consultas de Generaciones."""

    def get_generaciones(self, session: Session) -> list[Generacion]:
        results = session.exec(select(GeneracionTabla)).all()
        return [
            Generacion(id=g.id_generacion, nombre=g.nombre_generacion)
            for g in results
        ]
