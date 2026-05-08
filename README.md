# Flatool

Browser-side version of Flatool for Curious Curriculum Club.

Flatool converts uploaded PNG/JPG/PDF files into PowerPoint files where each page is flattened as a non-editable slide background. Files are processed locally on the user's device instead of uploaded to a server.

The download name is generated automatically from the first naturally sorted upload, plus `RESULT`.

## Modes

- `Multi PNG/JPG/PDF to one PPTX`: combine many images or PDF pages into one PowerPoint.
- `Batch PDF to multiple PPTX`: convert each uploaded PDF into its own PowerPoint and download all results as a ZIP.

## Local preview

```powershell
.\.venv\Scripts\python.exe -m http.server 8080
```

Then open:

```text
http://localhost:8080
```

## Test license keys

```text
FLATOOL-BETA-2026
CCC-FOUNDER-2026
```

The license gate is intentionally lightweight because this version is fully client-side. It is useful for normal buyer friction, but it is not strong DRM.

## Core files

- `index.html` loads the browser app.
- `app.py` contains the Flatool UI and PPTX generation logic.
- `flatool_core.py` contains the reusable PDF/image-to-PPTX logic.
- `logo.png` is used as the startup loading mark when present.
