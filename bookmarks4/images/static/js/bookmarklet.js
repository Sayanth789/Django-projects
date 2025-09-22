const siteUrl = '//127.0.0.1:8000';
const styleUrl = siteUrl + '/static/css/bookmarklet.css';
const minWidth = 250;
const minHeight = 250;

// load the CSS
var head = document.getElementsByTagName('head')[0];
var link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = styleUrl + '?r=' + Math.floor(Math.random() * 9999999999999999);
head.appendChild(link);


// load HTML

var body = document.getElementsByTagName('body')[0];
boxHtml = ` 
    <div id="bookmarklet">
        <a href="#" id="close">&times;</a>
        <h1>Select an image to the bookmark:</h1>
        <div class="images"></div>
    </div>`;
body.innerHTML += boxHtml;


function bookmarkletLaunch(){
    bookmarklet = document.getElementById('bookmarklet');
    var imagesFound = bookmarklet.querySelector('.images');


    // clear images found.
    imagesFound.innerHTML = '';

    // display bookmarklet
    bookmarklet.style.display = 'block';
    // close event
    bookmarklet.querySelector('#close').addEventListener('click', function(){
        bookmarklet.style.display = 'none'
    }); 

    // Find images in the DOM with the minimum dimension.

    images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"],img[src$=".png"]');
    images.forEach(image => {
        if (image.naturalWidth >= minWidth && image.naturalHeight >= minHeight)
        {
            var imageFound = document.createElement('img');
            imageFound.src = image.src;
            imagesFound.append(imageFound);
        }
    })

    // select image event 
    imagesFound.querySelectorAll('img').forEach(image=>{
        image.addEvenetListener('click', function(event) {
            imagesSelected = event.target;
            bookmarklet.style.display = 'none';
            window.open(siteUrl + 'images/create/?url=' 
            + encodeURIComponent(imageSelected.src)
            + '&title='
            + encodedURIComponent(document.title),
            '_blank');
        })
    })

}

// Launch he bookmarklet
bookmarkletLaunch();

function bookmarkletLaunch() {
    bookmarklet = document.getElementById('bookmarklet');
    var imagesFound = bookmarklet.querySelector('.images');

    // clear images found.
    imagesFound.innerHTML = '';
    // display bookmarklet 
    bookmarklet.style.diaplay = 'block';
    // close  event
    bookmarklet.querySelector('#close').addEventListener('click', function() {
        bookmarklet.style.display = 'none'
    });

    // find images in the DOM with the minimum dimensions.
    images = document.querySelectorAll('img[src$=".jsp"],img[src$=."jpeg"],img[src$=".png"]');
    images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"],img[src$=".png"]');
    images.forEach(image => {
        if(image.naturalWidth > minWidth
            && image.naturalHeight >= minHeight)
             {
                var imageFound = document.createElement('img');
                imageFound.src = image.src;
                imagesFound.append(imageFound);    
            }
    })

    // Select the image event.
    imagesFound.querySelectorAll('img').forEach(image => {
        image.addEvenetListener('click', function(event) {
            imageSelected = event.target;
            bookmarklet.style.display = 'none';
            window.open(siteUrl + 'images/create/?url=' + encodeURICompenent(imageSelected.src)
        + '&title='
        + encodeURIComponent(document.title),
        '_blank');
        })
    })
}    

// Launch the bookmarklet 
bookmarkletLaunch();

// In the above a click() event is attached to each image element within the imagesFound container.

// When user click any of the images, the image element clicked is stored in the variable imageSelected.

// The bookmarklet is then hidden by setting its display property to none. etc.
