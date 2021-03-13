# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, request, url_for, render_template
import youtube_dl
import base64
import json
import re


def youtube_erro(erro):
	if "in your country" in erro:
		print('erro de localização do video')
		return 'video indisponivel no pais'

	elif 'Too Many Requests' in erro:
		print('bloqueio da  api')
		return 'muitas requisições'

	else:
		return 'desconhecido'



def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match.group(6)

    return youtube_regex_match


def baixar(song_url, song_title):

	try:
		outtmpl = './'+song_title + '.%(ext)s'
		ydl_opts = {
			'noplaylist' : True,
			'format': 'bestaudio[ext=m4a]',
			'outtmpl': outtmpl
			
		}

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			info_dict = ydl.extract_info(song_url, download=False)
		
		if (info_dict['duration']/60) >= 18:
			return 'arquivo grande demais'
		else:
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				info_dict = ydl.extract_info(song_url, download=True)

			return 'ok'

	except Exception as e:
		erro = str(e)
		return youtube_erro(erro)
		

def yt_dados(url):
	try:
		ydl_opts = {'noplaylist' : True}

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			meta = ydl.extract_info(
				url, download=False)

		'''
		titulo = meta['title']
		tempo = meta['duration']
		tempo = tempo/60
		tempo = int(tempo)
		id_video = meta['id']
		'''
		
		return meta

	except Exception as e:
		#print("resultado: "+str(e))
		erro = str(e)
		return youtube_erro(erro)

app = Flask(__name__) 
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/info", methods=["GET", "POST"])
def info():
	data = request.form
	link = data.get("link")
	dados = yt_dados(link)

	return dados

@app.route("/buscar", methods=["GET", "POST"])
def buscaVideo():
	data = request.form
	textoBusca = data.get("texto")
	numeroDeResultados = data.get("num")
	if numeroDeResultados == None or numeroDeResultados == 0 or not numeroDeResultados:
		numeroDeResultados = 1
	resultado = {'resultados':[]}
	metadata = yt_dados(f'ytsearch{numeroDeResultados}: {textoBusca}')
	metadata = metadata["entries"]
	for i in metadata:
		titulo = i["title"]
		duracao = int(i['duration']/60)
		url = f'https://youtu.be/{i["id"]}'
		resultado["resultados"].append({'titulo': titulo, 'tempo': duracao, 'link': url})
	return resultado

@app.route("/musica", methods=["GET", "POST"])
def baixaMusica():
	print('musica')
	data = request.form
	link = data.get("link")
	validar = youtube_url_validation(link)
	if validar:
		nome = validar
		print(nome)
		retorno = baixar(link, nome)
		if retorno =='ok':
			with open(f"{nome}.m4a", "rb") as file:
				encoded_string = base64.b64encode(file.read())

			base64_string = encoded_string.decode('utf-8')
			raw_data = {'nome': f'{nome}.m4a', 'file': base64_string}
			json_data = json.dumps(raw_data, indent=2)

			return json_data
		else:
			return json.dumps({'erro-api': retorno}, indent=2)
	else:
		return json.dumps({'erro':'URL invalida'}, indent=2)