const token = prompt("Input the password")
const ws = new WebSocket(`ws://${location.hostname}:8000/ws/${token}`)
ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    let point = {}
    players.forEach(item => {
        point[item] = 5
    })
    data.reverse()
    let html_logs = ""
    data.forEach(item => {
        point[item[0]]++
        point[item[1]]--
        html_logs += `<div class="alert alert-danger" role="alert">${item[0]} killed ${item[1]} at ${item[2]} </div>`
    })
    point = Object.entries(point).sort(([, a], [, b]) => b - a)
    let html = ""
    point.forEach(item => {
        html += `<li><mark>${item[0]}</mark><small>${item[1]}</small></li>`
    })
    document.getElementById("points").innerHTML = html
    document.getElementById("logs").innerHTML = html_logs
}
ws.onclose = () => {
    alert("Disconnect to server socket")
}