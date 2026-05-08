import streamlit as st

from logos_core import build_locked_pptx, build_output_name, is_valid_license


APP_NAME = "Logos"
BRAND_NAME = "Curious Curriculum Club"
APP_VERSION = "v1.2 - International Edition"


st.set_page_config(page_title=f"{APP_NAME} | {BRAND_NAME}", page_icon="L", layout="centered")

st.markdown(
    """
    <style>
      .stApp {
        background:
          radial-gradient(circle at 50% 8%, rgba(255, 255, 255, 0.22), transparent 15rem),
          linear-gradient(135deg, #111111 0%, #1a1a1a 48%, #0a0a0a 100%);
        color: #f7f2e8;
      }

      .block-container {
        max-width: 760px;
        padding-top: 4.2rem;
        padding-bottom: 2.5rem;
      }

      [data-testid="stHeader"],
      [data-testid="stToolbar"],
      [data-testid="stDecoration"] {
        display: none;
      }

      .logos-shell {
        border: 1px solid rgba(255, 255, 255, 0.12);
        background: rgba(0, 0, 0, 0.38);
        padding: 2.5rem 2rem 1.4rem;
        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.34);
      }

      .logos-kicker {
        color: #b9b4aa;
        font-size: 0.76rem;
        letter-spacing: 0;
        text-align: center;
        margin-bottom: 1.25rem;
      }

      .logos-title {
        color: #ffffff;
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 900;
        line-height: 1;
        text-align: center;
        margin: 0;
        text-transform: uppercase;
      }

      .logos-tagline {
        color: #f2eadf;
        font-size: 1rem;
        font-style: italic;
        font-weight: 700;
        text-align: center;
        margin: 1rem 0 2rem;
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
        margin-top: 1.8rem;
      }
    </style>
    <div class="logos-shell">
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

uploaded_files = st.file_uploader(
    "Select files",
    type=["png", "jpg", "jpeg", "pdf"],
    accept_multiple_files=True,
    disabled=not license_ok,
)

if not license_ok:
    st.info("Enter a valid license key to unlock processing.")

if license_ok and uploaded_files:
    output_name = build_output_name(uploaded_files)
    st.caption(f"Output: {output_name}")

    if st.button("Process files", type="primary"):
        try:
            with st.spinner("Building your locked PowerPoint..."):
                pptx_bytes = build_locked_pptx(uploaded_files)

            st.success("Done. Your PowerPoint is ready.")
            st.download_button(
                "Download PPTX",
                data=pptx_bytes,
                file_name=output_name,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
        except Exception as error:
            st.error(f"Processing failed: {error}")

st.markdown(
    f"""
      <div class="logos-footer">
        <span>{APP_VERSION}</span>
        <span>Help & Feedback</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
