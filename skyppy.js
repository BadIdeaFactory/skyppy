let skyppy = (function (allTimings) {
  let index = 0;
  let counter = 0;
  let margin = 0.1;
  let activeTimings = 0;
  filterTiming();
  console.log("filtered timings");
  console.log(activeTimings);
  //player.play();

  function skip() {
    //console.log("--------------- " + index + " --------------------- " + counter);
    //console.log(activeTimings);

    if (counter === 0) {

      if (typeof activeTimings !== 'undefined') {
        console.log("skipping");
        player.currentTime = activeTimings[index][1];
      }
      
      //console.log(activeTimings[index][1]);
      requestAnimationFrame(timeUpdate);
    } else {
      player.pause();
      //console.log("the end!")
    }
  }

  function timeUpdate() {

    let position = player.currentTime * (timeline.clientWidth / player.duration);
    //console.log(position);

    document.getElementById("progress-marker").style.marginLeft = position+"px";

    if (player.currentTime >= activeTimings[index][2] - margin) {
      index = index + 1;
      skip();
    } else {
      requestAnimationFrame(timeUpdate);
    }
  }

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

  const switches = document.getElementsByClassName('filterCheckbox');

  function greySwitchText(element) {
    if (element.checked === false) {
      element.previousElementSibling.classList.add("deselected");
    } else {
      element.previousElementSibling.classList.remove("deselected");
    }
  } 

  Array.from(switches).forEach(element => {

    greySwitchText(element);

    element.addEventListener('click', event => {
      greySwitchText(event.target);
      drawTimeline(allTimings);
      return false;
    });
  });


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

      allTimings[lastClickedSegmentIndex][0] = segmentType;
      filterTiming();
      console.log("CLICKED");
      drawTimeline(allTimings);
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

  //let result;

  player.on('play', event => {
    console.log("play event");
    console.dir(skyppy);
    skip();
    //skyppy.skip();
  });

  const timeline = document.getElementById('timeline');
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


  /*let replace = function(url) {
    player.source = {
      type: 'video',
      sources: [
        {
          src: url,
          provider: 'youtube',
        },
      ],
    }
  };*/

  //timings = filterTiming();
  drawTimeline(allTimings);

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
        allTimings = segmenter_to_list;

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
    //timings = times;
    let tl = document.getElementById('timeline');
    //let te = document.getElementById('timeline-edit');
    tl.innerHTML = "";
    //te.innerHTML = "";
    let totalTime = times[times.length-1][2];
    //console.log(tl);

    times.forEach((element, index) => {
      let widthPc = ((element[2] - element[1]) / totalTime) * 100;
      let label = element[0];

      let inputElements = document.getElementsByClassName('filterCheckbox');

      let matched = false;

      Array.from(inputElements).forEach(input => {
        if (input.checked == true) {
          if (input.value == element[0]) {
            tl.insertAdjacentHTML('beforeend', `<div class="label-${label}" style="width:${widthPc}%" data-index="${index}"></div>`);
            matched = true;
          }
        }
      });

      if (matched == false) {
        tl.insertAdjacentHTML('beforeend', `<div class="label-${label}" style="width:${widthPc}%; opacity:0.2" data-index="${index}"></div>`);
      }

    });

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
    let inputElements = document.getElementsByClassName('filterCheckbox');
    let result = [];
   
    allTimings.forEach(element => {
      Array.from(inputElements).forEach(input => {
        if (input.checked == true) {
          if (input.value == element[0]) {
            result.push(element);
          }
        }
      });
    });
  
    activeTimings = result;
  }
});

window.onload = function() {

  fetch("test.json")
  .then(response => response.json())
  .then(json => {
    skyppy(json.data);
  });
  
}