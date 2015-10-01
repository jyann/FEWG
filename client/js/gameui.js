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
	var formhtml = '<input id="AddrInput" type="text" autofocus/>'
				+ '<input id="PortInput" type="text"/>'
				+ '<button id="ConnectBtn">Connect</button>';
	$("#InputForm").html(formhtml);

	$("#ConnectBtn").click(function(){
		try{
			connect($("#AddrInput").val()+":"+$("#PortInput").val());
		}
		catch(err){
			$("#LogView").html('<p class="err">Connection error</p>');
		}
	});
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
	var formhtml = '<input id="Username" type="text" autofocus/>'
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
	var formhtml = '<button id="LogoutBtn">Logout</button><br/>'
				+ '<input id="GameName" type="text" autofocus/>'
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
	var formhtml = '<button id="QuitGameBtn">Quit Game</button>'
			+ '<button id="LogoutBtn">Logout</button><br/>'
			+ '<input id="GameInput" type="text" autofocus/>';
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
			var msg = $("#GameInput").val();
			if(msg == 'quit')
				msg += ' game';
			websock.send(msg);
			$("#GameInput").val('');
		}
	});
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
			initGameUI(data);
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

	window.onbeforeunload = function(){
		websock.send('logout');
	};
});
