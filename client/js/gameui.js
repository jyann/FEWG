function putLoginUI(){
	$("#GameFrame").html('<p>Enter a name:</p>');
	var formhtml = '<input id="Username" type="text"/>'
				+ '<input id="Password" type="text"/>'
				+ '<button id="LoginButton">Login</button>';
	$("#InputForm").html(formhtml);

	$("#LoginButton").click(function(){
		var loginMsg = 'login'
			+ ' ' + $("#Username").val()
			+ ' ' + $("#Password").val();
		websock.send(loginMsg);
	});
}

function putLobbyUI(data){
	$("#GameFrame").html(data);
	var formhtml = '<input id="GameName" type="text"/>'
				+ '<button id="CreateGame">Create</button>'
				+ '<button id="JoinGame">Join</button>';
	$("#InputForm").html(formhtml);

	$("#CreateGame").click(function(){
		var msg = 'create game '
				+ $("#GameName").val();
		websock.send(msg);
	});
	$("#JoinGame").click(function(){
		var msg = 'join game '
				+ $("#GameName").val();
		websock.send(msg);
	});
}

function putGameUI(data){
	$("#GameFrame").html(data);
	var formhtml = '<input id="GameInput" type="text"/>';
	$("#InputForm").html(formhtml);

	$("#GameInput").keypress(function(e){
		if(e.which == 13){
			websock.send($("#GameInput").val());
			$("#GameInput").val('');
		}
	});
}

function initUI(){
	$("#ConnStatus").html('<p>Connected</p>');
	state = 'login';
	putLoginUI();
}

function updateUI(data){
	if(state == 'login'){
		if(data == 'failed'){
			putLoginUI();
		}
		else{
			state = 'logged in';
			putLobbyUI(data);
		}
	}
	else if(state == 'logged in'){
		if(data == 'logged out'){
			state = 'login';
			putLoginUI();
		}
		else if(JSON.parse(data).gameslist != undefined){
			putLobbyUI(data);
		}
		else if(JSON.parse(data).game != undefined){
			putGameUI(data);
		}
	}

	if(data == 'server full')
		$("#GameFrame").html('The server is currently full. Try again later.');
}