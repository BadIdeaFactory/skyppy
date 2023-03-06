function getYouTubeId(url) {
  //get the v argument from the url
  let v = url.match(/v=([^&]+)/)[1];
  return v;
}

function getSArgument(url) {
  //get the s argument from the url
  try {
    let s = url.match(/s=([^&]+)/)[1];
    return s;
  } catch (error) {
    return "avoid";
  }
}

/**
 * get label from url attributes
 * url
 */
function getSoundLabel(url) {
  let getSArgumentString = getSArgument(url);
  console.log(getSArgumentString);
  function urlmatch(regex) {
    try {
      return url.match(regex)[1];
    } catch (error) {
      return false;
    }
  }

  let soundLabel = {
    l: {
      label: "lower voice",
      custom: urlmatch(/l=([^&]+)/),
      active: getSArgumentString.includes("l"),
      css: "btn-lower",
    },
    h: {
      label: "higher voice",
      custom: urlmatch(/h=([^&]+)/),
      active: getSArgumentString.includes("h"),
      css: "btn-higher",
    },
    q: {
      label: "quiet",
      custom: urlmatch(/q=([^&]+)/),
      active: getSArgumentString.includes("q"),
      css: "btn-quiet",
    },
    n: {
      label: "noise",
      custom: urlmatch(/n=([^&]+)/),
      active: getSArgumentString.includes("n"),
      css: "btn-noise",
    },
    m: {
      label: "music",
      custom: urlmatch(/m=([^&]+)/),
      active: getSArgumentString.includes("m"),
      css: "btn-music",
    },
  };

  // Get the value of the "arg1" parameter

  return soundLabel;
}

/**
 *
 * @param {object} option [contain url and other variables ]
 * @param {object} data [contain stats data ]
 * @return {NULL}
 *
 */
function main(option, data) {
  //console.log(option, data);

  let entries = Object.entries(data["video_link_openings"]);
  let sorted = entries.sort((a, b) => a[1] - b[1]);
  let video_link_openings = sorted.reverse();
  let total_requests = data["total_requests"];
  //console.log(total_requests, video_link_openings);

  let totalRequests = document.getElementById("total-requests");
  let skyppyedVideos = document.getElementById("skyppyed-videos");

  totalRequests.innerHTML = total_requests;

  function render_video(video_link_openings_element) {
    //console.log(video_link_openings_element);
    let li = document.createElement("li");
    let video = document.createElement("a");

    //let domain = new URL(location);
    //const protocol = domain.protocol;

    let tr = document.createElement("tr");
    let thumbnailTd = document.createElement("td");

    video.href = video_link_openings_element[0];
    let soundLabel = getSoundLabel(video.href);

    let thumbnail_url = `https://img.youtube.com/vi/${getYouTubeId(
      video_link_openings_element[0]
    )}/sddefault.jpg`;

    let thumbnail = `<a href="${video.href}"><img class="responsive-img" src="${thumbnail_url}" /></a>`;

    thumbnail.src = thumbnail_url;

    thumbnailTd.innerHTML = thumbnail;
    tr.appendChild(thumbnailTd);

    Object.keys(soundLabel).forEach((els, val) => {
      console.log(els);
      console.log(val);
      let el = soundLabel[els];
      console.log(el);
      let voice = document.createElement("td");
      let vSelect = "deselected";
      let vOpacity = "0.3";

      if (el.active === true) {
        vSelect = "";
        vOpacity = "1";
      }

      let vLabel = el.label;
      if (el.custom !== false) {
        vLabel = decodeURI(el.custom);
      }

      voice.innerHTML = `<label><span style="white-space: nowrap" id="checkname-${els}" class="checkname ${vSelect}">${vLabel}</span><i id="${el.css}" style="height:0; opacity:${vOpacity};"></i></label>`;

      tr.appendChild(voice);
    });

    let hits = document.createElement("td");
    hits.innerHTML =
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg>' +
      video_link_openings_element[1];

    tr.appendChild(hits);

    return tr;
  }

  video_link_openings.forEach((video_link_openings_element) => {
    skyppyedVideos.appendChild(render_video(video_link_openings_element));
  });
}
