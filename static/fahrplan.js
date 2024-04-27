async function search(event) {
    event.preventDefault()  // disable submit button
    let data = new FormData(this)
    console.log(data)

    let params = new URLSearchParams(data)
    let url = "/query?" + params

    const response = await fetch(url);
    let results = document.querySelector('#status')
    if (!response.ok) {
        results.innerText = `No response from server: ${response.statusText}`
        return
    }
    results.innerText = `${response.statusText}`

}

document.querySelector('#query').addEventListener("submit", search)