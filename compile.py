import subprocess
import fire
import os

ARTICLES_DIR = "articles"
DEV_MODE = True
FRONTEND_BASE_URL = (
    "http://localhost:3000" if DEV_MODE else "/foundation"
)  # foundation from ghpages repo


def exec_nbconvert(filename):
    subprocess.check_output(
        f"jupyter nbconvert --to html {filename} --HTMLExporter.theme=dark",
        shell=True,
    )


def inject(txt, at, content):
    return txt.replace(
        at,
        f"""{at}{content}""",
    )  # just add after the meta charset


def inject_header(html_file, to_inject):
    with open(html_file, "r") as f:
        txt = f.read()
        txt = inject(txt, """<meta charset="utf-8"/>""", to_inject)
        with open(html_file, "w") as outfile:
            outfile.write(txt)


# exec_nbconvert("articles/convolutions.ipynb")
# inject_header("articles/convolutions.html", '<link rel="stylesheet" href="custom.css">')
def files_with_ext(path="", ext="html"):
    return [i for i in os.listdir(path) if i.endswith("." + ext)]


def convert_all_ipynb_to_html(path):
    files = files_with_ext(path, "ipynb")
    for f in files:
        exec_nbconvert(os.path.join(path, f))


def add_custom_css_to_all_html(path):
    files = files_with_ext(path, "html")
    for f in files:
        inject_header(
            os.path.join(path, f), '<link rel="stylesheet" href="custom.css">'
        )


def add_to_toc(path, BASE, filename="index.html"):
    with open(filename, "r") as rf:
        # read and don't read last lists
        txt = "".join([t for t in rf.readlines() if "<li>" not in t])
        files = files_with_ext(path, "html")
        links = [os.path.join(BASE, path, f) for f in files]
        names = [f.replace(".html", "") for f in files]
        combined_html = ""
        for l, n in zip(links, names):
            combined_html += f'\n<li><a href="{l}">{n}</a></li>\n'
        txt = inject(txt, '<ul id="table-of-contents">', combined_html)

        with open(filename, "w") as wf:
            wf.write(txt)


def run(base=FRONTEND_BASE_URL):
    convert_all_ipynb_to_html(ARTICLES_DIR)
    add_custom_css_to_all_html(ARTICLES_DIR)
    add_to_toc(ARTICLES_DIR, base)


if __name__ == "__main__":
    fire.Fire(run)
