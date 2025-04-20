import streamlit as st
import tempfile
import os
import time

from predictor import preprocess_video, predict_word

def main():
    st.title("Video Upload for Model Processing")
    
    # File uploader for video
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])
    
    # Placeholder for loading animation
    loading_placeholder = st.empty()
    
    if uploaded_file is not None:
        # Show loading animation
        with loading_placeholder:
            with st.spinner("Processing..."):
                time.sleep(2)  # Simulating processing time
        
        # Save the uploaded video to a temporary file
        temp_dir = tempfile.mkdtemp()
        video_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())
        
        # Preprocess and predict
        st.spinner("Running lip-reading model...")
        preprocessed_input = preprocess_video(video_path)
        predicted_word = predict_word(preprocessed_input)

        # st.success(f"Predicted Word: **{predicted_word}**")
        
        # Display video
        st.video(video_path)
        
        # Remove loading placeholder and show output
        loading_placeholder.empty()
        
        # Display transcription text under video
        st.markdown("### Transcription:")
        st.markdown(f"## {predicted_word}")


if __name__ == "__main__":
    main()
