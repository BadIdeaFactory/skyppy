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
      return "default label";
    }
  }

  let soundLabel = {
    l: ["lower voice", urlmatch(/l=([^&]+)/), getSArgumentString.includes("l")],
    h: [
      "higher voice",
      urlmatch(/h=([^&]+)/),
      getSArgumentString.includes("h"),
    ],
    q: ["quiet", urlmatch(/q=([^&]+)/), getSArgumentString.includes("q")],
    n: ["noise", urlmatch(/n=([^&]+)/), getSArgumentString.includes("n")],
    m: ["music", urlmatch(/m=([^&]+)/), getSArgumentString.includes("m")],
  };

  // Get the value of the "arg1" parameter

  return soundLabel;
}

function renderSoundLabel(soundLabel) {
  return JSON.stringify(soundLabel);
}

/**
 *
 * @param {object} option [contain url and other variables ]
 * @param {object} data [contain stats data ]
 * @return {NULL}
 *
 */
function main(option, data) {
  console.log(option, data);

  let entries = Object.entries(data["video_link_openings"]);
  let sorted = entries.sort((a, b) => a[1] - b[1]);
  let video_link_openings = sorted.reverse();
  let total_requests = data["total_requests"];
  console.log(total_requests, video_link_openings);

  let totalRequests = document.getElementById("total-requests");
  let skyppyedVideos = document.getElementById("skyppyed-videos");

  totalRequests.innerHTML = total_requests;

  function render_video(video_link_openings_element) {
    console.log(video_link_openings_element);
    let li = document.createElement("li");
    let video = document.createElement("a");
    let thumbnail = document.createElement("img");

    let domain = new URL(location);
    const protocol = domain.protocol;
    // video.href =
    //   protocol + "//" + domain.host + "/#v=" + video_link_openings_element[0];
    // video.innerText = `${video.href} - visualization: ${video_link_openings_element[1]}`;
    // let thumbnail_url = `https://img.youtube.com/vi/${video_link_openings_element[0]}/maxresdefault.jpg`;
    // thumbnail.src = thumbnail_url;
    // thumbnail.classList.add("responsive-img");

    // li.appendChild(video);
    // li.appendChild(thumbnail);
    // return li;

    let tr = document.createElement("tr");
    let videoTd = document.createElement("td");
    let thumbnailTd = document.createElement("td");

    video.href = video_link_openings_element[0];
    let soundLabel = getSoundLabel(video.href);
    video.innerText = `visualization: ${
      video_link_openings_element[1]
    } + filter: ${renderSoundLabel(soundLabel)}`;

    let thumbnail_url = `https://img.youtube.com/vi/${getYouTubeId(
      video_link_openings_element[0]
    )}/maxresdefault.jpg`;
    thumbnail.src = thumbnail_url;
    thumbnail.classList.add("responsive-img");

    videoTd.appendChild(video);
    thumbnailTd.appendChild(thumbnail);
    tr.appendChild(thumbnailTd);
    tr.appendChild(videoTd);

    return tr;
  }

  video_link_openings.forEach((video_link_openings_element) => {
    skyppyedVideos.appendChild(render_video(video_link_openings_element));
  });
}
