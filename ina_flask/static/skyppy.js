/**
 *
 * @param {object} option [contain url and other variables ]
 * @return {NULL}
 *
 */

function main(option) {
  const api_url = option["server_url"];
  const max_video_lenght_in_minutes = option["max_video_lenght_in_minutes"];
  const hashArray = window.location.hash.substr(1).split("&");
  var ina_skyppy_data;
  let skyppy = function (allTimings, player) {
    let index = 0;
    let margin = 0.1;
    let activeTimings = 0;

    // rome-ignore lint/js/noUndeclaredVariables

    player.on("play", () => {
      //player.volume = 1;
      player.muted = false;
      player.play();
      requestAnimationFrame(timeUpdate);
    });

    function timeUpdate() {
      let position =
        player.currentTime * (timeline.clientWidth / player.duration);
      document.getElementById(
        "progress-marker"
      ).style.marginLeft = `${position}px`;
      index = 0;

      //console.log(activeTimings);

      while (
        player.currentTime >= activeTimings[index][2] - margin &&
        player.currentTime < player.duration
      ) {
        //console.log(player.currentTime);
        //console.log(player.duration);
        if (index + 1 < activeTimings.length) {
          index++;
        }
        //console.log("index = " + index);
      }

      if (player.currentTime < activeTimings[index][1] - margin) {
        // it's in a gap between active timings
        // jump to the start of the next active timing
        player.currentTime = activeTimings[index][1];
      }

      requestAnimationFrame(timeUpdate);
    }

    const labelParams = ["l", "h", "q", "n", "m"];

    // grab parameters from the URL

    if (window.location.hash.length > 0) {
      hashArray.forEach((hash) => {
        let keyval = hash.split("=");

        if (labelParams.includes(keyval[0])) {
          let labelRef = document.getElementById(`checkname-${keyval[0]}`);
          if (labelRef != null) {
            labelRef.innerHTML = decodeURIComponent(keyval[1]);
          }
        }

        // check for switches state
        if (keyval[0] === "s") {
          let switchesOn = keyval[1].split("");

          labelParams.forEach((val) => {
            if (switchesOn.includes(val)) {
              document.getElementById(`switchname-${val}`).checked = true;
            } else {
              document.getElementById(`switchname-${val}`).checked = false;
            }
          });
        }

        // check for segment override
        let firstChar = keyval[0].substr(0, 1);
        if (firstChar === "i") {
          let index = keyval[0].substr(1);
          let segmentType = keyval[1];
          allTimings[index][0] = segmentType;
        }
      });
    }

    console.log("filter timing 2");
    filterTiming();

    const labelEdit = document.getElementsByClassName("editCheckname");

    Array.from(labelEdit).forEach((element) => {
      element.addEventListener("click", (event) => {
        let sibling = event.target.nextElementSibling;
        sibling.contentEditable = "true";
        sibling.focus();
        event.preventDefault();
        return false;
      });
    });

    const label = document.getElementsByClassName("checkname");

    Array.from(label).forEach(addLabelListeners);

    function addLabelListeners(element, index) {
      element.addEventListener("input", (event) => {
        if (
          event.inputType === "insertParagraph" ||
          (event.inputType === "insertText" && event.data == null)
        ) {
          // check for return bring hit
          event.target.contentEditable = false;
          event.target.innerHTML = event.target.innerHTML.replace("<br>", "");
          event.target.blur();
          addUrlParam(labelParams[index], encodeURI(event.target.innerText));
        }
        event.preventDefault();
        return false;
      });

      element.addEventListener("blur", (event) => {
        event.target.blur();
        event.target.contentEditable = "false";
        event.preventDefault();
        addUrlParam(labelParams[index], encodeURI(event.target.innerText));
        return false;
      });

      element.addEventListener("click", (event) => {
        if (event.target.contentEditable === "true") {
          event.preventDefault();
          return false;
        }
      });
    }

    const switches = document.getElementsByClassName("filterCheckbox");

    function greySwitchText(element) {
      if (element.checked === false) {
        element.previousElementSibling.classList.add("deselected");
      } else {
        element.previousElementSibling.classList.remove("deselected");
      }
    }

    function updateSwitchState() {
      let switchStr = "";

      labelParams.forEach((val, index) => {
        if (switches[index].checked === true) {
          switchStr += val;
        }
      });

      addUrlParam("s", switchStr);
    }

    Array.from(switches).forEach((element) => {
      greySwitchText(element);

      element.addEventListener("click", (event) => {
        greySwitchText(event.target);
        filterTiming();
        drawTimeline(allTimings);
        updateSwitchState();
        return false;
      });
    });

    function addPickerListeners(element) {
      element.addEventListener("click", (event) => {
        let segmentType = null;
        let param = null;
        let classList = event.target.classList;

        if (classList.contains("label-l")) {
          param = labelParams[0]; // l
        }

        if (classList.contains("label-h")) {
          param = labelParams[1]; // h
        }

        if (classList.contains("label-q")) {
          param = labelParams[2]; // q
        }

        if (classList.contains("label-n")) {
          param = labelParams[3]; // n
        }

        if (classList.contains("label-m")) {
          param = labelParams[4]; // m
        }

        segmentType = param;

        if (param.length != null) {
          addUrlParam(`i${lastClickedSegmentIndex}`, param);
        }

        allTimings[lastClickedSegmentIndex][0] = segmentType;
        console.log("filter timing 1");
        filterTiming();
        drawTimeline(allTimings);
        event.preventDefault();
        return false;
      });
    }

    const timeline = document.getElementById("timeline");
    let lastClickedSegmentIndex = null;

    timeline.addEventListener("click", (event) => {
      let offset =
        (document.getElementById("pagebody").clientWidth -
          timeline.clientWidth) /
        2;
      let newTime =
        (player.duration * (event.clientX - offset)) / timeline.clientWidth;
      player.currentTime = newTime;
      player.play();
      lastClickedSegmentIndex = event.target.getAttribute("data-index");
      let pickers = document.getElementsByClassName("picker");
      Array.from(pickers).forEach(addPickerListeners);
      return false;
    });

    drawTimeline(allTimings);

    function drawTimeline(times) {
      let tl = document.getElementById("timeline");
      tl.innerHTML = "";
      let totalTime = times[times.length - 1][2];

      times.forEach((element, index) => {
        let widthPc = ((element[2] - element[1]) / totalTime) * 100;
        let label = element[0];

        let inputElements = document.getElementsByClassName("filterCheckbox");

        let matched = false;

        Array.from(inputElements).forEach((input) => {
          if (input.checked === true) {
            if (input.value === element[0]) {
              tl.insertAdjacentHTML(
                "beforeend",
                `<div class="label-${label}" style="width:${widthPc}%" data-index="${index}"></div>`
              );
              matched = true;
            }
          }
        });

        if (matched === false) {
          tl.insertAdjacentHTML(
            "beforeend",
            `<div class="label-${label}" style="width:${widthPc}%; opacity:0.2" data-index="${index}"></div>`
          );
        }

        // switch the search button back on (and hide the spinner) and remove controls, show segment selectors

        document.querySelector(".fa-search").style.removeProperty("display");
        document.querySelector("#button-search").disabled = false;
        document.querySelector(".spinner").style.display = "none";
        document.querySelector(".label-holder").style.removeProperty("display");

        //document.querySelector(".plyr__controls").style.display = "none";
      });

      const spanLowerPicker = `<span title="${
        document.getElementById("checkname-l").innerText
      }" class="picker label-l"></span>`;
      const spanHigherPicker = `<span title="${
        document.getElementById("checkname-h").innerText
      }" class="picker label-h"></span>`;
      const spanMusicPicker = `<span title="${
        document.getElementById("checkname-m").innerText
      }" class="picker label-m"></span>`;
      const spanQuietPicker = `<span title="${
        document.getElementById("checkname-q").innerText
      }" class="picker label-q"></span>`;
      const spanNoisePicker = `<span title="${
        document.getElementById("checkname-n").innerText
      }" class="picker label-n"></span>`;

      // rome-ignore lint/js/noUndeclaredVariables
      tippy(".label-l", {
        trigger: "long-press",
        placement: "bottom",
        content:
          spanHigherPicker +
          spanMusicPicker +
          spanQuietPicker +
          spanNoisePicker,
        allowHTML: true,
        theme: "l",
      });

      // rome-ignore lint/js/noUndeclaredVariables
      tippy(".label-h", {
        trigger: "long-press",
        placement: "bottom",
        content:
          spanLowerPicker + spanMusicPicker + spanQuietPicker + spanNoisePicker,
        allowHTML: true,
        theme: "h",
      });

      // rome-ignore lint/js/noUndeclaredVariables
      tippy(".label-m", {
        trigger: "long-press",
        placement: "bottom",
        content:
          spanLowerPicker +
          spanHigherPicker +
          spanQuietPicker +
          spanNoisePicker,
        allowHTML: true,
        theme: "m",
      });

      // rome-ignore lint/js/noUndeclaredVariables
      tippy(".label-q", {
        trigger: "long-press",
        placement: "bottom",
        content:
          spanLowerPicker +
          spanHigherPicker +
          spanMusicPicker +
          spanNoisePicker,
        allowHTML: true,
        theme: "q",
      });

      // rome-ignore lint/js/noUndeclaredVariables
      tippy(".label-n", {
        trigger: "long-press",
        placement: "bottom",
        content:
          spanLowerPicker +
          spanHigherPicker +
          spanMusicPicker +
          spanQuietPicker,
        allowHTML: true,
        theme: "n",
      });
    }

    function filterTiming() {
      let inputElements = document.getElementsByClassName("filterCheckbox");
      let result = [];

      if (typeof allTimings != "undefined") {
        allTimings.forEach((element) => {
          Array.from(inputElements).forEach((input) => {
            if (input.checked === true) {
              if (input.value === element[0]) {
                result.push(element);
              }
            }
          });
        });
        activeTimings = result;
      }
    }
  };

  function addUrlParam(key, val) {
    let newParam = `${key}=${val}`;
    let params = newParam;

    let exactMatch = false;
    let search = document.location.hash;

    if (search) {
      // Try to replace an existance instance
      params = search.replace(new RegExp(`([#&])${key}[^&]*`), `$1${newParam}`);

      if (search.endsWith(newParam)) {
        exactMatch = true;
      }

      if (search.indexOf(`${newParam}&`) >= 0) {
        exactMatch = true;
      }

      // If nothing was replaced OR an exact match wasn't found, then add the new param to the end
      if (params === search && exactMatch === false) {
        params += `&${newParam}`;
      }
    }
    document.location.hash = params;
  }

  function getYouTubeId(url) {
    var regExp =
      /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    var match = url.match(regExp);
    return match && match[7].length == 11 ? match[7] : false;
  }

  // https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url

  window.onload = function () {
    //fetch("test.json").then((response) => response.json()).then((json) => {
    // SXG4KdstVw4
    // j0seO3yo504
    // rgldcSmxY5o
    // DqH-iwA0ZmU
    // 7I6dSSmrwEg
    // 4mHq6Y7JSmg
    // looRuovPcbg
    // Tn5uyhySpuc
    // dFCbJmgeHmA
    // --P6IGVLVZo
    // jomcECjuYa0
    // v-xh_gq8sbk
    // cPyXP-wb2RM

    //fetch("https://a4yxhpkq3n.us-east-1.awsapprunner.com/api?url=www.youtube.com/watch%3Fv%3DDqH-iwA0ZmU").then((response) => response.json()).then((json) => {
    /*fetch("http://localhost:8080/api?url=www.youtube.com/watch%3Fv%3DlooRuovPcbg").then((response) => response.json()).then((json) => {
      skyppy(json.data);
    });*/

    if (window.location.hash.length > 0) {
      hashArray.forEach((hash) => {
        let keyval = hash.split("=");
        console.log("looking for youtube id");

        // check for youtube id
        if (keyval[0] === "v") {
          let searchUrl = "https://www.youtube.com/watch?" + hash;
          console.log(searchUrl);
          document.getElementById("box-search").value = searchUrl;
        }
      });
      getVideoData();
    }

    document
      .getElementById("button-search")
      .addEventListener("click", function (event) {
        getVideoData();
        event.preventDefault();
        return false;
      });

    //console.log("calling loadData...");
    //loadData("d_Hfal3unHE");
  };

  function getVideoData() {
    console.log("searching........");

    let player = null;

    // disable button, hide search graphic and show spinner

    document.querySelector(".fa-search").style.display = "none";
    document.querySelector("#button-search").disabled = true;
    document.querySelector(".spinner").style.display = "block";

    let searchBox = document.getElementById("box-search");
    let searchStr = searchBox.value;
    console.log(searchStr.len);
    if (searchStr === "") {
      console.log("zero length");
      searchStr = searchBox.getAttribute("placeholder");
    }
    console.log(searchStr);

    if (player !== null) {
      player.destroy();
    }
    let youTubeId = getYouTubeId(searchStr);
    document
      .getElementById("player")
      .setAttribute("data-plyr-embed-id", youTubeId);

    addUrlParam("v", youTubeId);

    let controls = [
      "play-large", // The large play button in the center
      "current-time", // The current time of playback
    ];

    player = new Plyr("#player", { controls });

    console.log("calling loadData...");
    loadData(youTubeId, player);
  }

  async function loadData(youTubeId, player) {
    console.log("in loadData...");

    //let loadProgress = 0;
    let tl = document.getElementById("timeline");
    tl.innerHTML = "";

    console.log(
      "trying " + `${api_url}api?url=www.youtube.com/watch%3Fv%3D` + youTubeId
    );

    //document.getElementById("timeline").innerHTML =
    // "Calculating. Please wait ...";

    // rimoso temporaneamente
    // const response = await fetchWithTimeout(
    //   `${api_url}api?url=www.youtube.com/watch%3Fv%3D` +
    //     youTubeId,
    //   {
    //     //const response = await fetchWithTimeout('http://localhost:8080/api?url=www.youtube.com/watch%3Fv%3DdFCbJmgeHmA', {

    //     timeout: 3000,
    //   }
    // );

    console.log("duration");
    console.log(player.duration);

    console.log("grabbing json...*.*!!!");

    let segmenterStr = "Segmenting";

    const poll = setInterval(function () {
      console.log("in setTimeout");
      fetch(`${api_url}api/status/${youTubeId}`)
        .then((response) => response.json())
        .then((data) => {
          //ina_skyppy_status = data;
          console.log("ina_skyppy_status");
          console.log(data);
          if (data.status_description === "complete") {
            clearInterval(poll);
            player.on("ready", () => {
              player.toggleControls(false);
            });
            //
          }

          if (data.status_description === "too long") {
            tl.innerHTML = `<div class="label-h" style="width:100%; color:red; padding-top:20px">"the video is too long - the online version only supports videos up to ${max_video_lenght_in_minutes} minutes long"</div>`;
          }

          if (data.status_description === "download") {
            tl.innerHTML = `<div class="label-loader" style="width:${data.percent_str}"></div>`;
          }

          if (data.status_description === "segmenter") {
            segmenterStr += ".";
            tl.innerHTML = `<div class="label-h" style="width:100%; color:#fff; padding-left:40%; padding-top:20px">${segmenterStr}</div>`;
          }
        });
    }, 1000);

    fetch(`${api_url}api?url=www.youtube.com/watch?v=${youTubeId}`)
      .then((response) => {
        response.json();
      })
      .then((data) => {
        ina_skyppy_data = data;
      })
      .then((another_fetch) =>
        fetch(`${api_url}api/status/${youTubeId}`)
          .then((response) => response.json())
          .then((data) => {
            ina_skyppy_data = data;
          })
          .then((data) => {
            countinua();
          })
      );

    function countinua() {
      const json = ina_skyppy_data;
      console.log("mio check", json);
      console.log("first json status");
      //alert("test");
      player.currentTime = 0;
      skyppy(json.data, player);
    }

    async function fetchWithTimeout(resource, options) {
      console.log("in fetch");
      const { timeout = 8000 } = options;

      const controller = new AbortController();
      const id = setTimeout(() => controller.abort(), timeout);

      const response = await fetch(resource, {
        ...options,
        signal: controller.signal,
      });
      clearTimeout(id);

      console.log(response);

      return response;
    }
  }
}
