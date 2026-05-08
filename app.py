import streamlit as st

from logos_core import build_locked_pptx, is_valid_license


APP_NAME = "Logos"
BRAND_NAME = "Curious Curriculum Club"


st.set_page_config(page_title=f"{APP_NAME} | {BRAND_NAME}", page_icon="L", layout="centered")

st.title(APP_NAME)
st.caption(f"{BRAND_NAME} - private browser-side material processing")

st.markdown(
    """
Upload PNG, JPG, JPEG, or PDF files. Logos will sort them naturally by filename,
turn each image or PDF page into a locked PowerPoint background, then give you a
downloadable `.pptx`.
"""
)

with st.expander("Privacy note", expanded=True):
    st.write(
        "In the stlite web build, processing runs in your browser. Your files stay on "
        "your device and are not uploaded to a Logos server."
    )

license_key = st.text_input("License Key", type="password", placeholder="Enter your Logos key")
license_ok = is_valid_license(license_key)

if license_key and license_ok:
    st.success("License accepted.")
elif license_key:
    st.error("License key not recognized.")

uploaded_files = st.file_uploader(
    "Select materials",
    type=["png", "jpg", "jpeg", "pdf"],
    accept_multiple_files=True,
    disabled=not license_ok,
)

output_name = st.text_input(
    "Output filename",
    value="logos-result.pptx",
    disabled=not license_ok,
)

if not license_ok:
    st.info("Enter a valid license key to unlock processing.")

if license_ok and uploaded_files:
    if st.button("Process files", type="primary"):
        try:
            with st.spinner("Building your locked PowerPoint..."):
                pptx_bytes = build_locked_pptx(uploaded_files)

            safe_output_name = output_name.strip() or "logos-result.pptx"
            if not safe_output_name.lower().endswith(".pptx"):
                safe_output_name = f"{safe_output_name}.pptx"

            st.success("Done. Your PowerPoint is ready.")
            st.download_button(
                "Download PPTX",
                data=pptx_bytes,
                file_name=safe_output_name,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
        except Exception as error:
            st.error(f"Processing failed: {error}")
