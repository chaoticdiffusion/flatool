# Logos

Browser-side Streamlit/stlite version of Logos for Curious Curriculum Club.

Logos converts uploaded PNG/JPG files or PDF files into PowerPoint files where each page is flattened as a non-editable slide background. The static web build runs in the user's browser through stlite/Pyodide, so files are processed locally instead of uploaded to a server.

The download name is generated automatically from the first naturally sorted upload, plus `RESULT`.

## Modes

- `Multi PNG/JPG to one PPTX`: combine many images into one PowerPoint.
- `Batch PDF to multiple PPTX`: convert each uploaded PDF into its own PowerPoint and download all results as a ZIP.

## Local preview

```powershell
.\.venv\Scripts\python.exe -m http.server 8080
```

Then open:

```text
http://localhost:8080
```

For the normal Streamlit development server:

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

## Test license keys

```text
LOGOS-BETA-2026
CCC-FOUNDER-2026
```

The license gate is intentionally lightweight because this version is fully client-side. It is useful for normal buyer friction, but it is not strong DRM.

## Core files

- `index.html` loads stlite from CDN and mounts the Streamlit app.
- `app.py` contains the Logos UI and PPTX generation logic.
- `logos_core.py` contains the reusable PDF/image-to-PPTX logic.
