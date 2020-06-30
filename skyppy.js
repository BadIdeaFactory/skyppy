  const showEvents = ['mouseenter', 'focus'];
  const hideEvents = ['mouseleave', 'blur'];

  /*showEvents.forEach(event => {
    button.addEventListener(event, show);
  });

  hideEvents.forEach(event => {
    button.addEventListener(event, hide);
  });*/

  const hashArray = window.location.hash.substr(1).split('&');
  //console.log(hashArray);

  
  const labelParams = ["l","h","q","n","m"];
  //console.log(labelParams);

  // grab any labels off the URL

  if (window.location.hash.length > 0) {
    //for (let h = 0; h < hashArray.length; h++) {
    hashArray.forEach(hash => {
      //let keyval = hashArray[h].split('=');
      let keyval = hash.split('=');
      let labelRef = document.getElementById('checkname-'+keyval[0]);
      if (labelRef != null) {
        labelRef.innerHTML = decodeURIComponent(keyval[1]);
      }
    });
  }

  const labelEdit = document.getElementsByClassName("editCheckname");
  //console.log(labelEdit);

  Array.from(labelEdit).forEach(element => {
    element.addEventListener('click', event => {
      let sibling = event.target.nextElementSibling;
      sibling.contentEditable = 'true';
      sibling.focus();
      event.preventDefault();
      return false;
    });
  });

  const label = document.getElementsByClassName("checkname");

  //for (let m = 0; m < label.length; m++) {
  Array.from(label).forEach(addLabelListeners);

  function addLabelListeners(element, index) {
    element.addEventListener('input', event => {
      console.log(event.inputType);
      console.dir(event);
      if (event.inputType == "insertParagraph" || (event.inputType == "insertText" && event.data == null)) { // check for return bring hit
        event.target.contentEditable = false;
        event.target.innerHTML = event.target.innerHTML.replace('<br>','');
        event.target.blur();
        addUrlParam(labelParams[m], event.target.innerText);
      }
      event.preventDefault();
      return false;
    });

    element.addEventListener('blur', event => {
      event.target.blur();
      event.preventDefault();
      addUrlParam(labelParams[index], event.target.innerText);
      return false;
    });
  }

  function addPickerListeners(element, index) {

    element.addEventListener('click', event => {

      let segmentType = null;
      let classList = event.target.classList;

      if (classList.contains("label-female")) {
        segmentType = "female";
      }
      if (classList.contains("label-male")) {
        segmentType = "male";
      }
      if (classList.contains("label-music")) {
        segmentType = "music";
      }
      if (classList.contains("label-noEnergy")) {
        segmentType = "noEnergy";
      }
      if (classList.contains("label-noise")) {
        segmentType = "noise";
      }

      all_timings[lastClickedSegmentIndex][0] = segmentType;
      let timings = filterTiming();
      drawTimeline(timings);
      event.preventDefault();
      return false;
    });
  }

  function addUrlParam(key, val){

    //key = encodeURIComponent(key); 
    //value = encodeURIComponent(value);

    let newParam = key + '=' + val,
        params = newParam;

    let search = document.location.hash;    

    if (search) {
      // Try to replace an existance instance
      params = search.replace(new RegExp('([#&])' + key + '[^&]*'), '$1' + newParam);

      // If nothing was replaced, then add the new param to the end
      if (params === search) {
        params += '&' + newParam;
      }
    }

    document.location.hash = params;
  };


  let player = new Plyr('#player');

  let result;

  player.on('play', event => {
    console.log("play event");
    start();
  });

  let timeline = document.getElementById('timeline');
  let lastClickedSegmentIndex = null;

  timeline.addEventListener('click', event => {
    let offset = (document.getElementById('pagebody').clientWidth - timeline.clientWidth) / 2;
    player.currentTime = player.duration * (event.clientX - offset) / timeline.clientWidth;
    player.play();
    lastClickedSegmentIndex = event.target.getAttribute("data-index");
    let pickers = document.getElementsByClassName('picker');
    Array.from(pickers).forEach(addPickerListeners);
    return false;
  });

  let replace = function(url) {
    player.source = {
      type: 'video',
      sources: [
        {
          src: url,
          provider: 'youtube',
        },
      ],
    }
  };

  let all_timings = null;

  fetch("test.json")
  .then(response => response.json())
  .then(json => {
    all_timings = json.data;
    let timings = filterTiming();
    drawTimeline(timings);
  });

  let miavar;
  let embed;
  let html_video;

  let start_download_video = function() {

    document.getElementById("crono").innerHTML = "start process...";

    /*let payload = {
        link_video: document.getElementById("youtube_link").value
    };

    axios({
    url: "{{url_for('give_video')}}",
    method: 'post',
    data: payload
    })
    .then(function (response) {
        mialet =  "json" + response.data["result"];
        embed = response.data["embed"];
        let video_id = embed.split("?v=");
        replace(video_id[video_id.length - 1]);
        console.log(video_id[video_id.length - 1]);
        html_data = response.data["html_data"];
        segmenter_to_list = response.data["segmenter_to_list"];
        all_timings = segmenter_to_list;

    }).then(function(result) {
        document.getElementById("crono").innerHTML = "process complete...";
        document.getElementById("result").innerHTML = "downloading ... ";
    }).then(function(result){
        document.getElementById("result").innerHTML = "result " + miavar;

        document.getElementById("segmenter_to_list_div").innerHTML = segmenter_to_list;
    }).catch(function (error) {
        document.getElementById("result").innerHTML = "Error..try later";
        console.log(error);
    });*/
  };

  function drawTimeline(times) {
    //console.log("p-----");
    //console.log(times);
    timings = times;
    let tl = document.getElementById('timeline');
    let te = document.getElementById('timeline-edit');
    tl.innerHTML = "";
    te.innerHTML = "";
    let totalTime = timings[timings.length-1][2];
    //console.log(tl);
    for (let t = 0; t < times.length; t++) {
      let widthPc = ((times[t][2] - times[t][1]) / totalTime) * 100;
      let label = times[t][0];
      tl.insertAdjacentHTML('beforeend', `<div class="label-${label}" style="width:${widthPc}%" data-index="${t}"></div>`);
      //te.insertAdjacentHTML('beforeend', `<div class="label-edit" style="width:${widthPc}%"></div>`);
    }

    const spanHigherPicker = `<span title="${document.getElementById('checkname-h').innerText}" class="picker label-female"></span>`;
    const spanMusicPicker  = `<span title="${document.getElementById('checkname-m').innerText}" class="picker label-music"></span>`;
    const spanQuietPicker  = `<span title="${document.getElementById('checkname-q').innerText}" class="picker label-noEnergy"></span>`;
    const spanNoisePicker  = `<span title="${document.getElementById('checkname-n').innerText}" class="picker label-noise"></span>`;
    const spanLowerPicker  = `<span title="${document.getElementById('checkname-l').innerText}" class="picker label-male"></span>`;

    tippy('.label-male', {
      trigger: 'long-press',
      placement: 'bottom',
      content: spanHigherPicker + spanMusicPicker + spanQuietPicker + spanNoisePicker,
      allowHTML: true,
      theme: 'male',
    });

    tippy('.label-female', {
      trigger: 'long-press',
      placement: 'bottom',
      content: spanLowerPicker + spanMusicPicker + spanQuietPicker + spanNoisePicker,
      allowHTML: true,
      theme: 'female',
    });

    tippy('.label-music', {
      trigger: 'long-press',
      placement: 'bottom',
      content: spanLowerPicker + spanHigherPicker + spanQuietPicker + spanNoisePicker,
      allowHTML: true,
      theme: 'music',
    });

    tippy('.label-noEnergy', {
      trigger: 'long-press',
      placement: 'bottom',
      content: spanLowerPicker + spanHigherPicker + spanMusicPicker + spanNoisePicker,
      allowHTML: true,
      theme: 'noEnergy',
    });

    tippy('.label-noise', {
      trigger: 'long-press',
      placement: 'bottom',
      content: spanLowerPicker + spanHigherPicker + spanMusicPicker + spanQuietPicker,
      allowHTML: true,
      theme: 'noise',
    });
  }

  function filterTiming() {
    result = [];
    //console.log("filterTiming");
    console.log(all_timings);
    let inputElements = document.getElementsByClassName('filterCheckbox');
    //console.log("inputElements");
    //console.log(inputElements);
    for (let i = 0; i < all_timings.length; i++) {
      //console.log(all_timings[i][0]);

      for(let j = 0; inputElements[j]; j++) {
        if(inputElements[j].checked == false) {
          if (inputElements[j].value == all_timings[i][0]) {
            result.push(all_timings[i]);
          }
          //break;
        }
      }
    }
    
    //console.log("-----");
    //console.log(result);
    //drawTimeline(result);
    return result;
  }


  let start = function (){
    let index = 0;
    let counter = 0;
    let margin = 0.1;
    let timings = filterTiming();
    //console.log(timings);
    //player.play();

    function skip() {
      //console.log("--------------- " + index + " --------------------- " + counter);

      if (counter === 0) {

        if (typeof timings !== 'undefined') {
          player.currentTime = timings[index][1];
        }
        
        //console.log(timings[index][1]);
        requestAnimationFrame(timeUpdate);
      } else {
        player.pause();
        //console.log("the end!")
      }
    }

    function timeUpdate() {

      //console.log(player.currentTime + " > " + timings[index][2]);

      if (player.currentTime >= timings[index][2] - margin) {
        //player.pause();
        index = index + 1;
        try {
          let stop = timings[index][1];
        }
        catch(err) {
          console.log(err);
          counter = 1;
        }
        //player.currentTime = timings[index][1];
        skip();
      } else {
        requestAnimationFrame(timeUpdate);
      }
    }

    skip();
  }
