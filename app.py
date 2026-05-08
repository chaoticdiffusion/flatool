import streamlit as st

from flatool_core import build_locked_pptx, build_output_name, build_pdf_batch_zip, is_valid_license


APP_NAME = "Flatool"
BRAND_NAME = "Curious Curriculum Club"


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

      .stHeading a,
      [data-testid="stHeadingWithActionElements"] a {
        display: none;
      }

      .flatool-kicker {
        color: #b9b4aa;
        font-size: 0.76rem;
        letter-spacing: 0;
        margin-bottom: 0.75rem;
      }

      .flatool-title {
        color: #ffffff;
        font-size: clamp(2.1rem, 5vw, 3.7rem);
        font-weight: 900;
        line-height: 1;
        margin: 0;
        text-transform: uppercase;
      }

      .flatool-tagline {
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

      [data-testid="stFormSubmitButton"] button {
        background: transparent;
        border: 1px solid rgba(255, 255, 255, 0.22);
        color: #ffffff;
      }

      [data-testid="stFormSubmitButton"] button:hover {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.42);
        color: #ffffff;
      }

      [data-testid="stFormSubmitButton"] button p {
        font-size: 0;
      }

      [data-testid="stFormSubmitButton"] button p::after {
        content: "\\1F511";
        font-size: 1.2rem;
        line-height: 1;
      }

      [data-testid="InputInstructions"] {
        display: none;
      }

      [data-testid="stForm"] {
        border: 0;
        padding: 0;
      }

      .flatool-section {
        border-top: 1px solid rgba(255, 255, 255, 0.18);
        margin-top: 3rem;
        padding-top: 2rem;
      }

      .flatool-section h2 {
        color: #ffffff;
        font-size: 1.75rem;
        margin: 0 0 1rem;
      }

      .flatool-steps {
        color: #e7e1d8;
        line-height: 1.7;
        margin-bottom: 1.5rem;
      }

      .flatool-steps li {
        margin-bottom: 0.5rem;
      }

      [data-testid="stExpander"] {
        background: #181818;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 2px;
      }

      .flatool-app-note {
        border-top: 1px solid rgba(255, 255, 255, 0.18);
        display: flex;
        flex-wrap: wrap;
        gap: 0.7rem 1.3rem;
        justify-content: space-between;
        color: #d8d0c6;
        margin-top: 2.5rem;
        padding-top: 1rem;
        font-size: 0.86rem;
      }

      .flatool-app-note strong {
        color: #ffffff;
      }
    </style>
    <div class="flatool-kicker">Flatool by Curious Curriculum Club</div>
    <h1 class="flatool-title">REST MORE, TEACH BETTER</h1>
    <div class="flatool-tagline">you're not lazy, just efficiency</div>
    """,
    unsafe_allow_html=True,
)

with st.form("license_form", border=False):
    key_col, submit_col = st.columns([3, 1])
    with key_col:
        license_key = st.text_input(
            "License Key",
            placeholder="Enter your Flatool key",
            label_visibility="collapsed",
        )
    with submit_col:
        apply_key = st.form_submit_button("Key", type="primary", use_container_width=True)

license_ok = is_valid_license(license_key)

if apply_key and license_ok:
    st.success("License accepted.")
elif apply_key and license_key:
    st.error("License key not recognized.")

mode = st.radio(
    "Mode",
    ["Multi PNG/JPG/PDF to one PPTX", "Batch PDF to multiple PPTX"],
    disabled=not license_ok,
)

is_pdf_batch = mode == "Batch PDF to multiple PPTX"
allowed_types = ["pdf"] if is_pdf_batch else ["png", "jpg", "jpeg", "pdf"]
upload_label = "Select PDF files" if is_pdf_batch else "Select PNG/JPG/PDF files"

if license_ok and not is_pdf_batch:
    st.caption("This mode combines every uploaded image or PDF page into one PPTX file.")
elif license_ok:
    st.caption("This mode creates one PPTX for each uploaded PDF, then downloads them together as a ZIP.")

uploaded_files = st.file_uploader(
    upload_label,
    type=allowed_types,
    accept_multiple_files=True,
    disabled=not license_ok,
)

if not license_ok:
    st.info("Enter a valid license key to unlock processing.")

if license_ok and uploaded_files:
    output_name = "Flatool PDF Batch RESULT.zip" if is_pdf_batch else build_output_name(uploaded_files)
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
    """
    <div class="flatool-section">
      <h2>How to use</h2>
      <ol class="flatool-steps">
        <li>Enter your Flatool license key, then click <strong>Apply Key</strong>.</li>
        <li>Choose a mode: combine PNG/JPG/PDF files into one PPTX, or process PDFs in batch.</li>
        <li>Upload your files. Flatool sorts filenames naturally, so 2 comes before 10.</li>
        <li>Click <strong>Process files</strong>, then download the result.</li>
      </ol>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("## FAQ")

with st.expander("Is my material kept private?", expanded=True):
    st.write(
        "Yes. Your files are processed on your own device and are not uploaded to a "
        "Flatool server."
    )

with st.expander("Which mode should I use?"):
    st.write(
        "Use Multi PNG/JPG/PDF to one PPTX when you want everything combined into one "
        "PowerPoint file. Use Batch PDF to multiple PPTX when each PDF should become "
        "its own PowerPoint file."
    )

with st.expander("Why does the first load take a while?"):
    st.write(
        "The first visit prepares the tool in your browser. After that, your browser may "
        "remember parts of it, so later visits can feel faster."
    )

with st.expander("Will the flattened file look different from the original?"):
    st.write(
        "Flatool turns each image or PDF page into a slide background. The result is meant "
        "to preserve the visual layout while making the slide content non-editable."
    )

with st.expander("What file formats are supported?"):
    st.write(
        "The one-file mode supports PNG, JPG, JPEG, and PDF. The batch mode supports PDF files."
    )

with st.expander("What should I do if a large PDF is slow?"):
    st.write(
        "Because processing happens on your device, very large PDFs depend on your browser, "
        "RAM, and phone or laptop performance. Try processing fewer files at once."
    )

st.markdown(
    """
    <div class="flatool-app-note">
      <span><strong>Windows and Mac app are available.</strong></span>
      <span>More fast, more stable, more rest.</span>
      <span>Contact: rheachaoticmateria@gmail.com</span>
    </div>
    """,
    unsafe_allow_html=True,
)
