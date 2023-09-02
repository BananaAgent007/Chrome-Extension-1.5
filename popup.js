var server = 'http://ec2-18-224-251-113.us-east-2.compute.amazonaws.com:8181'


//add eventlisteners for each button
let startTimer = document.getElementById("start");
let stopTimer = document.getElementById("stop");
let resetTimer = document.getElementById("reset");
let enterusername = document.getElementById("entername");
let saveTime = document.getElementById("save");
let showTimes = document.getElementById("times");
let clearTime = document.getElementById("clear");

let prediction = document.getElementById('prediction');
let avewordcnt = document.getElementById('avewordcnt'); 
let biggestword = document.getElementById('biggestword'); 
let difficulty = document.getElementById('difficulty'); 

//variables to keep track of time
var startTime;
var elapsedTime = 0;
var timerInterval; 
var cont = false; 
var websitePreviousURL;


var username; //modify html to include a text box for username 
var websiteURL = ""; //modify html to indicate current website link
ErrorMsg.innerHTML = "";
chrome.storage.local.get('loadCount', ({loadCount}) =>{
	if (loadCount == null)
	{
		chrome.storage.local.set({loadCount});
		loadCount = 0;
	}
	else
	self.loadCount = loadCount;

	console.log('checking for loadCount: ' + loadCount);
	self.loadCount = self.loadCount +1;
});
//store data that needs to be re-accessed each time popup.html refreshes 
chrome.storage.local.get('startTime', ({startTime}) =>{
	self.startTime = startTime;
	console.log('checking for past startTime: ' + startTime);
});

chrome.storage.local.get('elapsedTime', ({elapsedTime}) =>{
	self.elapsedTime = elapsedTime;
	console.log('checking for past elapsedTime: ' + elapsedTime);
});

//gets active website url 
 chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {

	 var activeTab = tabs[0];
	 console.log(tabs);
    self.websiteURL = activeTab.url; 
	 console.log('active website is: ' + activeTab.url);

 });
 
 chrome.storage.local.get('websitePreviousURL', ({websitePreviousURL}) =>{

	 if(websitePreviousURL!=null)
	 {
		if (self.websiteURL != websitePreviousURL)
		{
			console.log('website change, reset timer ');
			console.log('websiteURL: ' + websiteURL);
			console.log('websitePreviousURL: ' + websitePreviousURL);
			resetTime()
			websitePreviousURL = self.websiteURL
			
		}
	 }
	 else
	 {
		 websitePreviousURL = self.websiteURL;
	 }
	 chrome.storage.local.set({websitePreviousURL});
});

chrome.storage.local.get('cont', ({cont}) =>{
	if (cont == true){
		self.timerInterval = setInterval(function printTime(){
			elapsedTime = Date.now() - startTime;
			chrome.storage.local.set({elapsedTime});
			setTime(timeToString(elapsedTime));

		}, 10);
		self.cont = true; 
		showButton("STOP"); 
		console.log('checking for cont: ' + cont);
	}
	else{
		self.cont = false; 
		clearInterval(self.timerInterval);
		setTime(timeToString(elapsedTime));
		showButton("PLAY"); 
		console.log('checking for cont: ' + cont);	
	}
	
});

chrome.storage.local.get('username', ({username}) =>{
	self.username = username;
	console.log('checking for past username: ' + username);
	document.getElementById("savename").value = username;
	showPrediction();
});


const showPrediction = async function(){
	
	fetch(server + '/showPrediction',{
		
		method: "POST",
			
		body: JSON.stringify({
			"username": self.username,
			"website": self.websiteURL
		}),
		headers: new Headers({
			"Content-Type": "application/json"
		})
		
	}).then((response) => {
        return response.json();
    }).then((text) => {
		var webstats = text["webstats"]; 

        console.log('showPrediction response text:');
		console.log(webstats); 

		prediction.innerHTML = "Time Predicition: " + timeToString(webstats[2]);
		avewordcnt.innerHTML =  "Average Word Size: " + webstats[1];
		biggestword.innerHTML = "Number of Words:       " + webstats[3];
		difficulty.innerHTML="Readability Score:     " + webstats[4];
    }).catch(err => {
		console.log("error caught");
		console.log(err);
		ErrorMsg.innerHTML = "Try another website";
	});

}


const saveTimefunc = async function(){
	
	stop();
	if(self.elapsedTime > 0)
	{
		console.log('SAVETIME: sending ' + username + ', ' + elapsedTime + ', ' + websiteURL );	
		fetch(server + '/saveTime',{
			
			method: "POST",
				
			body: JSON.stringify({
				"username": self.username,
				"time": self.elapsedTime,
				"website": self.websiteURL
			}),
			headers: new Headers({
				"Content-Type": "application/json"
			})
			
		}).catch(err => {
			console.log("error caught");
			console.log(err);
		}).then((response) => {
			return response.json();
		}).then((text) => {
			resetTime();
			console.log('saveTimefunc GET response text: ');
			console.log(text); 	
		 }).catch(err => {
			console.log("saveTimefunc error caught: " + err);
		});
	}	
}

function getUsername(){
	self.username = document.getElementById('savename').value;
	//save username locally 
	chrome.storage.local.set({username});
	console.log("getUsername: " );
	resetTime();
	showPrediction();

}


function showButton(button){
	const currbutton = button === "PLAY" ? startTimer : stopTimer;
	const hidebutton = button === "PLAY" ? stopTimer : startTimer;
	
	currbutton.style.display = "block";
	hidebutton.style.display = "none"; 
}
	
	
function start(){
	startTime = Date.now() - elapsedTime; 
	chrome.storage.local.set({startTime});
	
	self.timerInterval = setInterval(function printTime(){
		elapsedTime = Date.now() - startTime;
		chrome.storage.local.set({elapsedTime});
		setTime(timeToString(elapsedTime));

	}, 10);
	self.cont = true; 
	chrome.storage.local.set({cont});
	
	showButton("STOP"); 
}

function stop(){
	clearInterval(self.timerInterval);
	showButton("PLAY"); 
	
	self.cont = false;
	chrome.storage.local.set({cont});
}

function resetTime(){
	clearInterval(self.timerInterval); 
	setTime("00:00:00");
	elapsedTime = 0;
	chrome.storage.local.set({elapsedTime});

	showButton("PLAY");
	
	self.cont = false;
	chrome.storage.local.set({cont});
	self.startTime = 0;
	chrome.storage.local.set({startTime});

};

function setTime(txt){
	document.getElementById("timeDisplay").innerHTML = txt;
};



function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}


function timeToString(time) {
  let diffInHrs = time / 3600000;
  let hh = Math.floor(diffInHrs);

  let diffInMin = (diffInHrs - hh) * 60;
  let mm = Math.floor(diffInMin);

  let diffInSec = (diffInMin - mm) * 60;
  let ss = Math.floor(diffInSec);

  let diffInMs = (diffInSec - ss) * 100;
  let ms = Math.floor(diffInMs);

  let formattedMM = mm.toString().padStart(2, "0");
  let formattedSS = ss.toString().padStart(2, "0");
  let formattedMS = ms.toString().padStart(2, "0");

  return `${formattedMM}:${formattedSS}:${formattedMS}`;
}

startTimer.addEventListener("click", start);
stopTimer.addEventListener("click", stop);
resetTimer.addEventListener("click", resetTime);
entername.addEventListener("click", getUsername);
saveTime.addEventListener("click", saveTimefunc);	
