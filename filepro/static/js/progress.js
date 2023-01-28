class PBar {
    constructor(containerEl) {
        this.containerEl = containerEl;

        this.barBgEl = document.createElement("div");
        this.barBgEl.classList.add("progress");
        this.barBgEl.style.height = "inherit";

        this.barEl = document.createElement("div");
        this.barEl.classList.add("progress-bar");
        this.barEl.style.width = "0%";
        this.barEl.innerHTML = "0%";
        this.barEl.color = "#0d6efd";
        this.barEl.style.height = "inherit";

        this.barBgEl.appendChild(this.barEl);
        this.containerEl.appendChild(this.barBgEl);

        this._relProgress = 0;
        this._color = "#0d6efd";

        this.isVisible = true;
    }

    setRelProgress(p) {
        this.barEl.style.width = `${p}%`;
        this.barEl.innerHTML = `${p}%`;
        this._relProgess = p;
    }

    setColor(color) {
        this.barEl.style.backgroundColor = color;
        this._color = color;
    }

    toggleVisible() {
        if (this.containerEl.style.display == "none") {
            this.containerEl.style.display = "block";
            this.isVisible = true;
        } else {
            this.containerEl.style.display = "none";
            this.isVisible = false;
        }
    }

    remove() {
        this.barBgEl.remove()
    }
}

class UrlField {
    constructor(containerEl, url) {
        this.url = url;

        this.containerEl = containerEl;

        this.groupEl = document.createElement("div");
        this.groupEl.classList.add("input-group");

        this.copyBtn = document.createElement("button");
        this.copyBtn.classList.add(
            "btn", "btn-black", "text-white",
            "border-1", "border-white", "rounded-start"
        );
        let icon = document.createElement("i");
        icon.classList.add("fa-solid", "fa-copy");
        this.copyBtn.appendChild(icon);

        this.urlField = document.createElement("input");
        this.urlField.classList.add(
            "form-control", "rounded-end", "bg-dark", "text-white"
        );
        this.urlField.readOnly = true;
        this.urlField.value = this.url ? this.url : "";

        this.groupEl.appendChild(this.copyBtn);
        this.groupEl.appendChild(this.urlField);

        this.containerEl.appendChild(this.groupEl);

        this.copyBtn.addEventListener("click",() => this.copyUrl());

        this.isVisible = true;
    }

    setUrl(url) {
        this.urlField.value = url;
        this.url = url;
    }

    copyUrl() {
        this.urlField.select();
        this.urlField.setSelectionRange(0, 99999);

        navigator.clipboard.writeText(this.url);

        // Bootstrap Tooltip Fuckery

        let bsToolTip = new bootstrap.Tooltip(this.urlField, {
            placement: "bottom",
            title: "Copied!"
        } );

        bsToolTip.show();
        bsToolTip.toggleEnabled();

        setTimeout(_ => {
            bsToolTip.toggleEnabled();
            bsToolTip.hide();
            bsToolTip.dispose();
        }, 700)
    }

    toggleVisible() {
        if (this.containerEl.style.display == "none") {
            this.containerEl.style.display = "block";
            this.isVisible = true;
        } else {
            this.containerEl.style.display = "none";
            this.isVisible = false;
        }
    }

    remove() {
        this.groupEl.remove();
    }
}

class Uploader {
    constructor(endpoint, containerEl, fileInputEl) {
        this.endpoint = endpoint;

        this.containerEl = containerEl;
        this.fileInputEl = fileInputEl;

        let pBarCont =  document.createElement("div");
        pBarCont.style.height = "30px";
        this.pBar = new PBar(pBarCont);
        this.pBar.toggleVisible();

        this.errorEl = document.createElement("code");
        this.errorEl.style.color = "white";
        this.errorEl.style.display = "none";

        this.fileNameEl = document.createElement("span");

        let urlFieldCont = document.createElement("div");
        this.urlField = new UrlField(urlFieldCont);
        this.urlField.toggleVisible();

        this.containerEl.appendChild(pBarCont);
        this.containerEl.appendChild(this.errorEl);
        this.containerEl.appendChild(this.fileNameEl);
        this.containerEl.appendChild(urlFieldCont);
    }

    #setup() {
        this.pBar.setRelProgress(0);
        this.pBar.setColor("#0d6efd");
        if (!this.pBar.isVisible) {
            this.pBar.toggleVisible();
        }

        this.urlField.setUrl("");
        if (this.urlField.isVisible) {
            this.urlField.toggleVisible();
        }

        this.errorEl.style.display = "none";
        this.fileNameEl.innerHTML = "";
    }

    async upload() {
        this.#setup();

        let files = this.fileInputEl.files;
        let form = new FormData();
        form.append('file', files[0]);

        let req = await axios.post(this.endpoint, form, {
            onUploadProgress: (p) => {
                this.pBar.setRelProgress(
                    (Math.round((p.loaded * 100) / p.total))
                );
            }
        })

        let data = await req.data;

        if (!data.error) {
            this.pBar.setRelProgress(100);
            this.pBar.toggleVisible();
            this.urlField.setUrl(data.full_url);
            this.urlField.toggleVisible();
            this.fileNameEl.innerHTML = data.filename;
        } else {
            this.pBar.setRelProgress(100);
            this.pBar.setColor("#dc3545");
            this.errorEl.innerHTML = "Error: "  + data.error;
            this.errorEl.style.display = "block";
        }
    }



    toggleVisible() {
        if (this.containerEl.style.display == "none") {
            this.containerEl.style.display = "block";
            this.isVisible = true;
        } else {
            this.containerEl.style.display = "none";
            this.isVisible = false;
        }
    }

    remove() {
        while (this.containerEl.firstChild) {
            this.containerEl.remove();
        }
    }
}