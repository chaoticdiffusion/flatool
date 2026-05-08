import streamlit as st

from logos_core import build_locked_pptx, build_output_name, build_pdf_batch_zip, is_valid_license


APP_NAME = "Logos"
BRAND_NAME = "Curious Curriculum Club"
APP_VERSION = "v1.2 - International Edition"


st.set_page_config(page_title=f"{APP_NAME} | {BRAND_NAME}", page_icon="L", layout="centered")

st.markdown(
    """
    <style>
      .stApp {
        background: #111111;
        color: #f7f2e8;
      }

      .block-container {
        max-width: 720px;
        padding-top: 3.5rem;
        padding-bottom: 2.5rem;
      }

      [data-testid="stHeader"],
      [data-testid="stToolbar"],
      [data-testid="stDecoration"] {
        display: none;
      }

      .logos-kicker {
        color: #b9b4aa;
        font-size: 0.76rem;
        letter-spacing: 0;
        margin-bottom: 0.75rem;
      }

      .logos-title {
        color: #ffffff;
        font-size: clamp(2.1rem, 5vw, 3.7rem);
        font-weight: 900;
        line-height: 1;
        margin: 0;
        text-transform: uppercase;
      }

      .logos-tagline {
        color: #f2eadf;
        font-size: 1rem;
        font-style: italic;
        font-weight: 700;
        margin: 0.9rem 0 2.2rem;
      }

      .stButton > button,
      .stDownloadButton > button {
        background: #f5efe5;
        color: #111111;
        border: 0;
        border-radius: 2px;
        font-weight: 800;
        min-height: 3.2rem;
        text-transform: uppercase;
      }

      .stButton > button:hover,
      .stDownloadButton > button:hover {
        background: #ffffff;
        color: #111111;
        border: 0;
      }

      .logos-footer {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        color: #9d988f;
        font-size: 0.74rem;
        margin-top: 2rem;
      }
    </style>
    <div class="logos-kicker">LOGOS INTERNATIONAL EDITION</div>
    <h1 class="logos-title">REST MORE, TEACH BETTER</h1>
    <div class="logos-tagline">you're not lazy, just efficiency</div>
    """,
    unsafe_allow_html=True,
)

license_key = st.text_input("License Key", type="password", placeholder="Enter your Logos key")
license_ok = is_valid_license(license_key)

if license_key and license_ok:
    st.success("License accepted.")
elif license_key:
    st.error("License key not recognized.")

mode = st.radio(
    "Mode",
    ["Multi PNG/JPG to one PPTX", "Batch PDF to multiple PPTX"],
    disabled=not license_ok,
)

is_pdf_batch = mode == "Batch PDF to multiple PPTX"
allowed_types = ["pdf"] if is_pdf_batch else ["png", "jpg", "jpeg"]
upload_label = "Select PDF files" if is_pdf_batch else "Select PNG/JPG files"

uploaded_files = st.file_uploader(
    upload_label,
    type=allowed_types,
    accept_multiple_files=True,
    disabled=not license_ok,
)

if not license_ok:
    st.info("Enter a valid license key to unlock processing.")

if license_ok and uploaded_files:
    output_name = "Logos PDF Batch RESULT.zip" if is_pdf_batch else build_output_name(uploaded_files)
    st.caption(f"Output: {output_name}")

    if st.button("Process files", type="primary"):
        try:
            if is_pdf_batch:
                with st.spinner("Building one PowerPoint per PDF..."):
                    result_bytes = build_pdf_batch_zip(uploaded_files)
                download_label = "Download ZIP"
                mime_type = "application/zip"
            else:
                with st.spinner("Building your locked PowerPoint..."):
                    result_bytes = build_locked_pptx(uploaded_files)
                download_label = "Download PPTX"
                mime_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

            st.success("Done. Your file is ready.")
            st.download_button(
                download_label,
                data=result_bytes,
                file_name=output_name,
                mime=mime_type,
            )
        except Exception as error:
            st.error(f"Processing failed: {error}")

st.markdown(
    f"""
      <div class="logos-footer">
        <span>{APP_VERSION}</span>
        <span>Help & Feedback</span>
      </div>
    """,
    unsafe_allow_html=True,
)
