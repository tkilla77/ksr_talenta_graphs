async function search(event) {
    event.preventDefault()  // disable submit button
    let data = new FormData(this)
    console.log(data)

    let params = new URLSearchParams(data)
    let url = "/query?" + params

    const response = await fetch(url);
    let status = document.querySelector('#status')
    let route = document.querySelector('#stops')
    if (!response.ok) {
        route.innerHTML = ""
        let text = await response.text()
        status.innerText = `No response from server: ${response.statusText}, ${text}`
        return
    }
    status.innerText = `${response.statusText}`
    let stops = await response.text()

    route.innerText = stops.toString()
}

document.querySelector('#query').addEventListener("submit", search)