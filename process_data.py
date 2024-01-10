import re 
from glob import glob
import tqdm

def clean_text(text):
    #remove credits from the script
    idx1 = list(re.finditer(r'FADE IN:', text))[0].span()[1]
    text = text[idx1:]

    #CHARACTER_NAME -> CHARACTER_NAME:
    cap1 = re.compile(r'^\t{5}([^\t]+)$', re.MULTILINE)
    text = cap1.sub(r'\1:',text)

    #remove cinematic info
    cap2 = re.compile(r'^\d.*\n\n', re.MULTILINE)
    text = cap2.sub('',text)

    #remove dialogue cues 
    cap3 =  re.compile(r'^\t{4}\(.*\n*.*\)\n', re.MULTILINE)
    text = cap3.sub('',text)

    #remove extra lines
    cap4 = re.compile(r'^.*FADE IN:.*\n', re.MULTILINE)
    cap5 = re.compile(r'^.*FADE OUT.*\n', re.MULTILINE)
    cap6 = re.compile(r'^.*PART.*$', re.MULTILINE)

    text = cap4.sub('',text)
    text = cap5.sub('',text)
    text = cap6.sub('',text)

    text = text.strip()
    
    #remove unecessary newlines 
    out_text = []
    buffer = []

    for line in text.split('\n'):
        if line != '':
            buffer.append(line.strip())
        else:
            out_text.append(' '.join(buffer))
            buffer = []

    #remove empty lines
    out_text = filter(lambda x: x, out_text)
    out_text = '\n'.join(out_text)

    return out_text

def process_files(raw_filepath, clean_filepath):
    raw_files = sorted(glob(f'{raw_filepath}/*.txt'))

    for idx, raw_file in enumerate(tqdm.tqdm(raw_files)):
        try:
            text = open(raw_file, encoding='utf-8').read()
            text = clean_text(text)

            with open(f'{clean_filepath}/{idx}.txt', 'w') as f:
                f.write(text)

        except(UnicodeDecodeError):
            continue
        


if __name__ == '__main__':
    process_files(
        raw_filepath='dataset/rawtext',
        clean_filepath='dataset/processed'
    )
