document.addEventListener('DOMContentLoaded', async () => {
    document.addEventListener('keydown', function (event) {
        if (event.key === 'F5' || event.key === 'Escape') {
            event.preventDefault();
            window.location.href = '/upload';
        }
    });
    const fileListWrapper = document.getElementById('file-list-wrapper');
    const uploadRedirectButton = document.getElementById('upload-tab-btn');

    const updateTabStyles = () => {
        const uploadTab = document.getElementById('upload-tab-btn');
        const imagesTab = document.getElementById('images-tab-btn');

        const isImagesPage = window.location.pathname.includes('images');

        uploadTab.classList.remove('upload__tab--active');
        imagesTab.classList.remove('upload__tab--active');

        if (isImagesPage) {
            imagesTab.classList.add('upload__tab--active');
        } else {
            uploadTab.classList.add('upload__tab--active');
        }
    };

    const displayFiles = async () => {
        const urlParams = new URLSearchParams(window.location.search);
        const page = urlParams.get('page') || 1;
        const response =
            await fetch(`/api/images-data?page=${page}`)
                .then(res=>res.json())

        const storedFiles = response.images

        const prevPage = document.getElementById('prev-page-btn');
        const nextPage = document.getElementById('next-page-btn');
        prevPage.href = `/images?page=${Number(page) - 1}`
        nextPage.href = `/images?page=${Number(page) + 1}`
        prevPage.disabled = Number(page) === 1

        const currentPage = document.getElementById('current-page-btn')
        currentPage.innerText = page;
        fileListWrapper.innerHTML = '';

        if (storedFiles.length === 0) {
            fileListWrapper.innerHTML = '<p class="upload__promt" style="text-align: center; margin-top: 50px;">No images uploaded yet.</p>';
        } else {
            const container = document.createElement('div');
            container.className = 'file-list-container';
            const header = document.createElement('div');
            header.className = 'file-list-header';
            header.innerHTML = `
                <div class="file-col file-col-image">Image</div>
                <div class="file-col file-col-name">Name</div>
                <div class="file-col file-col-size">Size</div>
                <div class="file-col file-col-url">Url</div>
                <div class="file-col file-col-type">Type</div>
                <div class="file-col file-col-delete">Delete</div>
            `;
            container.appendChild(header);

            const list = document.createElement('div');
            list.id = 'file-list';

            storedFiles.forEach((image) => {
                const imageUrl = `${window.location.origin}/images/${image.filename}.${image.file_type}`
                const fileItem = document.createElement('div');
                fileItem.className = 'file-list-item';
                fileItem.innerHTML = `
                    <div class="file-col file-col-image">
                        <span class="file-icon">
                        <img src="${imageUrl}" alt="file icon" width="50">
                        </span>
                    </div>
                    <div class="file-col file-col-name">
                        <span class="file-name">${image.original_name}</span>
                    </div>
                    <div class="file-col file-col-size">
                        <span class="file-name">${image.size}KB</span>
                    </div>
                    <div class="file-col file-col-url">
                        <a href="${imageUrl}" target="_blank">
                            ${imageUrl}
                        </a>
                    </div>
                    <div class="file-col file-col-type">
                        <span class="file-name">${image.file_type}</span>
                    </div>
                    <div class="file-col file-col-delete">
                        <button class="delete-btn" data-filename="${image.filename}.${image.file_type}">
                            <img src="/static/image-uploader/img/icon/delete.png" alt="delete icon">
                        </button>
                    </div>
                `;
                list.appendChild(fileItem);
            });

            container.appendChild(list);
            fileListWrapper.appendChild(container);
            await addDeleteListeners();
        }

        updateTabStyles();
    };

    const addDeleteListeners = async () => {
        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', async (event) => {
                const filename = event.currentTarget.dataset.filename;
                await fetch(`/api/images/${filename}`, {
                    method: 'DELETE',
                })
                    .then(() => displayFiles())
                    .catch(error => console.error("Error deleting image:", error));
            });
        });
    };

    if (uploadRedirectButton) {
        uploadRedirectButton.addEventListener('click', () => {
            window.location.href = '/upload';
        });
    }

    displayFiles();
});