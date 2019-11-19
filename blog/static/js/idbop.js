//Open new IndexedDB conncetion.
var dbPromise = idb.open('puydinfo-db', 5, function (upgradeDb) {
    upgradeDb.createObjectStore('spectacles', {keyPath: 'pk'});
});
//collect latest post from server and store in idb.
fetch('/getdata').then(function (response) {
    return response.json();
}).then(function (jsondata) {
    dbPromise.then(function (db) {
        var tx = db.transaction('spectacles', 'readwrite');
        var feedsStore = tx.objectStore('spectacles');
        for (var key in jsondata) {
            if (jsondata.hasOwnProperty(key)) {
                feedsStore.put(jsondata[key]);
            }
        }
    });
});
//retrive data from idb and display on page.
var post = "";
dbPromise.then(function (db) {
    var tx = db.transaction('spectacles', 'readonly');
    var feedsStore = tx.objectStore('spectacles');
    return feedsStore.openCursor();
}).then(function logItems(cursor) {
    if (!cursor) {
        //if true means we are done cursoring over all records in feeds.
        try {
            document.getElementById('offlinedata').innerHTML = post;
        } catch (e) {

        }

        return;
    }
    for (var field in cursor.value) {
        if (field == 'fields') {
            feedsData = cursor.value[field];
            for (var key in feedsData) {
                if (feedsData.type[0] == 2) {
                    var title = '<div class="col-md-4"><h3><a href="/ville/' + feedsData.slug + '">' + feedsData.name + '</a></h3></div>';
                } else if (feedsData.type[0] == 4) {
                    var title = '<div class="col-md-4"><h3><a href="/animation/' + feedsData.slug + '">' + feedsData.name + '</a></h3></div>';
                } else {
                    var title = '<div class="col-md-4"><h3><a href="/show/' + feedsData.slug + '">' + feedsData.name + '</a></h3></div>';
                }


            }
            post = post + title;
        }
    }
    return cursor.continue().then(logItems);
});