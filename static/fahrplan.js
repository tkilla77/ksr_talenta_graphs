async function search(event) {
    // disable submit button normal action
    event?.preventDefault()

    // get user choice from the form
    let form = document.querySelector('#query')

    let params = new URLSearchParams()
    params.set('from', form.querySelector('#from').value)
    params.set('to', form.querySelector('#to').value)
    params.set('algo', form.querySelector('#algo').value)
    
    // send user data to server
    let url = "/query?" + params
    const response = await fetch(url)

    // update our own URL params to make a nice perma-URL
    // see https://stackoverflow.com/questions/3338642/updating-address-bar-with-new-url-without-hash-or-reloading-the-page
    let location = new URL(window.location.href)
    for (let param of params) {
        location.searchParams.set(param[0], param[1])
    }
    history.pushState({}, null, location)

    // update UI to match response
    let status = document.querySelector('#status')
    let route = document.querySelector('#stops')
    if (response.ok) {
        let routeInfo = await response.json()
        status.innerText = `${response.statusText}, duration: ${routeInfo.duration.toPrecision(2)}s`
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

document.querySelector('#search').addEventListener("click", search)

// Read our own URL params and update the form accordingly
// Also run a search if both from and to are given.
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

async function updateStops() {
    // Read the set of possible stops to populate the suggestions
    let url = "/allstops"
    const response = await fetch(url)
    if (response.ok) {
        const stops = await response.json()
        let list = document.querySelector('#stops-list')
        list.innerHTML = ''
        for (let stop of stops) {
            let option = document.createElement('option')
            option.value = stop
            list.appendChild(option)
        }
    } else {
        console.log(response)
    }
}

updateStops()