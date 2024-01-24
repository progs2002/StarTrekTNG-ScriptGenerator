Fine-tuning gpt2 to generate random episode scripts from <b>Star Trek The Next Generation</b>

Dataset_source - https://www.st-minutiae.com/resources/scripts/#thenextgeneration

Raw text files cleaned using ```process_data.py``` and pushed to hub https://huggingface.co/datasets/progs2002/star-trek-tng-scripts

gpt2 is fine-tuned for 7500 steps on the mentioned dataset with a context window of 512 tokens.
model weights, training hyperparameters and metrics are pushed to hub https://huggingface.co/progs2002/star-trek-tng-script-generator

Model is deployed on Huggingface Spaces using streamlit for the front end. https://huggingface.co/spaces/progs2002/StarTrekTNG-EpisodeScriptGenerator