function buscaYT() {
	let inputlink = document.querySelector('input[id=link]');
	let link = inputlink.value;
	let url = 'https://t-youtube-info.herokuapp.com/info';
	var data = new FormData();
	data.append('link', link);
	let xhr = new XMLHttpRequest();
	xhr.open('POST', url, true);
	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4) {
			if (xhr.status = 200)
				preencheCampos(xhr.responseText);
				
		}
	}
	xhr.send(data);
	var btnlimpar = document.getElementById("limpar");
	btnlimpar.style.display = "inline";
	  
}

function preencheCampos(json) {

	var elemento_pai = document.getElementById('centro');
	var conteudo = document.createElement('textarea');
	conteudo.setAttribute("class", "resultado");
	conteudo.setAttribute("rows", "15");
	conteudo.setAttribute("cols", "50");
	var keys = Object.keys(JSON.parse(json));
	var texto = document.createTextNode(keys.formats);
	conteudo.appendChild(texto);
	elemento_pai.appendChild(conteudo);


}

function limpar(){
	let textos = document.getElementsByClassName("resultado");
	if (textos.length <=1 ) {
		var btnlimpar = document.getElementById("limpar");
		btnlimpar.style.display = "none";
	}
	for(var i=0; i<textos.length; i++) {
		textos[-i].remove();
	}
}