const genTitleBtn = document.querySelector(".gen-title-btn")
const titleInput = document.querySelector("#title")
genTitleBtn.addEventListener('click', async () => {
  const response = await fetch("/gen-title")
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
  const response = await fetch("/gen-article")
  let data = ""
  if (response.status == 500) {
    data = "Не удалось сгенерировать :("
  } else {
    data = await response.text()
  }
  console.log(data)
  articleInput.value = data
})

window.URL = window.URL || window.webkitURL;
const genImageBtn = document.querySelector(".gen-image-btn")
const img = document.querySelector(".article-image")
let base64Img = ""

genImageBtn.addEventListener('click', async () => {
  document.querySelector(".send-article").disabled = true;
  const response = await fetch("/gen-image")
  console.log(response.ok);
  const imageBlob = await response.blob();
  console.log(imageBlob);
  await new Promise((resolve) => setTimeout(resolve, 100));
  const imageUrl = window.URL.createObjectURL(imageBlob)

  console.log(imageUrl)
  img.src = imageUrl
  img.classList.remove("hidden")

  const convertBlobToBase64 = (blob) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result);
      reader.onerror = (error) => reject(error);
      reader.readAsDataURL(blob);
    });
  };

  base64Img = await convertBlobToBase64(imageBlob);
  await new Promise((resolve) => setTimeout(resolve, 100));
  document.querySelector(".send-article").disabled = false;
})

const formElement = document.querySelector(".add-article-form")
const hiddenInput = document.querySelector("#image")
formElement.addEventListener('submit', () => {
  hiddenInput.value = base64Img
})
