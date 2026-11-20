import importlib.util
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "ceunia" / "triads" / "runtime.py"
spec = importlib.util.spec_from_file_location("ceunia_triads_runtime", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_sha256_is_stable():
    assert mod.sha256_text("CEUNIA") == mod.sha256_text("CEUNIA")
    assert len(mod.sha256_text("CEUNIA")) == 64

def test_plan_never_claims_execution():
    row = {
        "numero": "01", "id_ceunia": "T001", "nombre_triada": "Tiempo Informacional",
        "personalidad_1": "Nikola Tesla", "personalidad_2": "Leonardo Fibonacci",
        "personalidad_3": "Albert Einstein", "perfil_conocimiento": "Señales y tiempo",
        "mision": "Medir una hipótesis", "entregable": "Informe reproducible",
        "criterio_evolutivo": "Comparación con línea base",
        "criterio_integracion": "Colaborar por necesidad", "estado": "DISEÑADA"
    }
    payload = mod.mission_payload(row)
    assert payload["triad_id"] == "T001"
    assert payload["execution_status"] == "PLANNED_NOT_EXECUTED"
    assert payload["requires_human_review"] is True
