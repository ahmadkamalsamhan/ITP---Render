import gradio as gr
import pandas as pd
from rapidfuzz import process
import re

# ------------------------------
# Matching Function
# ------------------------------
def match_files(file1, file2, ignore_special_chars=True, min_score=80):
    df1 = pd.read_excel(file1.name)
    df2 = pd.read_excel(file2.name)

    col1 = df1.columns[0]
    col2 = df2.columns[0]

    # Normalize strings
    def normalize(s):
        s = str(s).lower()
        if ignore_special_chars:
            s = re.sub(r'[^a-z0-9\s]', '', s)
        return s.strip()

    df1['norm'] = df1[col1].apply(normalize)
    df2['norm'] = df2[col2].apply(normalize)

    results = []
    for val2 in df2['norm']:
        best_match, score, _ = process.extractOne(val2, df1['norm'])
        if score >= min_score:
            results.append((val2, best_match, score))
        else:
            results.append((val2, None, score))

    return pd.DataFrame(results, columns=[col2, f'Best Match ({col1})', 'Score'])

# ------------------------------
# Gradio Interface
# ------------------------------
iface = gr.Interface(
    fn=match_files,
    inputs=[
        gr.File(label="Excel File 1"),
        gr.File(label="Excel File 2"),
        gr.Checkbox(label="Ignore Special Characters", value=True),
        gr.Slider(minimum=0, maximum=100, step=1, value=80, label="Minimum Match Score (%)")
    ],
    outputs=gr.DataFrame(label="Matching Results"),
    live=False
)

iface.launch(server_name="0.0.0.0", server_port=8080, share=True)
