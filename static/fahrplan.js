async function search(event) {
    event?.preventDefault()  // disable submit button
    let form = document.querySelector('#query')
    let data = new FormData(form)
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

let params = new URLSearchParams(window.location.search)
if (params) {
    let from = params.get("from")
    if (from) {
        document.querySelector("#from").value=from
    }
    let to = params.get("to")
    if (to) {
        document.querySelector("#to").value=to
    }
    let algo = params.get("algo")
    if (algo) {
        document.querySelector("#algo").value=algo
    }
    if (from && to) {
        search()
    }
}