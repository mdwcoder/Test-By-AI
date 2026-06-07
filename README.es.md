[Español](README.es.md) | [English](README.en.md)

---

# test-by-ai

`test-by-ai` es una herramienta CLI stateless y multiplataforma para ejecutar pruebas automatizadas contra APIs REST usando una especificacion OpenAPI.

Detecta problemas de salud, incumplimientos de contrato y fallos de manejo de errores con configuracion minima.

## Instalacion

### Linux y macOS

```bash
./init.sh
source ~/.bashrc  # o ~/.zshrc
test-by-ai --help
```

El instalador crea `.venv`, instala dependencias y registra el alias `test-by-ai`.

### Windows PowerShell

```powershell
.\init.ps1
```

Reinicia el terminal y verifica:

```powershell
test-by-ai --help
```

### Instalacion manual

```bash
git clone https://github.com/yourusername/test-by-ai.git
cd test-by-ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m test_by_ai.cli --help
```

## Uso basico

```bash
test-by-ai path/to/openapi.json
```

Esto ejecuta las suites por defecto contra el servidor definido en la especificacion.

## Casos de uso

- Smoke tests de APIs.
- Verificacion de contrato OpenAPI.
- Pruebas negativas y de errores.
- Comprobaciones rapidas antes de desplegar.
