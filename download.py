import os
import tqdm
import requests
import re

def download(tag, sequences, path):
    print("")
    print(f"Downloading {tag} dataset with {len(sequences)} files...")
    if not os.path.exists(path):
        os.makedirs(path)
    for sequence in tqdm.tqdm(sequences):
        filename = os.path.basename(sequence)
        if not os.path.exists(os.path.join(path, filename)):
            try:
                download_file(sequence, path)
            except Exception as e:
                error = str(e).split("\n")[-1]
                print(error)
        else:
            print(f"File {filename} already exists, skipping...")

def download_file(url, path):
    local_filename = url.split('/')[-1]
    local_filename = os.path.join(path, local_filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)

    return local_filename

def unzip_all(base_path, delete_zip=True):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".zip"):
                print(f"Unzipping {file}...")
                os.system(f"unzip {os.path.join(root, file)} -d {root}")
                if delete_zip:
                    print(f"Removing {file}...")
                    os.system(f"rm {os.path.join(root, file)}")

if __name__ == "__main__":
    #baseurl = "https://web.archive.org/web/20220210102816/http://cvlab.hanyang.ac.kr/tracker_benchmark/"
    baseurl = "https://web.archive.org/web/http://cvlab.hanyang.ac.kr/tracker_benchmark/"
    OTB50_seq_names = []
    OTB100_seq_names = []

    seq_files = []
    with open("files.txt", "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            url = baseurl + line

            if i < 49:
                OTB50_seq_names.append(url)
                OTB100_seq_names.append(url)
            else:
                OTB100_seq_names.append(url)

    download("OTB50", OTB50_seq_names, "./OTB50")
    download("OTB100", OTB100_seq_names, "./OTB100")

    # If you want to automatically unzip all files, will not delete zip files
    #unzip_all("./OTB50", delete_zip=False)  
    #unzip_all("./OTB100", delete_zip=False) 







