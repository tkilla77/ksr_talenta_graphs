async function search(event) {
    // disable submit button normal action
    event?.preventDefault()

    // get user choice from the form
    let form = document.querySelector('#query')
    let data = new FormData(form)

    // send user data to server
    let params = new URLSearchParams(data)
    let url = "/query?" + params
    const response = await fetch(url);

    // update our own URL params to make a nice perma-URL
    let location = new URL(window.location.href)
    for (let param of params) {
        location.searchParams.set(param[0], param[1])
    }
    history.pushState({}, null, location)

    // update UI to match response
    let status = document.querySelector('#status')
    let route = document.querySelector('#stops')
    if (response.ok) {
        status.innerText = `${response.statusText}`
        let routeInfo = await response.json()
        route.innerText = `Die Fahrzeit von ${params.get('from')} nach ${params.get('to')} beträgt ${routeInfo.length} Minuten.`
        for (let stop of routeInfo.path) {
            route.innerHTML += `<my-stop>${stop[0]}: ${stop[1]}m</my-stop>`
        }
    } else {
        route.innerHTML = ""
        let text = await response.text()
        status.innerText = `No response from server: ${response.statusText}, ${text}`
    }
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