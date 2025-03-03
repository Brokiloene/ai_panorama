const genTitleBtn = document.querySelector(".gen-title-btn")
const titleInput = document.querySelector("#title")
genTitleBtn.addEventListener('click', async () => {
  const URL = '/ai-gen/article-headline?prompt='
  const response = await fetch(`${URL}${titleInput.value}`)
  if (response.status == 500) {
    data = "Не удалось сгенерировать :("
  } else {
    data = await response.text()
  }  console.log(data)
  titleInput.value = data
})

const genArticleBtn = document.querySelector(".gen-article-btn")
const articleInput = document.querySelector("#article_text")
genArticleBtn.addEventListener('click', async () => {
  const URL = '/ai-gen/article-body?prompt='
  const response = await fetch(`${URL}${articleInput.value}`)
  let data = ""
  if (response.status == 500) {
    data = "Не удалось сгенерировать :("
  } else {
    data = await response.text()
  }
  console.log(data)
  articleInput.value = data
})

window.URL = window.URL || window.webkitURL

const genImageBtn = document.querySelector(".gen-image-btn")
const sendArticleBtn = document.querySelector(".send-article")
const imgElement = document.querySelector(".article-image")
const formElement = document.querySelector(".add-article-form")

let imageBlob = null

genImageBtn.addEventListener('click', async () => {
  sendArticleBtn.disabled = true

  try {
    const URL = '/ai-gen/article-thumbnail'
    const response = await fetch(`${URL}${titleInput.value}${articleInput.value}`)
    if (!response.ok) {
      console.error("Ошибка при получении изображения:", response.statusText)
      return
    }

    imageBlob = await response.blob()
    const imageUrl = window.URL.createObjectURL(imageBlob)
    
    imgElement.src = imageUrl
    imgElement.classList.remove("hidden")

    sendArticleBtn.disabled = false
  } catch (error) {
    console.error("Ошибка при запросе к /gen-image:", error)
  }
})

formElement.addEventListener('submit', async (event) => {
  event.preventDefault()

  try {
    const formData = new FormData(formElement)
    if (imageBlob) {
      formData.append("image", imageBlob, "generated-image.png")
    }

    const response = await fetch(formElement.action, {
      method: formElement.method,
      body: formData
    })

    if (!response.ok) {
      console.error("Ошибка при отправке формы:", response.statusText)
      return
    }

    const result = await response.json()
    console.log("Сервер ответил:", result)

  } catch (error) {
    console.error("Ошибка при отправке формы:", error)
  }
})
