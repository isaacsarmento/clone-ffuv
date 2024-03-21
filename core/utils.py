def parser_wordlist(filepath: str):
    wordlists = []
    try:
        with open(filepath, 'r') as f:
            for chunk in read_chunks(f):
                for x in chunk.split():
                    wordlists.append(x)
    except Exception:
        pass
    return wordlists

#ler 2048 bytes
def read_chunks(file_obj, chunk_size=2048):
    while True:
        data = file_obj.read(chunk_size)
        if not data:
            break
        yield data