import gradio as gr
import os
import tempfile
from openai import OpenAI


def tts(text, model, voice, api_key):
    if api_key == '':
        raise gr.Error('Please enter your OpenAI API Key')
    else:
        try:
            client = OpenAI(api_key=api_key)

            response = client.audio.speech.create(
                model=model, # "tts-1","tts-1-hd"
                voice=voice, # 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'
                input=text,
            )

        except Exception as error:
            # Handle any exception that occurs
            raise gr.Error("An error occurred while generating speech. Please check your API key and try again.")
            print(str(error))

    # Create a temp file to save the audio
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_file.write(response.content)

    # Get the file path of the temp file
    temp_file_path = temp_file.name

    return temp_file_path


with gr.Blocks() as demo:
    gr.Markdown("# <center> OpenAI Text-To-Speech API with Gradio </center>")
    #gr.HTML("You can also access the Streaming demo for OpenAI TTS by clicking this <a href='https://huggingface.co/spaces/ysharma/OpenAI_TTS_Streaming'>Gradio demo link</a>")
    with gr.Row(variant='panel'):
      api_key = gr.Textbox(type='password', label='OpenAI API Key', placeholder='Enter your API key to access the TTS demo')
      model = gr.Dropdown(choices=['tts-1','tts-1-hd'], label='Model', value='tts-1')
      voice = gr.Dropdown(choices=['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'], label='Voice Options', value='alloy')

    text = gr.Textbox(label="Input text", placeholder="Enter your text and then click on the 'Text-To-Speech' button, or simply press the Enter key.")
    btn = gr.Button("Text-To-Speech")
    output_audio = gr.Audio(label="Speech Output")
    
    text.submit(fn=tts, inputs=[text, model, voice, api_key], outputs=output_audio, api_name="tts_enter_key", concurrency_limit=None)
    btn.click(fn=tts, inputs=[text, model, voice, api_key], outputs=output_audio, api_name="tts_button", concurrency_limit=None)

demo.launch()