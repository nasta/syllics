function open_login(){
	document.getElementById('loginbg').style.display='block';
	document.getElementById('login').style.display='block';
	showloginbg();
}

function close_login(){
	document.getElementById('loginbg').style.display='none';
	document.getElementById('login').style.display='none';
}

function showloginbg(){
	var sWidth,sHeight;
	sWidth = screen.width;
	sWidth = document.body.offsetWidth;
	sHeight=document.body.offsetHeight;
	if (sHeight<screen.height){sHeight=screen.height;}
	document.getElementById("loginbg").style.width = sWidth + "px";
	document.getElementById("loginbg").style.height = sHeight + "px";
	document.getElementById("loginbg").style.display = "block";
	document.getElementById("loginbg").style.display = "block";
	document.getElementById("loginbg").style.right = document.getElementById("login").offsetLeft + "px";
}

function logo_in() {
	alert()
	//验证
	//转向...
	//myform.action=""
	//myform.submit()
	close_login();
};