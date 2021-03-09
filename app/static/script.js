const showData = (result)=>{
    for(const campo in result){
        console.log(campo)
    };
};





function buscaYT() {
	let inputlink = document.querySelector('input[id=link]');
	let link = inputlink.value;
	let url = 'https://t-youtube-info.herokuapp.com/info';
	var data = new FormData();
	data.append('link', link);

	const options = {
        method: 'POST',
        mode: 'cors',
        cache: 'default',
        body: data
    };

	fetch(url, options)
    .then(response =>{ response.json()
        .then( data => showData(data))
    })
    .catch(e => console.log('Deu Erro: '+ e,message))

	var btnlimpar = document.getElementById("limpar");
	btnlimpar.style.display = "inline";
	  
};

function preencheCampos(json) {

	var elemento_pai = document.getElementById('centro');
	var conteudo = document.createElement('textarea');
	conteudo.setAttribute("class", "resultado");
	conteudo.setAttribute("rows", "15");
	conteudo.setAttribute("cols", "50");
	//var obj = JSON.parse(json);
	var texto = document.createTextNode(json);
	conteudo.appendChild(texto);
	elemento_pai.appendChild(conteudo);


};

function limpar(){
	let textos = document.getElementsByClassName("resultado");
	if (textos.length <=1 ) {
		var btnlimpar = document.getElementById("limpar");
		btnlimpar.style.display = "none";
	};
	for(var i=0; i<textos.length; i++) {
		textos[-i].remove();
	};
};
