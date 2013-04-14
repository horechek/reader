function Item(id, title, summary, isRead) {
    this.id = id
    this.title = title;
    this.summary = summary;
    this.isRead = isRead;
}

function HomeModel(){
    var self = this;

    self.feeds = 'Bob'
    self.items = ko.observableArray([]);
    self.mainContent = ko.observable();
    self.mainTitle= ko.observable();

    self.reloadItems = function (feedId, data, event) {
        //ходим аяксом и забираем итемы по feedId
        $.ajax({
            url : "/feeds/load_items/" + feedId + "/",
            dataType: 'json',
            method: 'get',
            success : function(data) {
                var items = [];
                $.each(data, function(index, value) {
                    (function(obj){
                        items.push(new Item(obj.pk, obj.fields.title, obj.fields.shortDescr, 0))
                    })(value);
                })
                self.items(items);    
            }
        });
    }

    self.reloadMainContent = function (itemId, data, event) {
        //ходим аяксом и забираем контент по itemId
        $.ajax({
            url : "/feeds/load_item_content/" + itemId + "/",
            dataType: 'json',
            method: 'get',
            success : function(data) {
                self.mainContent(data.content)
                self.mainTitle(data.title)
            },
            error: function(data, stats, error) {
                console.log("login fault: " + data + ", " + 
                        stats + ", " + error);
            }
        });

        // self.mainContent("reloaded")
    }
}

$(function(){
    model = new HomeModel();
    ko.applyBindings(model);
})