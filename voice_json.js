//uses webspeech API. SpeechRecognition is an interface for webspeech API
try {
    var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    var recognition = new SpeechRecognition(); //recognition gives access to all the API's methods and functions
  }
  catch(e) {
    console.error(e);
    $('.app').hide();
  }
  
  
  var noteTextarea = $('#note-textarea'); //input field where spoken text shows up
  var noteContent = '';
  
  recognition.continuous = true;
  
  recognition.onresult = function(event) {
    var current = event.resultIndex;  
    var transcript = event.results[current][0].transcript;
    var mobileRepeatBug = (current == 1 && transcript == event.results[0][0].transcript); //dealing with a bug in android
    if(!mobileRepeatBug) {
      noteContent += transcript; // append transcript to input field text
      noteTextarea.val(noteContent); // update text in input
    }
  
  };
  
  recognition.onstart = function() {
  console.log("onStart");
  //runs when listening starts
  }
  
  recognition.onspeechend = function() {
    console.log("onEnd");
    //when speech over
  }
  
  recognition.onerror = function(event) {
    if(event.error == 'no-speech') {
      alert("Error");
    };
  }
  
  window.onload = function() {
    recognition.start();
    //start listening when page loads
  
  };
  
  //this is jquery
  $('#start-record-btn').on('click', function(e) {
    if (noteContent.length) {
      noteContent += ' ';
    }
    recognition.stop();
    recognition.start(); //restart recording
  });
  
  $('#pause-record-btn').on('click', function(e) {
    recognition.stop(); //pause button
  });
  
  noteTextarea.on('input', function() {
    noteContent = $(this).val(); //initialize noteContent for later use
  })
  function func(command,reply)
  {
      $("p").append("<span class=\"mine\">"+command+"</span><span class=\"reply\">Pi: "+reply+"</span>"); //log of all commands and replies

  }      
  $('#send-command').on('click', function(e) {
    //ajax to recieve json data from flask_server.py makes request to flask_server
    $.ajax({
        url: '/voiceWebInterfacePost', //URL to send request to
        data: $('form').serialize(), //sending form data to the server
        type: 'POST', //request type
        success: function(response) { //on success
            console.log(response);
            resp_obj=JSON.parse(response); //parse the json string and you get an object
            func(resp_obj['command'],resp_obj['reply']);
                    },
        error: function(error) {
            console.log(error);
        }
    });
  
    if(!noteContent.length) {
    }
    else {
  
      noteContent = '';
  
      noteTextarea.val('');
    }

  })
  
  
  