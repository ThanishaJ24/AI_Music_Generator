from audiocraft.models import MusicGen

import streamlit as st
import os
import torch
import torchaudio
import numpy as np
import base64

@st.cache_resource
def load_model():
    model = MusicGen.get_pretrained("facebook/musicgen-small")
    return model


def generate_music_tensors(description,duration:int):
    print("Description: ",description)
    print("Durationn: ",duration)
    model=load_model()

    model.set_generation_params(
        use_sampling=True,
        top_k=250,
        duration=duration
    )

    output=model.generate(
        descriptions=[description],
        progress=True,
        return_tokens=True
    )

    return output[0]

def save_audio(sample: torch.Tensor):
    sample_rate = 32000,
    save_path = " audio_output/"

    assert samples.dim() == 2 or samples.dim() == 3

    samples=samples.detach().cpu()

    if samples.dim() == 2:
        sample=samples[None, ... ]

    for idx, audio in enumerate(samples):
        audio_path=os.path.join(save_path, f"audio_{idx}.wav")
        torchaudio.save(audio_path,audio,sample_rate)


def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file,'rb') as f:
        data = f.read()

    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}"> Download {file_label}</a>'

    return href


st.set_page_config(
    page_icon="	:musical_note:",
    page_title="Music Generator"
)

def main():
    st.title("Text to music Generator")

    with st.expander("See Explanation"):
        st.write("This is a music generator app built using the following  Meta's Audiocraft library Music Gen model.")

    text_area= st.text_area("Enter yor description....")
    time_slider = st.slider("Select time duration(int seconds)",2,20,5)

    if text_area and time_slider:
        st.json(
            {
                "Your Description":text_area,
                "Selected time duration":time_slider
            }
        )

    st.subheader("Generated Music")

    music_tensor = generate_music_tensors(text_area,time_slider)

    print("Music Tensors: ",music_tensor)

    save_music_file=save_music_file(music_tensor)

    audio_filepath = 'audio_output/audio_0.wav'

    audio_file = open(audio_filepath,'rb')
    audio_bytes=audio_file.read()

    st.audio(audio_bytes)
    st.markdown(get_binary_file_downloader_html(audio_filepath,'Audio'),unsafe_allow_html=True)

if __name__ == "__main__":
    main()



