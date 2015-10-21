function emptyForms(){
	$("#AddrInput").val('');
	$("#PortInput").val('');
	$("#Username").val('');
	$("#Password").val('');
	$("#GameName").val('');
	$("#GameInput").val('');
}

// connect ui
function initConnectUI(){
	$("#ConnStatus").html('<p>Not Connected</p>');
	if(state != 'connecting')
		putConnectForm();
	state = 'connecting';
	putConnectUI();
}
function putConnectUI(){
	$("#GameFrame").html('<p>Enter server address and port:</p>');
}
function putConnectForm(){
	$("#QuitGameBtn").hide();
	$("#LogoutBtn").hide();
	$("#DisconnectBtn").hide();

	$("#ConnectForm").show();
	$("#LoginForm").hide();
	$("#LobbyForm").hide();
	$("#GameForm").hide();

	emptyForms();
}
function connect(serverAddr){
	websock = new WebSocket('ws://'+serverAddr);
	websock.onopen = function(msg){
		$("#LogView").html('');
		initLoginUI();
	};
	websock.onclose = function(msg){
		initConnectUI();
	};
	websock.onmessage = function(msg){
		//$("#LogView").text(msg.data);
		updateUI(msg.data);
	};
	websock.onerror = function(msg){
		$("#LogView").html('<p class="err">Connection error</p>');
	};
}

// login ui
function initLoginUI(){
	$("#ConnStatus").html('<p>Connected</p>');
	if(state != 'login')
		putLoginForm();
	state = 'login';
	putLoginUI();
}
function putLoginUI(){
	$("#GameFrame").html('<p>Enter a name:</p>');
}
function putLoginForm(){
	$("#QuitGameBtn").hide();
	$("#LogoutBtn").hide();
	$("#DisconnectBtn").show();

	$("#ConnectForm").hide();
	$("#LoginForm").show();
	$("#LobbyForm").hide();
	$("#GameForm").hide();

	emptyForms();
}

//lobby ui
function initLobbyUI(data){
	if(state != 'inlobby')
		putLobbyForm();
	state = 'inlobby';
	putLobbyUI(data);
}
function putLobbyUI(data){
	var jsondata = JSON.parse(data);

	var html = '<table><tr>';
	$.each(jsondata.gameslist, function(key, item){
		html += '<td>Game: '+item.name+'<br/>'
			+ 'Players: '+item.player_count+'</td>';
	});
	$("#GameFrame").html(html+'</tr></table>');
}
function putLobbyForm(){
	$("#QuitGameBtn").hide();
	$("#LogoutBtn").show();
	$("#DisconnectBtn").show();

	$("#ConnectForm").hide();
	$("#LoginForm").hide();
	$("#LobbyForm").show();
	$("#GameForm").hide();

	emptyForms();
}

// game ui
function initGameUI(data){
	if(state != 'ingame')
		putGameForm();
	state = 'ingame';
	putGameUI(data);
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
}
function putGameForm(){
	$("#QuitGameBtn").show();
	$("#LogoutBtn").show();
	$("#DisconnectBtn").show();

	$("#ConnectForm").hide();
	$("#LoginForm").hide();
	$("#LobbyForm").hide();
	$("#GameForm").show();

	emptyForms();
}

function updateUI(data){
	if(state == 'login'){
		if(data == 'failed'){
			putLoginUI();
		}
		else{
			initLobbyUI(data);
		}
	}
	if(state == 'inlobby'){
		if(data == 'logged out'){
			initLoginUI();
		}
		if(JSON.parse(data).game != undefined){
			initGameUI(data);
		}
		if(JSON.parse(data).gameslist != undefined)
			putLobbyUI(data);
	}
	if(state == 'ingame'){
		if(data == 'logged out'){
			initLoginUI();
		}
		if(JSON.parse(data).status == 'game_quit'){
			initLobbyUI(data);
		}
		if(JSON.parse(data).game != undefined)
			putGameUI(data);
	}

	if(data == 'server full')
		$("#GameFrame").html('The server is currently full. Try again later.');
}

$(document).ready(function(){
	state = 'loading';
	if(window.WebSocket === undefined){
		$("#GameFrame")
		.html('<p>This application requires Websocket support. '
			+ 'Update your browser or try a different one.</p>');
	}
	else{
		initConnectUI();
	}

	// Button handlers
	$("#DisconnectBtn").click(function(){
		if(websock != undefined){
			var msg = 'quit';
			websock.send(msg);
		}
	});
	$("#QuitGameBtn").click(function(){
		if(websock != undefined){
			var msg = 'quit game';
			websock.send(msg);
		}
	});
	$("#LogoutBtn").click(function(){
		if(websock != undefined){
			var msg = 'logout';
			websock.send(msg);
		}
	});
	// Connect
	$("#ConnectBtn").click(function(){
		try{
			connect($("#AddrInput").val()+":"+$("#PortInput").val());
		}
		catch(err){
			$("#LogView").html('<p class="err">Connection error</p>');
		}
	});
	// Login
	$("#LoginButton").click(function(){
		var loginMsg = 'login'
			+ ' ' + $("#Username").val()
			+ ' ' + $("#Password").val();
		websock.send(loginMsg);
	});
	// Lobby
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
	// Game
	$("#GameInput").keypress(function(e){
		if(e.which == 13){
			var msg = $("#GameInput").val();
			if(msg == 'quit')
				msg += ' game';
			websock.send(msg);
			$("#GameInput").val('');
		}
	});

	// Let server know before leaving
	window.onbeforeunload = function(){
		if(websock != undefined)
			websock.send('logout');
	};
});
