from flask import Flask, render_template, request, flash, send_file, session, redirect, url_for
from ssl_script import download_video
import os
import tempfile

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        tmpdirname = tempfile.mkdtemp()
        download_video(url, save_path=tmpdirname)
        # Find the first video file in the temp directory
        video_file = None
        for fname in os.listdir(tmpdirname):
            if fname.lower().endswith(('.mp4', '.webm', '.mkv', '.mov', '.avi', '.flv')):
                video_file = os.path.join(tmpdirname, fname)
                break
        if video_file and os.path.exists(video_file):
            session['temp_video_path'] = video_file
            session['temp_video_name'] = os.path.basename(video_file)
            flash('Download completed!', 'success')
            return redirect(url_for('preview'))
        else:
            flash('Download failed. Please check the URL and try again.', 'danger')
    return render_template('index.html')

@app.route('/preview')
def preview():
    file_path = session.get('temp_video_path')
    file_name = session.get('temp_video_name')
    if file_path and os.path.exists(file_path):
        return render_template('preview.html', file_name=file_name)
    else:
        flash('No video to preview.', 'danger')
        return redirect(url_for('index'))

@app.route('/temp_video')
def temp_video():
    file_path = session.get('temp_video_path')
    file_name = session.get('temp_video_name')
    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=False, download_name=file_name)
    else:
        flash('Video not found.', 'danger')
        return redirect(url_for('index'))

@app.route('/download_video')
def download_video_route():
    file_path = session.get('temp_video_path')
    file_name = session.get('temp_video_name')
    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=file_name)
    else:
        flash('Video not found.', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
