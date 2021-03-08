# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, request, url_for, render_template
import youtube_dl
import json

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

		if "in your country" in erro:
			print('erro de localização do video')
			return 'erro, video indisponivel'

		elif 'Too Many Requests' in erro:
			print('bloqueio da  api')
			return 'erro, ip block'

		else:
			return 'erro desconhecido'


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