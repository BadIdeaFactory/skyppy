let skyppy = function(allTimings) {
	let index = 0;
	let margin = 0.1;
	let activeTimings = 0;
	// rome-ignore lint/js/noUndeclaredVariables
	let player = new Plyr("#player");

	player.on(
		"play",
		() => {
			player.play();
			requestAnimationFrame(timeUpdate);
		},
	);

	filterTiming();

	function timeUpdate() {
		let position = player.currentTime * (timeline.clientWidth / player.duration);
		document.getElementById("progress-marker").style.marginLeft = `${position}px`;
		index = 0;

		while (player.currentTime >= activeTimings[index][2] - margin) {
			index++;
		}

		if (player.currentTime < activeTimings[index][1]) {
			// it's in a gap between active timings
			// jump to the start of the next active timing
			player.currentTime = activeTimings[index][1];
		}

		requestAnimationFrame(timeUpdate);
	}

	const hashArray = window.location.hash.substr(1).split("&");
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

	const labelEdit = document.getElementsByClassName("editCheckname");

	Array.from(labelEdit).forEach((element) => {
		element.addEventListener(
			"click",
			(event) => {
				let sibling = event.target.nextElementSibling;
				sibling.contentEditable = "true";
				sibling.focus();
				event.preventDefault();
				return false;
			},
		);
	});

	const label = document.getElementsByClassName("checkname");

	Array.from(label).forEach(addLabelListeners);

	function addLabelListeners(element, index) {
		element.addEventListener(
			"input",
			(event) => {
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
			},
		);

		element.addEventListener(
			"blur",
			(event) => {
				event.target.blur();
				event.target.contentEditable = "false";
				event.preventDefault();
				addUrlParam(labelParams[index], encodeURI(event.target.innerText));
				return false;
			},
		);

		element.addEventListener(
			"click",
			(event) => {
				if (event.target.contentEditable === "true") {
					event.preventDefault();
					return false;
				}
			},
		);
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

		element.addEventListener(
			"click",
			(event) => {
				greySwitchText(event.target);
				filterTiming();
				drawTimeline(allTimings);
				updateSwitchState();
				return false;
			},
		);
	});

	function addPickerListeners(element) {
		element.addEventListener(
			"click",
			(event) => {
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
				filterTiming();
				drawTimeline(allTimings);
				event.preventDefault();
				return false;
			},
		);
	}

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
  
	const timeline = document.getElementById("timeline");
	let lastClickedSegmentIndex = null;

	timeline.addEventListener(
		"click",
		(event) => {
			let offset =
				(document.getElementById("pagebody").clientWidth - timeline.clientWidth) /
				2;
			let newTime =
				player.duration * (event.clientX - offset) / timeline.clientWidth;
			player.currentTime = newTime;
			player.play();
			lastClickedSegmentIndex = event.target.getAttribute("data-index");
			let pickers = document.getElementsByClassName("picker");
			Array.from(pickers).forEach(addPickerListeners);
			return false;
		},
	);

	drawTimeline(allTimings);

	function drawTimeline(times) {
		let tl = document.getElementById("timeline");
		tl.innerHTML = "";
		let totalTime = times[times.length - 1][2];

		times.forEach((element, index) => {
			let widthPc = (element[2] - element[1]) / totalTime * 100;
			let label = element[0];

			let inputElements = document.getElementsByClassName("filterCheckbox");

			let matched = false;

			Array.from(inputElements).forEach((input) => {
				if (input.checked === true) {
					if (input.value === element[0]) {
						tl.insertAdjacentHTML(
							"beforeend",
							`<div class="label-${label}" style="width:${widthPc}%" data-index="${index}"></div>`,
						);
						matched = true;
					}
				}
			});

			if (matched === false) {
				tl.insertAdjacentHTML(
					"beforeend",
					`<div class="label-${label}" style="width:${widthPc}%; opacity:0.2" data-index="${index}"></div>`,
				);
			}
		});

		const spanLowerPicker = `<span title="${document.getElementById(
			"checkname-l",
		).innerText}" class="picker label-l"></span>`;
		const spanHigherPicker = `<span title="${document.getElementById(
			"checkname-h",
		).innerText}" class="picker label-h"></span>`;
		const spanMusicPicker = `<span title="${document.getElementById(
			"checkname-m",
		).innerText}" class="picker label-m"></span>`;
		const spanQuietPicker = `<span title="${document.getElementById(
			"checkname-q",
		).innerText}" class="picker label-q"></span>`;
		const spanNoisePicker = `<span title="${document.getElementById(
			"checkname-n",
		).innerText}" class="picker label-n"></span>`;

		// rome-ignore lint/js/noUndeclaredVariables
		tippy(
			".label-l",
			{
				trigger: "long-press",
				placement: "bottom",
				content: spanHigherPicker +
				spanMusicPicker +
				spanQuietPicker +
				spanNoisePicker,
				allowHTML: true,
				theme: "l",
			},
		);

		// rome-ignore lint/js/noUndeclaredVariables
		tippy(
			".label-h",
			{
				trigger: "long-press",
				placement: "bottom",
				content: spanLowerPicker +
				spanMusicPicker +
				spanQuietPicker +
				spanNoisePicker,
				allowHTML: true,
				theme: "h",
			},
		);

		// rome-ignore lint/js/noUndeclaredVariables
		tippy(
			".label-m",
			{
				trigger: "long-press",
				placement: "bottom",
				content: spanLowerPicker +
				spanHigherPicker +
				spanQuietPicker +
				spanNoisePicker,
				allowHTML: true,
				theme: "m",
			},
		);

		// rome-ignore lint/js/noUndeclaredVariables
		tippy(
			".label-q",
			{
				trigger: "long-press",
				placement: "bottom",
				content: spanLowerPicker +
				spanHigherPicker +
				spanMusicPicker +
				spanNoisePicker,
				allowHTML: true,
				theme: "q",
			},
		);

		// rome-ignore lint/js/noUndeclaredVariables
		tippy(
			".label-n",
			{
				trigger: "long-press",
				placement: "bottom",
				content: spanLowerPicker +
				spanHigherPicker +
				spanMusicPicker +
				spanQuietPicker,
				allowHTML: true,
				theme: "n",
			},
		);
	}

	function filterTiming() {
		let inputElements = document.getElementsByClassName("filterCheckbox");
		let result = [];

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
};

window.onload = function() {
	fetch("test.json").then((response) => response.json()).then((json) => {
		skyppy(json.data);
	});
};
