async function search(event) {
    event.preventDefault()  // disable submit button
    let data = new FormData(this)
    console.log(data)

    const response = await fetch("query", {
        method: "POST",
        body: data,
    });
    if (!response.ok) {
        let results = document.querySelector('#route')
        results.innerText = `No response from server: ${response.statusText}`
        return
    }
    
}

document.querySelector('#query').addEventListener("submit", search)