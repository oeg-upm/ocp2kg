from evol_kg import main as evol_kg
import argparse
import gradio as gr
import os
import uuid
import tempfile

# Función que devuelve el nombre del archivo
def update_filename(file):
    message= "No file uploaded"
    if file:
        message= f"Uploaded file: **{file.name.split('/')[-1]}**"
    return message

# Function to allow Gradio to overwrite the args values
def gradio_interface(changes_kg_input, old_mapping_input, ontology_input, yarrrml_toggle):
    # Create the args object manually
    gr.Info("Starting process, this may take a while.")

    if changes_kg_input is None or old_mapping_input is None:
        raise gr.Error("Both KG and mappings should be provided.")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ttl", dir=os.path.dirname(changes_kg_input.name)) as temp_file:
        new_mappings_path = temp_file.name

    ontology_input_name = None
    if ontology_input is not None:
        ontology_input_name= ontology_input.name
    
    args = argparse.Namespace(
        changes_kg_path=changes_kg_input.name,
        old_mapping_path=old_mapping_input.name,
        ontology_path=ontology_input_name,
        new_mappings_path=new_mappings_path,
        yarrrml=yarrrml_toggle
    )

    try:
        # Run the evol_kg function
        evol_kg(args)
        gr.Info("Processing completed successfully. File is ready for download.")
    except Exception as e:
        raise gr.Error(f"Error during processing: {str(e)}")

    # Return the status message and the path to the generated file
    return new_mappings_path

def define_demo():
    # Create the Gradio interface
    with gr.Blocks(css="""
        .file-box-left {
            background-color: #e0f7fa;  /* Light cyan background for the first box */
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .file-box-middle {
            background-color: #d3d3d3;  /* Grey background for the middle box */
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .file-box-right {
            background-color: #ffcccb;  /* Light red background for the third box */
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .column-markdown {
            text-align: center;  /* Center align Markdown text */
        }
    """) as demo:
        gr.Markdown("## Script for processing RML mappings and ontologies")

        with gr.Row():
            with gr.Column(elem_classes=["file-box-left"]):
                gr.Markdown("### Upload the Knowledge Graph", elem_classes=["column-markdown"])
                changes_kg_input = gr.File(label="Knowledge Graph")
                changes_kg_name = gr.Markdown(value="", label="File Name")
            with gr.Column(elem_classes=["file-box-middle"]):
                gr.Markdown("### Upload the old version of the relational mapping in RML", elem_classes=["column-markdown"])
                old_mapping_input = gr.File(label="Relational Mapping")
                old_mapping_name = gr.Markdown(value="", label="File Name")
            with gr.Column(elem_classes=["file-box-right"]):
                gr.Markdown("### Upload the Ontology (optional)", elem_classes=["column-markdown"])
                ontology_input = gr.File(label="Ontology")
                ontology_name = gr.Markdown(value="", label="File Name")

        yarrrml_toggle = gr.Checkbox(label="Convert to YARRRML", value=False)

        # output = gr.Textbox(label="Output", lines=10, interactive=False)
        process_button = gr.Button("Process")
        download_button = gr.File(label="Download Result", visible=False)

        # Link the Gradio interface to the main function
        process_button.click(
            gradio_interface,
            inputs=[changes_kg_input, old_mapping_input, ontology_input, yarrrml_toggle],
            outputs=[download_button]
        )

        # Actualizar los nombres de los archivos debajo de cada campo de subida
        changes_kg_input.change(update_filename, inputs=[changes_kg_input], outputs=[changes_kg_name])
        old_mapping_input.change(update_filename, inputs=[old_mapping_input], outputs=[old_mapping_name])
        ontology_input.change(update_filename, inputs=[ontology_input], outputs=[ontology_name])

        # Update the visibility of the download button after the process
        process_button.click(
            lambda: gr.update(visible=True),  # Make the download button visible after processing
            inputs=[],
            outputs=[download_button]
        )
    return demo


# Run the interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Demo')
    parser.add_argument('-p','--port', help='Port in which the demo will be available.', required=False, default=5959)
    parser.add_argument('-d','--data_volume', help='Path were all data will be stored.', required=False, default=".")
    parser.add_argument('-r','--root_path', help='Path of the url where the app is running, default in main url.', required=False, default=None)
    args = parser.parse_args()

    if "SD_PORT" in os.environ:
        SD_PORT= int(os.environ['SD_PORT']) #Port for deploying gradio
    else:
        SD_PORT= args.port

    if "DATA_VOLUME" in os.environ:
        DATA_VOLUME= os.environ['DATA_VOLUME']
    else:
        DATA_VOLUME= args.data_volume

    if "ROOT_PATH" in os.environ:
        ROOT_PATH= os.environ['ROOT_PATH']
    else:
        ROOT_PATH= args.root_path

    demo= define_demo()

    demo.launch(server_port=SD_PORT, share=False, server_name="0.0.0.0", root_path=ROOT_PATH)

# ontology_path: /home/ibai/OEG/ocp2kg/examples/ppds/epo-ontology/ePO_3.1.ttl
# changes_kg_path: /home/ibai/OEG/ocp2kg/examples/ppds/input_data/epo-changes_data/change_data_3.1.0.ttl
# old_mapping_path: /home/ibai/OEG/ocp2kg/examples/ppds/mappings/AUT_full_mapping.rml.ttl