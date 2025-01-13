const form = document.querySelector('.add-article-form')

form.addEventListener('submit', async (event) => {
    event.preventDefault()

    const formData = new FormData(form)

    try {
        await fetch(form.action, {
            method: form.method,
            body: formData
        })
    } catch (error) {
        console.log(`Ошибка сети: ${error.message}`)
    }
})
