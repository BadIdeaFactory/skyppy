fetch("http://0.0.0.0:8080/api?url=www.youtube.com/watch?v=YLslsZuEaNE").then(response => response.json()).then(data => console.log(data))
.then(another_fetch => fetch("http://0.0.0.0:8080/api/status/YLslsZuEaNE").then(response => response.json()).then(data => console.log(data)))
