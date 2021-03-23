# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, request, url_for, render_template
import json
from youtube_search import YoutubeSearch

app = Flask(__name__) 
@app.route("/")
def index():
	return render_template("index.html")


@app.route("/buscar", methods=["GET", "POST"])
def buscaVideo():
	data = request.form
	textoBusca = data.get("texto")
	numeroDeResultados = data.get("num")
	if numeroDeResultados == None or numeroDeResultados == 0 or not numeroDeResultados:
		numeroDeResultados = 3
	
	results = YoutubeSearch(textoBusca, max_results=numeroDeResultados).to_json()

	
	return results