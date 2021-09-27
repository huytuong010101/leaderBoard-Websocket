let options = ""
players.forEach(item => {
    options += `<option value="${item}">${item}</option>`
})
document.getElementById("win-player").innerHTML = options
document.getElementById("lose-player").innerHTML = options
const token = prompt("Input the password")
const ws = new WebSocket(`ws://${location.hostname}:8000/admin/${token}`)
ws.onmessage = function (event) {
    const data = JSON.parse(event.data)
    data.reverse()
    let html = ""
    data.forEach(item => {
        html += `<li class="list-group-item list-group-item-primary">${item[0]} win ${item[1]} at ${item[2]} </li>`
    })
    document.getElementById("logs").innerHTML = html
}
ws.onclose = () => {
    alert("Disconnect to server socket")
}
document.getElementById("add-btn").onclick = () => {
    const win = document.getElementById("win-player").value
    const lose = document.getElementById("lose-player").value
    if (win == lose) {
        alert("Winner and loser must be difference")
        return
    }
    ws.send(JSON.stringify({
        "type": "add",
        "win": win,
        "lose": lose
    }))
}
document.getElementById("remove-btn").onclick = () => {
    const win = document.getElementById("win-player").value
    const lose = document.getElementById("lose-player").value
    if (win == lose) {
        alert("Winner and loser must be difference")
        return
    }
    ws.send(JSON.stringify({
        "type": "remove",
        "win": win,
        "lose": lose
    }))
}