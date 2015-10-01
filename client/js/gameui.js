
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
	var formhtml = '<button id="LogoutBtn">Logout</button><br/>'
				+ '<input id="GameName" type="text"/>'
				+ '<button id="CreateGameBtn">Create</button>'
				+ '<button id="JoinGameBtn">Join</button>';
	$("#InputForm").html(formhtml);

	$("#LogoutBtn").click(function(){
		var msg = 'logout';
		websock.send(msg);
	});
	$("#CreateGameBtn").click(function(){
		var msg = 'create game '
				+ $("#GameName").val();
		websock.send(msg);
	});
	$("#JoinGameBtn").click(function(){
		var msg = 'join game '
				+ $("#GameName").val();
		websock.send(msg);
	});
}

function putGameUI(data){
	var jsondata = JSON.parse(data);

	var html = '<table><tr>';
	$.each(jsondata.game.players, function(key, item){
		html += '<td> Player: '+key+'<br/>'
			+'HP: '+item.vars.health+'/'+item.stats.health+'<br/>'
			+'DEF: '+item.vars.defense+'</td>';
	});
	$("#GameFrame").html(html+'</tr></table><hr/>');

	var formhtml = '<button id="QuitGameBtn">Quit Game</button>'
			+ '<button id="LogoutBtn">Logout</button><br/>'
			+ '<input id="GameInput" type="text"/>';
	$("#InputForm").html(formhtml);

	$("#QuitGameBtn").click(function(){
		var msg = 'quit game';
		websock.send(msg);
	});
	$("#LogoutBtn").click(function(){
		var msg = 'logout';
		websock.send(msg);
	});
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
			state = 'inlobby';
			putLobbyUI(data);
		}
	}
	if(state == 'inlobby'){
		if(data == 'logged out'){
			state = 'login';
			putLoginUI();
		}
		if(JSON.parse(data).game != undefined){
			state = 'ingame';
			putGameUI(data);
		}
		if(JSON.parse(data).gameslist != undefined)
			putLobbyUI(data);
	}
	if(state == 'ingame'){
		if(data == 'logged out'){
			state = 'login';
			putLoginUI();
		}
		if(JSON.parse(data).status == 'game_quit'){
			state = 'inlobby';
			putLobbyUI(data);
		}
		if(JSON.parse(data).game != undefined)
			putGameUI(data);
	}

	if(data == 'server full')
		$("#GameFrame").html('The server is currently full. Try again later.');
}

$(document).ready(function(){
	if(window.WebSocket === undefined){
		$("#GameFrame")
		.html('<p>This application requires Websocket support. Update your browser or try a different one.</p>');
	}
	else{
		var wsAddr = "ws://localhost:1234";
		websock = new WebSocket(wsAddr);
		websock.onopen = function(msg){
			initUI();
		};
		websock.onclose = function(msg){
			$("#GameFrame").html('');
			$("#InputForm").html('');
			$("#ConnStatus").html('<p>Disconnected</p>');
		};
		websock.onmessage = function(msg){
			$("#LogView").text(msg.data);
			updateUI(msg.data);
		};
		websock.onerror = function(msg){
			$("#GameFrame").html('<p class="err">Connection error</p>');
		};
	}

	window.onbeforeunload = function(){
		websock.send('logout');
	};
});
