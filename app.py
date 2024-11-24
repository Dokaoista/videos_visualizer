from flask import Flask, render_template, send_from_directory, url_for
import os
import subprocess
import unicodedata

app = Flask(__name__)

# Configuração das pastas
BASE_VIDEO_FOLDER = 'D:\outros\Cursos\Desec Pentest Mobile\kodak-pentest-mobile-desec - OInimigo.wtf'  # Substitua pelo caminho correto
THUMBNAIL_FOLDER = 'static/thumbnails'
ALLOWED_EXTENSIONS = {'mp4', 'webm', 'ogg', 'ts'}

if not os.path.exists(THUMBNAIL_FOLDER):
    os.makedirs(THUMBNAIL_FOLDER)

def allowed_file(filename):
    """Verifica se o arquivo possui uma extensão permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_videos_by_module():
    """Percorre as subpastas e organiza vídeos e arquivos de download por módulo."""
    modules = {}
    for root, _, files in os.walk(BASE_VIDEO_FOLDER):
        module_name = os.path.basename(root)
        videos = []
        downloads = []

        for file in sorted(files):
            if allowed_file(file):  # Verifica se é um vídeo
                relative_path = os.path.relpath(os.path.join(root, file), BASE_VIDEO_FOLDER)
                title = os.path.splitext(file)[0]
                videos.append({
                    'filename': relative_path.replace("\\", "/"),
                    'title': title,
                    'thumbnail': generate_thumbnail(os.path.join(root, file))
                })
            else:  # Caso não seja vídeo, adiciona como arquivo de download
                relative_path = os.path.relpath(os.path.join(root, file), BASE_VIDEO_FOLDER)
                downloads.append({
                    'filename': relative_path.replace("\\", "/"),
                    'title': file
                })

        if videos or downloads:
            modules[module_name] = {'videos': videos, 'downloads': downloads}

    # Ordena os módulos por nome, ignorando acentos
    modules_sorted = dict(sorted(modules.items(), key=lambda x: remove_accents(x[0].lower())))
    return modules_sorted

def remove_accents(input_str):
    """Remove acentos de uma string."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', input_str)
        if unicodedata.category(c) != 'Mn'
    )

def generate_thumbnail(video_path):
    thumbnail_filename = os.path.basename(video_path).rsplit('.', 1)[0] + '.png'
    thumbnail_path = os.path.join(THUMBNAIL_FOLDER, thumbnail_filename)
    
    if not os.path.exists(thumbnail_path):
        command = [
            'ffmpeg',
            '-i', video_path,
            '-ss', '00:00:02',
            '-vframes', '1',
            thumbnail_path
        ]
        subprocess.run(command, capture_output=True, text=True)
        
    return f'thumbnails/{thumbnail_filename}'

@app.route('/')
def index():
    """Renderiza a página inicial com vídeos organizados por módulo e links de download."""
    videos_by_module = get_videos_by_module()
    return render_template('index.html', videos_by_module=videos_by_module)

@app.route('/videos/<path:filename>')
def serve_video(filename):
    """Serve o vídeo solicitado."""
    return send_from_directory(BASE_VIDEO_FOLDER, filename)

@app.route('/download/<path:filename>')
def download_file(filename):
    """Serve o arquivo solicitado para download."""
    return send_from_directory(BASE_VIDEO_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
