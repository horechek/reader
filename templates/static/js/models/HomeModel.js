function Item(id, title, summary, isRead, date) {
    this.id = id
    this.title = title;
    this.summary = summary;
    this.date = date;
    this.isRead = ko.observable(isRead);
}

function HomeModel(){
    var self = this;

    self.feeds = 'Bob'
    self.items = ko.observableArray([]);
    self.mainContent = ko.observable();
    self.mainTitle = ko.observable();
    self.mainDate = ko.observable();

    self.reloadItems = function (url, model, event) {
        $.ajax({
            url : url,
            dataType: 'json',
            method: 'get',
            success : function(data) {
                var items = [];
                $.each(data, function(index, value) {
                    (function(obj){
                        items.push(
                            new Item(
                                obj.pk, obj.fields.title, 
                                obj.fields.shortDescr, 
                                obj.fields.isRead,
                                obj.fields.date
                            )
                        )
                    })(value);
                })
                self.items(items);    
            }
        });
    }

    self.reloadMainContent = function (itemId, item, event) {
        console.dir()
        $.ajax({
            url : "/feeds/load_item_content/" + itemId + "/",
            dataType: 'json',
            method: 'get',
            success : function(data) {
                self.mainContent(data.content)
                self.mainTitle(data.title)
                self.mainDate(data.date)
                item.isRead(data.isRead)
            },
            error: function(data, stats, error) {
                console.log("login fault: " + data + ", " + 
                        stats + ", " + error);
            }
        });
    }

    self.toggleTag = function (tag_id, model, event) {
        $.ajax({
            url : "/feeds/toggle_tag/" + tag_id + "/",
            dataType: 'json',
            method: 'get',
            success : function(data) {
            },
            error: function(data, stats, error) {
                console.log("login fault: " + data + ", " + 
                        stats + ", " + error);
            }
        });
    }
}

$(function(){
    model = new HomeModel();
    ko.applyBindings(model);
})