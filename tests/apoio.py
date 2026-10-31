from pathlib import Path
import tempfile


def PastaTemporaria():
    # Mantém e confere os arquivos temporários dentro da área dos testes.
    raiz = Path(__file__).resolve().parent
    pasta = tempfile.TemporaryDirectory(prefix="temporario_", dir=raiz)
    if not Path(pasta.name).resolve().is_relative_to(raiz):
        raise RuntimeError("Pasta de teste fora do projeto.")
    return pasta
