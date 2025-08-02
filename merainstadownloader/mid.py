import streamlit as st
import yt_dlp
import os
import tempfile

# 💫 Page setup
st.set_page_config(page_title="meraInstaDownloader 📥", page_icon="🎬")

# 🌈 Custom CSS for funky styling
st.markdown("""
    <style>
        .main {
            background-color: #fdf6f6;
            color: #333;
            font-family: 'Helvetica Neue', sans-serif;
        }

        h1 {
            color: #d62976;
            text-align: center;
            font-size: 3rem;
        }

        .stButton>button {
            background-color: #d62976;
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            font-size: 1.1rem;
            border-radius: 10px;
            transition: 0.3s;
        }

        .stButton>button:hover {
            background-color: #ad1457;
            transform: scale(1.03);
        }

        .css-1emrehy {
            font-size: 1.2rem;
            color: #444;
        }
    </style>
""", unsafe_allow_html=True)

# 🌟 Title
st.markdown("### 🎬 meraInstaDownloader")
st.markdown("#### *Download Instagram Reels in Style!* 💃🕺")

# 📥 Input
url = st.text_input("🔗 Paste Instagram Reel URL here", placeholder="https://www.instagram.com/reel/xyz...")

if st.button("✨ Download Now"):
    if url:
        with st.spinner("🔄 Fetching and downloading reel..."):
            try:
                # ⏳ Temp folder
                with tempfile.TemporaryDirectory() as tmpdir:
                    ydl_opts = {
                        'format': 'bv*+ba/best',
                        'merge_output_format': 'mp4',
                        'outtmpl': os.path.join(tmpdir, '%(title).100s.%(ext)s'),
                        'noplaylist': True,
                        'quiet': True,
                    }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        file_path = ydl.prepare_filename(info)
                        title = info.get("title", "reel")
                        description = info.get("description", "No caption available.")

                    with open(file_path, "rb") as f:
                        video_bytes = f.read()

                    st.success("✅ Reel downloaded successfully!")
                    st.video(video_bytes)

                    st.download_button(
                        label="⬇️ Click to Save Reel",
                        data=video_bytes,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4"
                    )

                    with st.expander("📝 View Caption"):
                        st.write(description)

            except Exception as e:
                st.error(f"❌ Oops! Something went wrong:\n\n{e}")
    else:
        st.warning("⚠️ Please paste a valid Instagram URL first.")
