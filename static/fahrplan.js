async function search(event) {
    event.preventDefault()  // disable submit button
    let data = new FormData(this)
    console.log(data)

    const response = await fetch("query", {
        method: "POST",
        body: data,
    });
    let results = document.querySelector('#status')
    if (!response.ok) {
        results.innerText = `No response from server: ${response.statusText}`
        return
    }
    results.innerText = `${response.statusText}`

}

document.querySelector('#query').addEventListener("submit", search)