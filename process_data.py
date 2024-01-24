import re 
from glob import glob
import tqdm

def clean_text(text):
    #TODO:can be written in a better way

    #remove credits from the script
    idx1 = list(re.finditer(r'FADE IN:', text))[0].span()[1]
    text = text[idx1:]

    #remove cinematic info
    cap2 = re.compile(r'^\d.*\n', re.MULTILINE)
    cap3 = re.compile(r'^.*STAR TREK.*$', re.MULTILINE)
    text = cap2.sub('',text)
    text = cap3.sub('',text)

    #CHARACTER_NAME -> CHARACTER_NAME:
    cap1 = re.compile(r'^\t{5}([^\t\n]+)$', re.MULTILINE)
    text = cap1.sub(r'\1:',text)

    #remove dialogue cues 
    cap4 =  re.compile(r'^\t{4}\(.*\n*.*\)\n', re.MULTILINE)
    text = cap4.sub('',text)

    #remove extra lines
    cap5 = re.compile(r'^.*FADE IN:.*\n', re.MULTILINE)
    cap6 = re.compile(r'^.*FADE OUT.*\n', re.MULTILINE)
    cap7 = re.compile(r'^.*PART.*$', re.MULTILINE)
    cap8 = re.compile(r'^.*ACT.*$', re.MULTILINE)
    cap9 = re.compile(r'^\s*\(\w+\).*$', re.MULTILINE)
    cap10 = re.compile(r'^.*TEASER.*$', re.MULTILINE)
    cap11 = re.compile(r'^thru.*$', re.MULTILINE)
    cap12 = re.compile(r'^\t{9}CUT.*$', re.MULTILINE)

    #remove occurances of INTERCUT
    cap15 = re.compile(r'^.*INTERCUT.*$', re.MULTILINE)
    text = cap15.sub('',text)

    #remove occurances of 'GO TO:'
    cap16 = re.compile(r'^.*GO TO:.*$', re.MULTILINE)
    text = cap16.sub('',text)

    text = cap5.sub('',text)
    text = cap6.sub('',text)
    text = cap7.sub('',text)
    text = cap8.sub('',text)
    text = cap9.sub('',text)
    text = cap10.sub('',text)
    text = cap11.sub('',text)
    text = cap12.sub('',text)

    text = text.strip()

    #remove null characters 
    cap13 = re.compile(r'^\s*\x00.*$', re.MULTILINE)
    text = cap13.sub('',text)

    #remove end of scene texts
    cap14 = re.compile(r'^\s*(THE )?END[^AR][^:]*$', re.MULTILINE)
    text = cap14.sub('',text)

    #TODO:remove "CUT TO:"
    cap16 = re.compile(r'^\s*CUT TO:.*$', re.MULTILINE)
    text = cap16.sub('',text)

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
    
    #remove uncessary dialogue from master.txt
    final_cap = re.compile(r'^[A-Z]+:\s*$\n', re.MULTILINE)

    for idx, raw_file in enumerate(tqdm.tqdm(raw_files)):
        try:
            text = open(raw_file, encoding='utf-8').read()
            text = clean_text(text)
            text = final_cap.sub('',text)

            with open(f'{clean_filepath}/{idx}.txt', 'w') as f:
                f.write(text)

        except UnicodeDecodeError:
            print(idx)
            continue

def create_master_file(clean_filepath):
    clean_files = glob(f'{clean_filepath}/*.txt')
    with open('./master.txt', 'w') as master_f:
        for filename in clean_files:
            f = open(filename, encoding='utf-8')
            master_f.write(f.read()+'\n')
            f.close()

if __name__ == '__main__':
    process_files(
        raw_filepath='dataset/rawtext',
        clean_filepath='dataset/processed'
    )
    create_master_file(clean_filepath='dataset/processed')
