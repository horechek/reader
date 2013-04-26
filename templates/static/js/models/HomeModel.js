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
    self.currentItem = ko.observable(false);
    self.currentType = ko.observable(false);
    self.currentListId = ko.observable(false);

    function updateTagCount(feedElemClass, unreadCount) {
        $(feedElemClass).text(unreadCount)
         var tagcount = 0;
        $(feedElemClass)
            .parent('li').parent('ul').find('.span-count')
            .each(function(index) {
                tagcount += parseInt($(this).text())
            })
        $(feedElemClass)
            .parent('li').parent('ul')
            .parent('li').find('.tag-span-count')
            .text(tagcount)
    }

    function updateMainCount() {
        $.ajax({
            url : '/feeds/get_unread_count/',
            dataType: 'json',
            method: 'get',
            success : function(data) {
                $("#main-count-span").text(data.count) 
            }
        });
    }

    self.showAll = function (model, event) {
        $.ajax({
            url : '/accounts/set_show/0/',
            dataType: 'json',
            method: 'get',
            success : function(data) {
               if (self.currentType() && self.currentListId()) {
                    self.reloadItems(self.currentListId(), self.currentType(), model, event)
                } 
            }
        });
    }

    self.showUnread = function (model, event) {
        $.ajax({
            url : '/accounts/set_show/1/',
            dataType: 'json',
            method: 'get',
            success : function(data) {
                if (self.currentType() && self.currentListId()) {
                    self.reloadItems(self.currentListId(), self.currentType(), model, event)
                }
            }
        });
    }

    self.reloadItems = function (id, type, model, event) {
        $.ajax({
            url : '/feeds/load_items/'+type+'/'+id+'/',
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
                self.currentType(type);
                self.currentListId(id);
                self.items(items);
            }
        });
    }

    self.reloadMainContent = function (itemId, item, event) {
        $.ajax({
            url : "/feeds/load_item_content/" + itemId + "/",
            dataType: 'json',
            method: 'get',
            success : function(data) {
                self.mainContent(data.content)
                self.mainTitle(data.title)
                self.mainDate(data.date)
                item.isRead(data.isRead)

                self.currentItem(itemId)
                
                updateTagCount(".feed-count-span-"+data.feedId, data.unreadCount)
                updateMainCount()
            },
            error: function(data, stats, error) {
                console.log("login fault: " + data + ", " + 
                        stats + ", " + error);
            }
        });
    }

    self.makeUnread = function (item, event) {
        if (self.currentItem()) {
            $.ajax({
                url : "/feeds/make_unread/" + self.currentItem() + "/",
                dataType: 'json',
                method: 'get',
                success : function(data) {
                    updateTagCount(".feed-count-span-"+data.feedId, data.unreadCount)
                    updateMainCount()

                    for (var i = 0; i < self.items().length; i++ ) {
                        if (self.items()[i].id == self.currentItem()) {
                            self.items()[i].isRead(0)
                        }
                    }
                },
                error: function(data, stats, error) {
                    console.log("login fault: " + data + ", " + 
                            stats + ", " + error);
                }
            });
        }
    }

    self.toggleTag = function (tagId, model, event) {
        $.ajax({
            url : "/feeds/toggle_tag/" + tagId + "/",
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