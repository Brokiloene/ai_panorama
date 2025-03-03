function refreshDialogButtonOptions() {
    const openDialogBtns = document.querySelectorAll('.open-dialog')
    const closeDialogBtns = document.querySelectorAll('.close-dialog')

    openDialogBtns.forEach(el => {
        el.addEventListener('click', () => {
            document.body.classList.add('disable-scroll')
        })
    })

    closeDialogBtns.forEach(el => {
        el.addEventListener('click', () => {
            document.body.classList.remove('disable-scroll')
        })
    })
}

refreshDialogButtonOptions()
const container = document.querySelector('.grid-container') 
const URL = '/articles?start_id='

function getLastNewsId() {
    const data = container.querySelector(".item-wrapper:last-of-type").id
    console.log(data)
    return data
}

async function loadNewsBatch(lastNewsId) {
    const raw_result = await fetch(`${URL}${lastNewsId}`)
    let data = ""
    if (raw_result.status !== 204) {
        data = await raw_result.json()
    }
    return data
}

let isLoading = false;
const sentinel = document.querySelector('#sentinel');

const observer = new IntersectionObserver(async (entries) => {
    if (entries[0].isIntersecting && !isLoading) {
        isLoading = true;
        const lastNewsId = getLastNewsId();
        const data = await loadNewsBatch(lastNewsId);
        if (data.length !== 0) {
            container.insertAdjacentHTML("beforeend", data);
            refreshDialogButtonOptions();
        }
        isLoading = false;
    }
});
observer.observe(sentinel);

